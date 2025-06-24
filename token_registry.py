from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from shutil import copy2

from dotenv import load_dotenv


SECRETS_DIR = Path(__file__).resolve().parent / "MIND_SECRETS"
DEFAULT_ENV = SECRETS_DIR / "env_default.env"


def load_agent_env(agent_name: str) -> None:
    """Load environment variables for a given agent.

    If the agent specific .env file does not exist but the default
    template does, the template is copied automatically.
    """
    env_file = SECRETS_DIR / f"env_{agent_name}.env"

    if not env_file.exists() and DEFAULT_ENV.exists():
        env_file.parent.mkdir(parents=True, exist_ok=True)
        copy2(DEFAULT_ENV, env_file)

    if env_file.exists():
        load_dotenv(env_file)


def get_env_var(key: str) -> Optional[str]:
    """Return the value of an environment variable if set."""
    return os.getenv(key)
