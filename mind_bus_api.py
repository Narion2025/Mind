import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, constr

app = FastAPI()

# in-memory anchor storage
anchors: Dict[str, Dict] = {}

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

def start():
    port = int(os.environ.get("API_PORT") or os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    start()
