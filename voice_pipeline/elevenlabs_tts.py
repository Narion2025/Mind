"""Streaming wrapper for the ElevenLabs text-to-speech API."""

from __future__ import annotations

from typing import Any

from token_registry import load_agent_env, get_env_var


TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"


class ElevenLabsTTS:
    """Small wrapper around the ElevenLabs API."""

    def __init__(self, agent: str) -> None:
        load_agent_env(agent)
        self.api_key = get_env_var("ELEVENLABS_API_KEY")

    def synthesize(self, text: str, voice_id: str) -> bytes:
        """Return raw audio bytes for the given text and voice."""
        if not self.api_key:
            raise RuntimeError("ELEVENLABS_API_KEY missing")
        import requests

        url = TTS_URL.format(voice_id=voice_id)
        headers = {"xi-api-key": self.api_key}
        response = requests.post(url, json={"text": text}, headers=headers, stream=True)
        response.raise_for_status()
        return response.content
