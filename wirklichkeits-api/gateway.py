from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import jwt
from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
import yaml

app = FastAPI(openapi_tags=[{"name": "anchor", "x-openai-isConsequential": True}])

ANCHOR_DIR = Path(__file__).resolve().parents[2] / "init" / "anchors"
ANCHOR_DIR.mkdir(parents=True, exist_ok=True)

JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")
HMAC_SECRET = os.getenv("HMAC_SECRET", "")

bearer_scheme = HTTPBearer(auto_error=False)

state_subscribers: list[WebSocket] = []
last_change: Optional[str] = None

class AnchorV1(BaseModel):
    gpt_id: str = Field(..., pattern="^[a-z0-9_-]{3,32}$")
    version: Optional[str] = "1.0"
    identity: Optional[str] = None
    priority: Optional[int] = Field(0, ge=0, le=9)
    created_at: Optional[str] = None
    permissions: Optional[list[str]] = None

class PartialAnchor(BaseModel):
    version: Optional[str] = None
    identity: Optional[str] = None
    priority: Optional[int] = Field(None, ge=0, le=9)
    permissions: Optional[list[str]] = None


def verify_jwt(token: str) -> Dict[str, Any]:
    if not JWT_PUBLIC_KEY:
        raise HTTPException(status_code=500, detail="JWT_PUBLIC_KEY not configured")
    try:
        return jwt.decode(token, JWT_PUBLIC_KEY, algorithms=["RS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")


def require_role(role: str):
    def wrapper(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), req: Request = None):
        if not credentials:
            raise HTTPException(status_code=401, detail="missing credentials")
        payload = verify_jwt(credentials.credentials)
        roles = payload.get("roles", [])
        if role not in roles:
            raise HTTPException(status_code=403, detail="forbidden")
        if HMAC_SECRET:
            received = req.headers.get("X-HMAC-Signature")
            if not received:
                raise HTTPException(status_code=401, detail="missing signature")
            body = req.scope.get("body")
            if body is None:
                body = b""
            if isinstance(body, str):
                body = body.encode()
            digest = hmac.new(HMAC_SECRET.encode(), body, hashlib.sha256).digest()
            expected = base64.b64encode(digest).decode()
            if not hmac.compare_digest(received, expected):
                raise HTTPException(status_code=401, detail="bad signature")
        return payload
    return wrapper


def save_anchor(anchor: AnchorV1):
    global last_change
    anchor.created_at = anchor.created_at or datetime.utcnow().isoformat()
    path = ANCHOR_DIR / f"{anchor.gpt_id}.yaml"
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(anchor.dict(), f, sort_keys=False, allow_unicode=True)
    last_change = datetime.utcnow().isoformat()


def load_anchor(gpt_id: str) -> AnchorV1:
    path = ANCHOR_DIR / f"{gpt_id}.yaml"
    if not path.exists():
        raise HTTPException(status_code=404, detail="not found")
    data = yaml.safe_load(path.read_text())
    return AnchorV1(**data)


@app.put("/anchors/{gpt_id}", tags=["anchor"], dependencies=[Depends(require_role("anchor.write"))])
async def upsert_anchor(gpt_id: str, anchor: AnchorV1, req: Request):
    if anchor.gpt_id != gpt_id:
        raise HTTPException(status_code=400, detail="gpt_id mismatch")
    await req.body()
    req.scope["body"] = req._body  # type: ignore
    save_anchor(anchor)
    await broadcast_state()
    return {"status": "ok"}


@app.get("/anchors/{gpt_id}", tags=["anchor"], dependencies=[Depends(require_role("anchor.read"))])
async def get_anchor(gpt_id: str, req: Request):
    await req.body()
    req.scope["body"] = req._body  # type: ignore
    anchor = load_anchor(gpt_id)
    return anchor


@app.patch("/anchors/{gpt_id}", tags=["anchor"], dependencies=[Depends(require_role("anchor.write"))])
async def patch_anchor(gpt_id: str, patch: PartialAnchor, req: Request):
    await req.body()
    req.scope["body"] = req._body  # type: ignore
    anchor = load_anchor(gpt_id)
    update = anchor.dict()
    patch_data = patch.dict(exclude_none=True)
    update.update(patch_data)
    anchor = AnchorV1(**update)
    save_anchor(anchor)
    await broadcast_state()
    return {"status": "ok"}


@app.get("/state")
async def get_state():
    return {"status": "ok", "lastChange": last_change}


async def broadcast_state():
    for ws in list(state_subscribers):
        try:
            await ws.send_text(json.dumps({"lastChange": last_change}))
        except WebSocketDisconnect:
            state_subscribers.remove(ws)


@app.websocket("/ws/state")
async def ws_state(ws: WebSocket):
    await ws.accept()
    state_subscribers.append(ws)
    try:
        await ws.send_text(json.dumps({"lastChange": last_change}))
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        state_subscribers.remove(ws)


