import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, constr, root_validator, validator

app = FastAPI(openapi_tags=[
    {"name": "anchor", "x-openai-isConsequential": True},
    {"name": "action", "x-openai-isConsequential": True},
])

# in-memory anchor storage
anchors: Dict[str, Dict] = {}
update_clients: List[WebSocket] = []

bundle_dir = Path(__file__).resolve().parent / "mind_dashboard_bundle"
app.mount("/dashboard", StaticFiles(directory=str(bundle_dir), html=True), name="dashboard")

# Pydantic models
ModelLiteral = constr(regex="^(gpt-4o|claude-3|gemini-pro)$")
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

def start():
    port = int(os.environ.get("API_PORT") or os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    start()
