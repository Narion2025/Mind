from __future__ import annotations
import os
from pathlib import Path
from typing import Optional, List

try:
    from dotenv import load_dotenv  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    def load_dotenv(path=None):  # type: ignore
        if path and Path(path).exists():
            for line in Path(path).read_text().splitlines():
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k, v)

PROJECT_ROOT = Path(__file__).resolve().parent
ENV_KEYS = [
    "MINDSWARM_GITHUB_TOKEN",
    "OPENAI_API_KEY",
    "HUMEAI_API_KEY",
    "ELEVENLABS_API_KEY",
]

def generate_env_files(agent_names: List[str]) -> None:
    lines = [f"{k}={os.getenv(k,'')}" for k in ENV_KEYS]
    content = "\n".join(lines)
    for name in agent_names:
        (PROJECT_ROOT / f".env.{name}").write_text(content)

def load_agent_env(agent_name: str) -> None:
    generate_env_files([agent_name])
    env_file = PROJECT_ROOT / f".env.{agent_name}"
    if env_file.exists():
        load_dotenv(env_file)

def get_env_var(key: str) -> Optional[str]:
    return os.getenv(key)
