"""Wrapper around the Hume.ai emotion API."""

from __future__ import annotations

from typing import Any, Dict

from token_registry import load_agent_env, get_env_var


HUME_ENDPOINT = "https://api.hume.ai/v0/feels"  # minimal emotion endpoint


class HumeClient:
    """Client for the Hume.ai emotion API."""

    def __init__(self, agent: str) -> None:
        load_agent_env(agent)
        self.api_key = get_env_var("HUMEAI_API_KEY")

    def analyze(self, audio: bytes) -> Dict[str, Any]:
        """Send audio bytes to the Hume API and return the detected emotion."""
        if not self.api_key:
            raise RuntimeError("HUMEAI_API_KEY missing")
        import requests

        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(HUME_ENDPOINT, files={"file": audio}, headers=headers)
        response.raise_for_status()
        return response.json()
