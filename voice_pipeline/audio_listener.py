"""Async WebSocket audio listener."""

from __future__ import annotations

import asyncio
from typing import AsyncIterator

import websockets


async def listen(uri: str) -> AsyncIterator[bytes]:
    """Yield raw audio chunks from a WebSocket URI.

    Parameters
    ----------
    uri:
        WebSocket server URI providing opus or pcm chunks.
    """
    async with websockets.connect(uri) as ws:
        async for message in ws:
            if isinstance(message, bytes):
                yield message
            else:
                yield message.encode()
