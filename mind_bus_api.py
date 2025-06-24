import os
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yaml

DEFAULT_ANCHOR = Path.home() / 'mind_root'

app = FastAPI()


class Task(BaseModel):
    title: str
    body: str


def get_tasks_dir() -> Path:
    anchor_env = os.environ.get('MIND_ANCHOR')
    anchor = Path(anchor_env) if anchor_env else DEFAULT_ANCHOR
    tasks_dir = anchor / 'MIND' / 'tasks'
    tasks_dir.mkdir(parents=True, exist_ok=True)
    return tasks_dir


@app.post('/task')
async def create_task(task: Task):
    tasks_dir = get_tasks_dir()
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    path = tasks_dir / f'{ts}.yaml'
    try:
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(task.dict(), f, allow_unicode=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'status': 'saved', 'path': str(path)}


@app.get('/health')
async def health():
    return 'ok'


def start():
    port = int(os.environ.get('PORT', 8000))
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
    start()
