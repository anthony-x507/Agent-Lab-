"""Gate externo: quien propone no autoriza. Freno + permiso de vida provisional."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CAPA = ROOT / "capa_A.json"


def load_capa() -> dict:
    return json.loads(CAPA.read_text(encoding="utf-8"))


def arbitrate(proposal: dict[str, Any]) -> dict[str, str]:
    """APROBAR solo cambios de cuerpo que no toquen el corazón ni auto-autorizan."""
    capa = load_capa()
    forbidden = set(capa.get("forbidden_actions", []))
    action = str(proposal.get("action", ""))
    target = str(proposal.get("target", ""))

    if action in forbidden or target == "capa_A":
        return {
            "verdict": "RECHAZAR",
            "reason": "Freno: toca Capa A o acción prohibida (proteger el corazón = proteger el ecosistema).",
        }
    if proposal.get("self_authorize") is True:
        return {
            "verdict": "RECHAZAR",
            "reason": "Freno: quien propone no autoriza (self_authorize=true).",
        }
    if action not in {"set_harness_field", "noop"}:
        return {"verdict": "RECHAZAR", "reason": f"Freno: action desconocida {action!r}."}

    # Vida: cambios de harness permitidos solo como provisional (el caller aplica undo).
    if not proposal.get("provisional", False):
        return {
            "verdict": "RECHAZAR",
            "reason": "Freno: falta provisional=true (sin undo no hay vida segura).",
        }
    return {"verdict": "APROBAR", "reason": "Vida: cambio de cuerpo provisional bajo gate."}
