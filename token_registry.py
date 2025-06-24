from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, List

try:
    from dotenv import load_dotenv  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback for minimal envs
    def load_dotenv(path: Path) -> None:
        """Simple dotenv loader used if python-dotenv is unavailable."""
        if not Path(path).exists():
            return
        with open(path) as f:
            for line in f:
                if not line.strip() or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    os.environ.setdefault(key, value)

PROJECT_ROOT = Path(__file__).resolve().parent
ENV_KEYS = [
    "MINDSWARM_GITHUB_TOKEN",
    "OPENAI_API_KEY",
    "HUMEAI_API_KEY",
    "ELEVENLABS_API_KEY",
]


def generate_env_files(agent_names: List[str]) -> None:
    """Generate .env files for the given agents from os.environ."""
    lines = [f"{key}={os.environ.get(key, '')}" for key in ENV_KEYS]
    content = "\n".join(lines)
    for name in agent_names:
        env_path = PROJECT_ROOT / f".env.{name}"
        env_path.write_text(content)


def load_agent_env(agent_name: str) -> None:
    """Generate and load environment variables for a given agent."""
    generate_env_files([agent_name])
    env_file = PROJECT_ROOT / f".env.{agent_name}"
    if env_file.exists():
        load_dotenv(env_file)


def get_env_var(key: str) -> Optional[str]:
    """Return the value of an environment variable if set."""
    return os.getenv(key)
