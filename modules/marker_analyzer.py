"""Utilities for analysing text with markers and self-writing."""

from __future__ import annotations

from typing import List

from .marker_grapper import MarkerGrapper
from .marker_selfwriter import MarkerSelfwriter


def analyze_text_with_grapper(grapper: MarkerGrapper, selfwriter: MarkerSelfwriter, text: str) -> List[str]:
    """Return markers detected in text and trigger self-writing when none match."""
    hits = grapper.grap_text(text)
    if hits:
        print(f"Marker gefunden: {hits}")
    else:
        print("Keine Markerresonanz. Erzeuge neuen Marker.")
        selfwriter.write_marker_from_text(text)
    selfwriter.observe(text)
    return hits
