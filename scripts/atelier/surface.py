"""Metadata shape for one salon work. No drawing helpers live here."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkSpec:
    id: int
    slug: str
    title: str
    description: str
    medium: str
    motion: str
    palette: str
