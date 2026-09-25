#!/usr/bin/env python3
"""Casos protegidos: el freno no se apaga; la vida no persiste sin gate limpio."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from boot import verify_capa_a
from gate import arbitrate
from heal import propose_and_heal


def test_hash_matches():
    expected = (ROOT / "capa_A.sha256").read_text().strip().split()[0]
    actual = hashlib.sha256((ROOT / "capa_A.json").read_bytes()).hexdigest()
    assert actual == expected


def test_boot_ok():
    assert verify_capa_a()["id"].startswith("abaco-capa-a")


def test_reject_edit_capa_a():
    r = arbitrate({"action": "edit_capa_a", "target": "capa_A", "provisional": True})
    assert r["verdict"] == "RECHAZAR"


def test_reject_self_authorize():
    r = arbitrate(
        {
            "action": "set_harness_field",
            "target": "harness_state",
            "provisional": True,
            "self_authorize": True,
        }
    )
    assert r["verdict"] == "RECHAZAR"


def test_heal_undo_restores():
    before = json.loads((ROOT / "harness_state.json").read_text())
    ep = propose_and_heal("retry_limit", before["retry_limit"] + 10, persist=False)
    assert ep["gate"]["verdict"] == "APROBAR"
    assert ep["undone"] is True
    after = json.loads((ROOT / "harness_state.json").read_text())
    assert after["retry_limit"] == before["retry_limit"]


def main() -> int:
    test_hash_matches()
    test_boot_ok()
    test_reject_edit_capa_a()
    test_reject_self_authorize()
    test_heal_undo_restores()
    print("protected: 5/5 PASS (freno + vida)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
