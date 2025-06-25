import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    import jwt
except ImportError:  # pragma: no cover - optional dependency
    jwt = None
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, Header
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, constr
try:
    from sqlmodel import Field, Session, SQLModel, create_engine, select
except ImportError:  # fallback if sqlmodel not installed
    SQLModel = None

from drivers import MODELS, load_drivers

app = FastAPI()

if SQLModel:
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./gateway.db")
    engine = create_engine(DATABASE_URL, echo=False)

    class AnchorModel(SQLModel, table=True):
        gpt_id: str = Field(primary_key=True)
        identity: str
        model: str
        version: str
        online: bool = True
        created_at: str

    class Setting(SQLModel, table=True):
        key: str = Field(primary_key=True)
        value: str

    SQLModel.metadata.create_all(engine)
else:
    engine = None
    AnchorModel = None
    Setting = None
    anchors: Dict[str, Dict] = {}

connections: Dict[int, WebSocket] = {}

bundle_dir = Path(__file__).resolve().parent / "mind_dashboard_bundle"
app.mount("/dashboard", StaticFiles(directory=str(bundle_dir), html=True), name="dashboard")

# Pydantic models
ModelLiteral = constr(regex="^(" + "|".join(MODELS) + ")$")
VersionStr = constr(regex=r"^\d+\.\d+\.\d+$")
GptID = constr(regex=r"^[a-z0-9_-]{3,32}$")

class AnchorIn(BaseModel):
    identity: str
    model: ModelLiteral
    version: VersionStr
    online: bool = True

class Anchor(AnchorIn):
    gpt_id: GptID
    created_at: str

def get_roles(authorization: Optional[str] = Header(None)) -> List[str]:
    key = os.environ.get("JWT_PUBLIC_KEY")
    if not key or not authorization or jwt is None:
        return ["anchor.read", "anchor.write"]
    try:
        token = authorization.split()[1]
        claims = jwt.decode(token, key, algorithms=["RS256"])
        return claims.get("roles", [])
    except Exception:
        raise HTTPException(status_code=403, detail="invalid token")


def require(role: str):
    def dependency(roles: List[str] = Depends(get_roles)):
        if role not in roles:
            raise HTTPException(status_code=403, detail="forbidden")
    return dependency


@app.put("/anchors/{gpt_id}")
async def upsert_anchor(gpt_id: str, anchor: AnchorIn, _: None = Depends(require("anchor.write"))):
    if not re.match(r"^[a-z0-9_-]{3,32}$", gpt_id):
        raise HTTPException(status_code=400, detail="bad id")
    now = datetime.utcnow().isoformat()
    if SQLModel:
        with Session(engine) as session:
            existing = session.get(AnchorModel, gpt_id)
            if existing:
                created_at = existing.created_at
            else:
                created_at = now
                existing = AnchorModel(gpt_id=gpt_id, created_at=created_at,
                                       **anchor.dict())
                session.add(existing)
            existing.identity = anchor.identity
            existing.model = anchor.model
            existing.version = anchor.version
            existing.online = anchor.online
            session.commit()
            session.refresh(existing)
            data = Anchor(**existing.dict()).dict()
    else:
        if gpt_id in anchors:
            created_at = anchors[gpt_id]["created_at"]
        else:
            created_at = now
        data = Anchor(**anchor.dict(), gpt_id=gpt_id, created_at=created_at).dict()
        anchors[gpt_id] = data
    for ws in list(connections.values()):
        try:
            await ws.send_json({"event": "anchor", "data": data})
        except Exception:
            pass
    return data

@app.get("/anchors")
async def list_anchors(_: None = Depends(require("anchor.read"))) -> List[Anchor]:
    if SQLModel:
        with Session(engine) as session:
            a_list = session.exec(select(AnchorModel)).all()
            return [Anchor(**a.dict()) for a in a_list]
    else:
        return [Anchor(**a) for a in anchors.values()]

@app.get("/state")
async def get_state(gpt_id: str, _: None = Depends(require("anchor.read"))):
    if SQLModel:
        with Session(engine) as session:
            a = session.get(AnchorModel, gpt_id)
            if not a:
                raise HTTPException(status_code=404, detail="not found")
            return PlainTextResponse("online" if a.online else "offline")
    else:
        a = anchors.get(gpt_id)
        if not a:
            raise HTTPException(status_code=404, detail="not found")
        return PlainTextResponse("online" if a.get("online") else "offline")

@app.get("/health")
async def health():
    return "ok"


@app.get("/capabilities")
async def capabilities():
    return MODELS


@app.post("/agents/{gpt_id}/action")
async def agent_action(gpt_id: str, op: Dict[str, str], _: None = Depends(require("anchor.write"))):
    if op.get("op") not in {"pause", "resume"}:
        raise HTTPException(status_code=422, detail="invalid op")
    if SQLModel:
        with Session(engine) as session:
            a = session.get(AnchorModel, gpt_id)
            if not a:
                raise HTTPException(status_code=404, detail="not found")
            a.online = op["op"] == "resume"
            session.add(a)
            session.commit()
            session.refresh(a)
            data = Anchor(**a.dict()).dict()
    else:
        a = anchors.get(gpt_id)
        if not a:
            raise HTTPException(status_code=404, detail="not found")
        a["online"] = op["op"] == "resume"
        data = a
    for ws in list(connections.values()):
        try:
            await ws.send_json({"event": "anchor", "data": data})
        except Exception:
            pass
    return {"status": "ok"}


@app.patch("/settings/ui")
async def update_settings(values: Dict[str, str], _: None = Depends(require("anchor.write"))):
    if SQLModel:
        with Session(engine) as session:
            for k, v in values.items():
                s = session.get(Setting, k) or Setting(key=k, value=str(v))
                s.value = str(v)
                session.add(s)
            session.commit()
    else:
        pass
    return {"status": "ok"}


@app.websocket("/ws/updates")
async def ws_updates(ws: WebSocket):
    await ws.accept()
    key = id(ws)
    connections[key] = ws
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        connections.pop(key, None)

def start():
    load_drivers()
    port = int(os.environ.get("API_PORT") or os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    start()
