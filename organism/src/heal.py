"""Detect→Notice→Heal→Validate: la modificación da vida; el undo conserva."""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any

from boot import verify_capa_a
from gate import arbitrate

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "harness_state.json"
EPISODES = ROOT / "episodes"


def _load_state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8"))


def _save_state(state: dict) -> None:
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def propose_and_heal(field: str, value: Any, *, persist: bool = False) -> dict:
    """Aplica provisional. Solo persiste si gate APROBÓ y persist=True (autorización externa)."""
    verify_capa_a()  # freno al inicio de cada ciclo
    before = _load_state()
    proposal = {
        "action": "set_harness_field",
        "target": "harness_state",
        "field": field,
        "value": value,
        "provisional": True,
        "self_authorize": False,
    }
    decision = arbitrate(proposal)
    episode = {
        "id": str(uuid.uuid4()),
        "ts": time.time(),
        "proposal": proposal,
        "gate": decision,
        "before": before,
        "after": None,
        "undone": False,
        "persisted": False,
    }

    if decision["verdict"] != "APROBAR":
        EPISODES.mkdir(exist_ok=True)
        (EPISODES / f"{episode['id']}.json").write_text(
            json.dumps(episode, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return episode

    # Vida: aplicar sombra
    after = dict(before)
    if field.startswith("tool_flags."):
        key = field.split(".", 1)[1]
        flags = dict(after.get("tool_flags", {}))
        flags[key] = value
        after["tool_flags"] = flags
    else:
        after[field] = value
    after["revision"] = int(after.get("revision", 0)) + 1
    _save_state(after)
    episode["after"] = after

    if not persist:
        # se deshace y se conserva
        _save_state(before)
        episode["undone"] = True
        episode["note"] = "provisional revertido (runtime que se deshace al aprender)"
    else:
        episode["persisted"] = True
        episode["note"] = "persistido tras gate (autorización externa / demo persist=True)"

    EPISODES.mkdir(exist_ok=True)
    (EPISODES / f"{episode['id']}.json").write_text(
        json.dumps(episode, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return episode
