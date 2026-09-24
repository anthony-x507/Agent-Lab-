# Agent Lab

**Plan maestro:** [`docs/PLAN-MAESTRO.md`](docs/PLAN-MAESTRO.md) (fases 0–5: dataset → LoRA → QEC → cableado → experimento).

Laboratorio local (sin nube de pago) para experimentar con **visión + razonamiento + árbitro Jev + simulador cuántico** en un clúster de dos Macs Apple Silicon unidos por **Tailscale**.

Repositorio hermano de código ejecutable: [`quantum-llm-lab`](https://github.com/anthony-x507/quantum-llm-lab). Aquí documentamos la visión, el estado del clúster y los resultados de los ciclos.

## Qué es

Un loop cerrado donde:

1. Se generan **escenas sintéticas** de física simple (pelota que cae / rebotes).
2. Un VLM en la **M4** propone un **circuito cuántico toy** como “firma” del fenómeno.
3. **Jev** arbitra en binario: **APROBAR** o **RECHAZAR** (compila, energía coherente, visión vs simulador).
4. **PennyLane** (CPU) ejecuta el circuito y deja traza.
5. El feedback alimenta el dataset para un futuro **fine-tune LoRA**.

Jev **nunca otorga grants**: solo veredicto + una línea de motivo.

## Arquitectura del clúster

| Máquina | RAM | Rol | Modelo |
|---------|-----|-----|--------|
| **MacBook M4** (Tailscale `100.81.85.29`, etiqueta Mac-139) | 128 GB | Visión + razonamiento principal | `mlx-community/Qwen3-VL-8B-Thinking-4bit` (~6 GB en disco, ~12 GB en runtime) |
| **Mac Studio** (Tailscale `100.109.80.94`) | 36 GB | Verificador / ranker | Qwen3-VL **2B/4B Thinking** 4-bit |

Red: misma cuenta Tailscale. SSH M4→Studio solo cuando la Studio esté **online** (hoy suele estar offline; hay que encenderla y abrir Tailscale).

## Loop de experimentación

```
visión (escena sintética)
  → razonamiento 8B (propuesta de circuito JSON)
  → Jev árbitro (APROBAR | RECHAZAR)
  → simulador PennyLane
  → feedback → dataset → LoRA (siguiente fase)
```

Detalle de la metáfora cuántica → LLM: ver [`docs/vision-cuantica-llm.md`](docs/vision-cuantica-llm.md).

## Scripts clave

| Archivo | Rol |
|---------|-----|
| `examples/llm_quantum_bridge.py` | Puente LLM/stub → circuito → PennyLane |
| `examples/vision_grounding.py` | Frames sintéticos + grounding (`--demo` / `--mlx`) |
| `examples/synthetic_physics_dataset.py` | Generador masivo de escenas (LoRA) |
| `examples/jev_arbiter.py` | Árbitro APROBAR/RECHAZAR |
| `requirements.txt` | Dependencias (PennyLane + MLX en Darwin) |

## Estado actual (2026-09-23)

- Lab ejecutable en `quantum-llm-lab` tip `e4f2928` (dataset sintético + cluster README).
- Primer ciclo de 5 escenas con el **8B Thinking** en la M4: **en curso** (descarga HF).
- Plan LoRA listo (`docs/lora_plan.md` + `train_lora.py` / `eval_lora.py`); ejecutar tras dataset+modelo. (instalación mlx-vlm + descarga del modelo). El log vivo irá en `data/experiment_log.jsonl`.
- Mac Studio: Tailscale **offline** (~20 días); el ranker 2B/4B espera a que vuelva.
- Sin Cloud Agents para este carril (crédito Cursor); todo local / `gh`.

## Cómo correr (en la M4)

```bash
git clone https://github.com/anthony-x507/quantum-llm-lab.git
cd quantum-llm-lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Demostración sin pesos:
python examples/vision_grounding.py --demo --pipeline
python examples/jev_arbiter.py --self-test
```

VLM real:

```bash
pip install -U mlx mlx-lm mlx-vlm
python examples/vision_grounding.py --mlx \
  --model mlx-community/Qwen3-VL-8B-Thinking-4bit
```

## Licencia / uso

Proyecto de experimentación personal de Anthony Sanchez / ABACO. Código y notas en español.

## Fine-tune con LoRA

Plan completo: [`docs/lora_plan.md`](docs/lora_plan.md).

**Cuándo lanzarlo:** cuando tengas `data/scenes/` con ~200+ escenas mixtas (caídas + figuras nuevas + entrelazamiento + superposición) y el 8B Thinking 4-bit ya cacheado en la M4.

**Qué esperar:** ~2–3 h en M4 128 GB (rank 32, 3 epochs, QLoRA). El adapter queda en `data/lora_adapter/` (megabytes). Éxito = +20 puntos en tasa Jev APROBAR sobre 10 escenas de prueba vs el base.

```bash
python examples/synthetic_physics_dataset.py --n-scenes 280 --out data/scenes --seed 42
python examples/train_lora.py --rank 32 --alpha 32 --lr 2e-4 --epochs 3
python examples/eval_lora.py --adapter data/lora_adapter --n-test 10
```

**Cargar el adapter:**

```python
from mlx_vlm import load
model, processor = load(
    "mlx-community/Qwen3-VL-8B-Thinking-4bit",
    adapter_path="data/lora_adapter",
)
```

Fase 3 (QEC): [`docs/quantum_error_correction.md`](docs/quantum_error_correction.md) — `python examples/qec_robustness.py --self-test`.

Nota: el entrenamiento usa **mlx-vlm** (VLM), no solo mlx-lm; Qwen3-VL necesita el stack de visión.

