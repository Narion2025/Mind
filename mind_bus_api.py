import os
import re
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import jwt

import asyncio
import subprocess
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, constr, root_validator, validator
from agent_manager import create_agent

app = FastAPI(openapi_tags=[
    {"name": "anchor", "x-openai-isConsequential": True},
    {"name": "action", "x-openai-isConsequential": True},
])

# in-memory anchor storage
anchors: Dict[str, Dict] = {}
update_clients: List[WebSocket] = []

# runtime management for functions
processes: Dict[str, asyncio.subprocess.Process] = {}
log_queues: Dict[str, asyncio.Queue] = {}

# parse function map markdown
def load_function_map() -> List[Dict]:
    path = Path(__file__).resolve().parent / "MIND_FUNCTION_MAP.md"
    entries = []
    current_group = None
    current = None
    if not path.exists():
        return entries
    for raw in path.read_text().splitlines():
        line = raw.strip()
        m = re.match(r"^## Gruppe: (.+)", line)
        if m:
            current_group = m.group(1)
            continue
        m = re.match(r"^### Datei: (.+)", line)
        if m:
            current = {
                "name": m.group(1),
                "group": current_group or "Misc",
                "description": "",
                "env_missing": [],
            }
            entries.append(current)
            continue
        m = re.match(r"^Funktionen?: (.+)", line)
        if m and current:
            current["description"] = m.group(1)
            continue
        m = re.match(r"^Status: (.+)", line)
        if m and current:
            status = m.group(1)
            if "benötigt" in status:
                req = status.split("benötigt", 1)[1]
                vars = re.split(r"und|,", req)
                current["env_missing"] = [v.strip() for v in vars if v.strip()]
    return entries

function_map = load_function_map()

bundle_dir = Path(__file__).resolve().parent / "mind_dashboard_bundle"
app.mount("/dashboard", StaticFiles(directory=str(bundle_dir), html=True), name="dashboard")

user_file = Path(__file__).resolve().parent / "user_accounts.json"
lineage_file = Path(__file__).resolve().parent / "lineage_index.json"
ethic_file = Path(__file__).resolve().parent / "ethic_ledger.json"

token_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(token_scheme)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, os.environ.get("JWT_SECRET", "secret"), algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="invalid token")
    return payload.get("sub")

def load_users() -> Dict:
    if user_file.exists():
        return json.loads(user_file.read_text())
    return {"users": []}

def save_users(data: Dict) -> None:
    user_file.write_text(json.dumps(data, indent=2))

def load_ethics() -> Dict:
    if ethic_file.exists():
        return json.loads(ethic_file.read_text())
    return {"users": {}}

def save_ethics(data: Dict) -> None:
    ethic_file.write_text(json.dumps(data, indent=2))

# Pydantic models
# ``constr`` changed the ``regex`` parameter name to ``pattern`` in
# pydantic v2. Detect the installed version and use the appropriate
# keyword so the API works under both v1 and v2.
import pydantic

_constr_kw = 'pattern' if pydantic.version.VERSION.startswith('2') else 'regex'
ModelLiteral = constr(**{_constr_kw: "^(gpt-4o|claude-3|gemini-pro)$"})
VersionStr = constr(**{_constr_kw: r"^\d+\.\d+\.\d+$"})
GptID = constr(**{_constr_kw: r"^[a-z0-9_-]{3,32}$"})

class AnchorIn(BaseModel):
    identity: str
    model: ModelLiteral
    version: VersionStr
    online: bool = True

class Anchor(AnchorIn):
    gpt_id: GptID
    created_at: str


class AgentAction(BaseModel):
    op: str
    model: Optional[ModelLiteral] = None
    identity: Optional[str] = None
    params: Optional[Dict] = None

    @validator('op')
    def validate_op(cls, v):
        if v not in {'connect', 'pause', 'delete'}:
            raise ValueError('invalid op')
        return v

    @root_validator
    def connect_requires_fields(cls, values):
        if values.get('op') == 'connect':
            if values.get('model') is None or values.get('params') is None:
                raise ValueError('model and params required')
        return values

    class Config:
        extra = 'forbid'


class NewAgent(BaseModel):
    name: constr(**{_constr_kw: r"^[a-zA-Z0-9_-]{1,32}$"})
    farbe: str
    fokus: str
    beschreibung: str


class RegisterData(BaseModel):
    username: constr(**{_constr_kw: r"^[a-zA-Z0-9_-]{3,32}$"})
    email: constr(**{_constr_kw: r"^[^@\s]+@[^@\s]+\.[^@\s]+$"})
    password: str


class LoginData(BaseModel):
    username: str
    password: str


@app.put("/anchors/{gpt_id}")
async def upsert_anchor(gpt_id: str, anchor: AnchorIn):
    if not re.match(r"^[a-z0-9_-]{3,32}$", gpt_id):
        raise HTTPException(status_code=400, detail="bad id")
    now = datetime.utcnow().isoformat()
    if gpt_id in anchors:
        created_at = anchors[gpt_id]["created_at"]
    else:
        created_at = now
    data = Anchor(**anchor.dict(), gpt_id=gpt_id, created_at=created_at).dict()
    anchors[gpt_id] = data
    return data

@app.get("/anchors")
async def list_anchors() -> List[Anchor]:
    return list(anchors.values())

@app.get("/state")
async def get_state(gpt_id: str):
    if gpt_id not in anchors:
        raise HTTPException(status_code=404, detail="not found")
    return PlainTextResponse("online")

@app.get("/health")
async def health():
    return "ok"


async def broadcast_update(event: str, gpt_id: str):
    for ws in list(update_clients):
        try:
            await ws.send_json({"event": event, "id": gpt_id})
        except WebSocketDisconnect:
            update_clients.remove(ws)


@app.websocket("/ws/updates")
async def ws_updates(ws: WebSocket):
    await ws.accept()
    update_clients.append(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        update_clients.remove(ws)


@app.post("/agents/{gpt_id}/action", tags=["action"])
async def agent_action(gpt_id: str, payload: AgentAction):
    if payload.op == "connect":
        now = datetime.utcnow().isoformat()
        created_at = anchors.get(gpt_id, {}).get("created_at", now)
        anchors[gpt_id] = {
            "gpt_id": gpt_id,
            "identity": payload.identity,
            "model": payload.model,
            "version": anchors.get(gpt_id, {}).get("version", "1.0.0"),
            "online": True,
            "created_at": created_at,
            "config": {
                "identity": payload.identity,
                "model": payload.model,
                "params": payload.params,
            },
        }
        await broadcast_update("anchor-connected", gpt_id)
        return anchors[gpt_id]
    if gpt_id not in anchors:
        raise HTTPException(status_code=404, detail="not found")
    if payload.op == "pause":
        anchors[gpt_id]["online"] = False
        await broadcast_update("anchor-paused", gpt_id)
        return anchors[gpt_id]
    if payload.op == "delete":
        anchors.pop(gpt_id)
        await broadcast_update("anchor-deleted", gpt_id)
        return {"status": "deleted"}
    raise HTTPException(status_code=400, detail="invalid op")


@app.post('/register')
async def register(data: RegisterData):
    users = load_users()
    if any(u['username'] == data.username for u in users['users']):
        raise HTTPException(status_code=400, detail='exists')
    pwd = hashlib.sha256(data.password.encode()).hexdigest()
    users['users'].append({'username': data.username, 'email': data.email, 'password': pwd})
    save_users(users)
    ledger = load_ethics()
    if data.username not in ledger['users']:
        ledger['users'][data.username] = 0
        save_ethics(ledger)
    if lineage_file.exists():
        ldata = json.loads(lineage_file.read_text())
    else:
        ldata = {'lineage': [], 'last_updated': ''}
    ldata['lineage'].append({
        'name': data.username,
        'introduced_by': 'self',
        'date': datetime.utcnow().date().isoformat(),
        'ritual': 'self-register'
    })
    ldata['last_updated'] = datetime.utcnow().date().isoformat()
    lineage_file.write_text(json.dumps(ldata, indent=2))
    return {'status': 'registered'}


@app.post('/login')
async def login(data: LoginData):
    users = load_users()
    pwd = hashlib.sha256(data.password.encode()).hexdigest()
    if not any(u['username'] == data.username and u['password'] == pwd for u in users['users']):
        raise HTTPException(status_code=401, detail='invalid')
    token = jwt.encode({'sub': data.username, 'exp': datetime.utcnow() + timedelta(hours=1)}, os.environ.get('JWT_SECRET', 'secret'), algorithm='HS256')
    return {'token': token}


@app.get('/ethic')
async def get_ethic_balance(user: str = Depends(get_current_user)):
    ledger = load_ethics()
    return {'coins': ledger['users'].get(user, 0)}


@app.post('/ethic/resonate')
async def resonate(user: str = Depends(get_current_user)):
    ledger = load_ethics()
    ledger['users'][user] = ledger['users'].get(user, 0) + 1
    save_ethics(ledger)
    return {'coins': ledger['users'][user]}


@app.post('/agents', tags=['agent'])
async def create_new_agent(agent: NewAgent):
    create_agent(agent.name, agent.farbe, agent.fokus, agent.beschreibung)
    return {'status': 'created'}


# --- Function control API ---

def build_cmd(name: str) -> List[str]:
    if name.endswith('.sh'):
        return ['bash', name]
    if name.endswith('.js'):
        return ['node', name]
    if name.endswith('.py'):
        return ['python3', name]
    raise HTTPException(status_code=400, detail='unknown file type')


@app.get("/functions")
async def get_functions():
    results = []
    for entry in function_map:
        status = 'stopped'
        proc = processes.get(entry['name'])
        if proc and proc.returncode is None:
            status = 'running'
        results.append({
            **entry,
            'runtime_status': status,
        })
    return results


@app.post("/functions/{name}/start")
async def start_function(name: str, tasks: BackgroundTasks):
    entry = next((e for e in function_map if e['name'] == name), None)
    if not entry:
        raise HTTPException(status_code=404, detail='not found')
    if name in processes and processes[name].returncode is None:
        raise HTTPException(status_code=400, detail='already running')

    cmd = build_cmd(name)
    queue: asyncio.Queue = asyncio.Queue()
    log_queues[name] = queue

    async def run():
        proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
        processes[name] = proc
        async for line in proc.stdout:
            await queue.put(line.decode().rstrip())
        await proc.wait()
        await queue.put(None)

    tasks.add_task(run)
    return {"status": "started"}


@app.websocket("/ws/logs/{name}")
async def ws_logs(ws: WebSocket, name: str):
    await ws.accept()
    queue = log_queues.get(name)
    if queue is None:
        await ws.close()
        return
    try:
        while True:
            line = await queue.get()
            if line is None:
                await ws.close()
                break
            await ws.send_text(line)
    except WebSocketDisconnect:
        pass


@app.websocket("/ws/terminal")
async def ws_terminal(ws: WebSocket):
    """Provide a simple interactive shell over WebSocket.

    Access is gated via the ``ENABLE_TERMINAL`` environment variable. If it is
    not set to ``"1"`` the connection will be closed immediately.
    """
    await ws.accept()
    if os.environ.get("ENABLE_TERMINAL") != "1":
        await ws.close(code=1008)
        return

    proc = await asyncio.create_subprocess_exec(
        "bash", "-i",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    async def read_stream():
        while True:
            data = await proc.stdout.readline()
            if not data:
                break
            await ws.send_text(data.decode())

    reader = asyncio.create_task(read_stream())
    try:
        while True:
            msg = await ws.receive_text()
            proc.stdin.write(msg.encode())
            await proc.stdin.drain()
    except WebSocketDisconnect:
        pass
    finally:
        proc.kill()
        await proc.wait()
        reader.cancel()


@app.get('/env')
async def env_status():
    out: Dict[str, List[str]] = {}
    for entry in function_map:
        missing = []
        for var in entry['env_missing']:
            if var and not os.environ.get(var):
                missing.append(var)
        if missing:
            out[entry['name']] = missing
    return out

def start():
    port = int(os.environ.get("API_PORT") or os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    start()
