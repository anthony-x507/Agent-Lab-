# Organism stub — freno + vida

Stub mínimo (2026-09-25) que baja la hipótesis de *pensamiento elevado* a código:

- **Freno (corazón / Capa A):** `capa_A.json` + `capa_A.sha256`. `boot.py` hace HALT si el hash no cuadra. `gate.py` rechaza editar el corazón, apagar escotillas o auto-autorizar.
- **Vida (modificación):** `heal.py` aplica un cambio de harness en provisional y **se deshace** (salvo `persist=True` tras gate limpio). Episodios en `episodes/`.

> El corazón no cambia; todo lo demás cambia para merecer ese corazón.

## Correr

```bash
cd organism
python3 src/boot.py
python3 demo_cycle.py
python3 protected/test_freno_y_vida.py
```

## Qué no es aún

No es auto-mod de código real, ni LoRA de carácter, ni telemetría de usuario. Es el esqueleto L4 mínimo del estudio de viabilidad: freno arquitectónico + undo como vida.
