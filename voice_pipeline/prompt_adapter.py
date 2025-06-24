"""Adapt prompts based on detected emotion."""

from __future__ import annotations


def adapt_prompt(text: str, emotion: str) -> str:
    """Return the text prefixed with the emotion tag."""
    tag = emotion.upper() if emotion else "NEUTRAL"
    return f"[{tag}] {text}"
