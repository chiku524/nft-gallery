#!/usr/bin/env python3
"""Write every Pugs On The Block trait as SVG + PNG, already seated on the 1024 canvas."""

from __future__ import annotations

from pathlib import Path

from potb_art import write_all


def main() -> int:
    write_all(Path(__file__).resolve().parents[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
