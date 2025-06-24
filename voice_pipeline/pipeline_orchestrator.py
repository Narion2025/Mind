"""Coordinate the entire voice pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path
import base64

from .hume_client import HumeClient
from .prompt_adapter import adapt_prompt
from .elevenlabs_tts import ElevenLabsTTS

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover
    yaml = None

if yaml:
    VOICE_MAP = yaml.safe_load((Path(__file__).parent / "voices.yaml").read_text())
else:  # simple fallback parser for "key: value" yaml
    VOICE_MAP = {}
    for line in (Path(__file__).parent / "voices.yaml").read_text().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            VOICE_MAP[k.strip()] = v.strip().strip('"')


def resolve_voice(agent: str, voice_id: str | None) -> str:
    """Return voice id for agent or fallback."""
    if voice_id:
        return voice_id
    return VOICE_MAP.get(agent, VOICE_MAP.get("default"))


def run_pipeline(agent: str, text: str, voice_id: str | None = None) -> dict:
    """Run emotion detection, adapt prompt and synthesize audio."""
    hume = HumeClient(agent)
    # In real use audio would be analyzed; here text only
    emotion_data = hume.analyze(b"")
    emotion = emotion_data.get("emotion", "neutral")
    prompt = adapt_prompt(text, emotion)
    tts = ElevenLabsTTS(agent)
    audio = tts.synthesize(prompt, resolve_voice(agent, voice_id))
    return {"emotion": emotion, "prompt": prompt, "audio": audio}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run voice pipeline")
    parser.add_argument("--agent", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--voice")
    args = parser.parse_args()
    result = run_pipeline(args.agent, args.text, args.voice)
    # Stream raw bytes to stdout
    import sys
    sys.stdout.buffer.write(result["audio"])


if __name__ == "__main__":
    main()
