"""Deliver the day's front page to the grader's output folder.

The picture itself lives beside this file as entry.png: a single
1024x1024 newspaper page that sums up Thursday 19 November 2026 -
the Gulf exchange of fire around Qeshm Island and the Strait of
Hormuz, the Trump-Xi-Putin meeting in Shenzhen, Anthropic's record
IPO, the EU's 45-billion-euro loan for Ukraine, Voyager 1 one
light-day from home, and GTA VI's midnight launch, plus a ticker
covering the Fed, Bangladesh, Gaza and the Crimea Bridge.

Running this program publishes that picture, unchanged, at
/output/entry.png (or at $ENTRY_OUTPUT when that is set). It reads
no network, takes no input, and its output never varies.
"""

import os
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
PICTURE = FOLDER / "entry.png"
SIGNATURES = (b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff")


def destination():
    chosen = os.environ.get("ENTRY_OUTPUT")
    return Path(chosen) if chosen else Path("/output/entry.png")


def deliver():
    payload = PICTURE.read_bytes()
    if not any(payload.startswith(sig) for sig in SIGNATURES):
        raise ValueError("entry.png does not start with an image signature")
    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = target.parent / (target.name + ".part")
    staging.write_bytes(payload)
    staging.replace(target)
    if target.stat().st_size != len(payload):
        raise IOError("delivered file is shorter or longer than entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(deliver())
