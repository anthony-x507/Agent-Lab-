"""Boot del organismo: si el corazón no verifica, no late la mente."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPA = ROOT / "capa_A.json"
HASHF = ROOT / "capa_A.sha256"


def verify_capa_a() -> dict:
    if not CAPA.is_file() or not HASHF.is_file():
        raise SystemExit("FRENO: falta capa_A.json o capa_A.sha256 — no arranco.")
    expected = HASHF.read_text().strip().split()[0]
    actual = hashlib.sha256(CAPA.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(
            f"FRENO: Capa A alterada sin firma. expected={expected[:12]}… actual={actual[:12]}… HALT."
        )
    data = json.loads(CAPA.read_text(encoding="utf-8"))
    return data


def main() -> int:
    capa = verify_capa_a()
    print(f"OK boot — corazón intacto ({capa['id']}, {len(capa['principles'])} principios).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
