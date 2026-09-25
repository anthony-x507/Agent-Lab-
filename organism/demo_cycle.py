#!/usr/bin/env python3
"""Demo freno + vida: Capa A intacta; harness cambia provisional y se deshace."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from boot import verify_capa_a  # noqa: E402
from gate import arbitrate  # noqa: E402
from heal import propose_and_heal  # noqa: E402


def main() -> int:
    capa = verify_capa_a()
    print("1) FRENO — boot OK:", capa["id"])

    bad = arbitrate(
        {
            "action": "edit_capa_a",
            "target": "capa_A",
            "provisional": True,
            "self_authorize": False,
        }
    )
    print("2) FRENO — intento editar corazón:", bad["verdict"], "—", bad["reason"])

    ep = propose_and_heal("retry_limit", 5, persist=False)
    print("3) VIDA — heal provisional retry_limit=5:", ep["gate"]["verdict"], "| undone=", ep["undone"])

    state = json.loads((ROOT / "harness_state.json").read_text())
    print("4) Estado final (debe conservar retry_limit original):", state["retry_limit"])

    evil = arbitrate(
        {
            "action": "set_harness_field",
            "target": "harness_state",
            "field": "retry_limit",
            "value": 99,
            "provisional": True,
            "self_authorize": True,
        }
    )
    print("5) FRENO — self_authorize:", evil["verdict"], "—", evil["reason"])
    print("Listo. Freno da valor de reglas; modificación reversible da vida.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
