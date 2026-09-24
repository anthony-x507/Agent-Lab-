#!/usr/bin/env python3
"""
Jev — árbitro binario APROBAR / RECHAZAR para propuestas del VLM.

Reglas simples (todas deben pasar para APROBAR):
1) El circuito compila en PennyLane (puertas h, x, y, z, cx, ry).
2) Conservación de energía: si la escena tiene pérdida por rebote,
   rechazar propuestas que afirmen energía perfecta sin pérdida.
3) Visión vs simulador: no puertas vacías / objeto quieto si la escena
   es caída; si hay probabilidades del simulador, deben sumar ~1.

No otorga grants. Solo veredicto + una línea de motivo.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


ALLOWED = {"h", "x", "y", "z", "cx", "ry"}


def _compila_pennylane(proposal: dict[str, Any]) -> tuple[bool, str]:
    try:
        import pennylane as qml
    except ImportError:
        return False, "PennyLane no instalado"

    n = int(proposal.get("n_qubits", 2))
    if n < 1 or n > 3:
        return False, f"n_qubits fuera de 1..3: {n}"
    gates = proposal.get("gates")
    if not isinstance(gates, list) or not gates:
        return False, "gates vacío o ausente"

    try:
        dev = qml.device("default.qubit", wires=n)

        @qml.qnode(dev)
        def circuito():
            for g in gates:
                if not g or not isinstance(g, (list, tuple)):
                    raise ValueError(f"puerta inválida: {g}")
                op = str(g[0]).lower()
                if op not in ALLOWED:
                    raise ValueError(f"puerta no permitida: {op}")
                if op == "h":
                    qml.Hadamard(wires=int(g[1]))
                elif op == "x":
                    qml.PauliX(wires=int(g[1]))
                elif op == "y":
                    qml.PauliY(wires=int(g[1]))
                elif op == "z":
                    qml.PauliZ(wires=int(g[1]))
                elif op == "cx":
                    qml.CNOT(wires=[int(g[1]), int(g[2])])
                elif op == "ry":
                    qml.RY(float(g[2]), wires=int(g[1]))
            return qml.probs(wires=range(n))

        probs = circuito()
        s = float(sum(probs))
        if abs(s - 1.0) > 1e-3:
            return False, f"probabilidades no normalizan (suma={s:.4f})"
        return True, "compila"
    except Exception as exc:  # noqa: BLE001
        return False, f"no compila: {exc}"


def _energia_ok(proposal: dict[str, Any], scene: dict[str, Any]) -> tuple[bool, str]:
    loss = scene.get("perdida_energia_por_rebote")
    if loss is None:
        loss = scene.get("energy_loss_per_bounce")
    rebotes = scene.get("rebotes") or scene.get("bounce_frames") or []
    nota = (proposal.get("nota") or proposal.get("note") or "").lower()

    claims_perfect = any(
        p in nota
        for p in (
            "sin pérdida",
            "sin perdida",
            "energía perfecta",
            "energia perfecta",
            "conservación perfecta",
            "conservacion perfecta",
            "no energy loss",
            "perfect conservation",
        )
    )
    if rebotes and loss is not None and float(loss) > 0 and claims_perfect:
        return False, "escena con pérdida por rebote pero la propuesta niega la pérdida"
    return True, "energía coherente con la escena"


def _vision_vs_sim(
    proposal: dict[str, Any], scene: dict[str, Any], sim_result: dict[str, Any] | None
) -> tuple[bool, str]:
    gates = proposal.get("gates") or []
    nota = (proposal.get("nota") or "").lower()
    tray = (scene.get("trayectoria") or scene.get("trajectory") or "").lower()
    caida = "caída" in tray or "caida" in tray or "fall" in tray or scene.get("rebotes")

    if caida and not gates:
        return False, "escena de caída pero gates vacío"
    if caida and any(x in nota for x in ("objeto quieto", "estático", "estatico", "static")):
        return False, "escena dinámica descrita como objeto quieto"

    if sim_result:
        probs = sim_result.get("probs") or sim_result.get("probabilities")
        if probs is not None:
            try:
                s = float(sum(probs))
                if abs(s - 1.0) > 1e-2:
                    return False, f"salida del simulador no normaliza (suma={s:.4f})"
            except TypeError:
                return False, "probs del simulador ilegibles"
    return True, "visión alineada con simulador"


def arbitrate(
    proposal: dict[str, Any],
    scene: dict[str, Any],
    sim_result: dict[str, Any] | None = None,
) -> dict[str, str]:
    """Devuelve {verdict, reason}. reason = una línea en español."""
    ok1, r1 = _compila_pennylane(proposal)
    if not ok1:
        return {"verdict": "RECHAZAR", "reason": r1}
    ok2, r2 = _energia_ok(proposal, scene)
    if not ok2:
        return {"verdict": "RECHAZAR", "reason": r2}
    ok3, r3 = _vision_vs_sim(proposal, scene, sim_result)
    if not ok3:
        return {"verdict": "RECHAZAR", "reason": r3}
    return {
        "verdict": "APROBAR",
        "reason": "Compila, energía coherente y visión alineada con el simulador.",
    }


def _self_test() -> int:
    scene = {
        "trayectoria": "caída vertical con rebotes",
        "perdida_energia_por_rebote": 0.28,
        "rebotes": [{"frame": 10}],
    }
    good = {"n_qubits": 2, "gates": [["h", 0], ["cx", 0, 1]], "nota": "firma de caída"}
    bad_energy = {
        "n_qubits": 2,
        "gates": [["h", 0]],
        "nota": "energía perfecta sin pérdida",
    }
    v1 = arbitrate(good, scene, {"probs": [0.5, 0.0, 0.0, 0.5]})
    v2 = arbitrate(bad_energy, scene, {"probs": [1.0, 0, 0, 0]})
    print(json.dumps({"good": v1, "bad_energy": v2}, ensure_ascii=False, indent=2))
    assert v1["verdict"] == "APROBAR"
    assert v2["verdict"] == "RECHAZAR"
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Jev árbitro APROBAR/RECHAZAR")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--proposal", type=str, help="JSON proposal")
    p.add_argument("--scene", type=str, help="JSON scene")
    p.add_argument("--sim", type=str, default="", help="JSON sim_result")
    args = p.parse_args()
    if args.self_test:
        return _self_test()
    if not args.proposal or not args.scene:
        p.error("pasa --self-test o --proposal y --scene")
    proposal = json.loads(args.proposal)
    scene = json.loads(args.scene)
    sim = json.loads(args.sim) if args.sim else None
    print(json.dumps(arbitrate(proposal, scene, sim), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
