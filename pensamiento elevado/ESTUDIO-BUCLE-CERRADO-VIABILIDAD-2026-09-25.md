# Estudio: hasta dónde llega el bucle cerrado de auto-mejora

**Fecha:** 25 de septiembre de 2026  
**Alcance:** hipótesis agente-organismo (constitución + harness + tests propios + auto-modificación + LoRA continuo) confrontada con el código y docs reales de [`anthony-x507/Agent-Lab-`](https://github.com/anthony-x507/Agent-Lab-)  
**Fuentes primarias:** `pensamiento elevado/PLAN-AGENTE-ORGANISMO-LORA-2026-09-24.md`, `TRANSCRIPCION-LIMPIA-2026-09-24.md`, resto de esa carpeta; más `examples/*`, `docs/PLAN-MAESTRO.md`, `docs/lora_plan.md`, `data/*`, `README.md`, `cluster.yaml`  
**Método:** inventario de blobs en `main` (37 archivos), lectura de scripts Python y contraste pieza a pieza con el plan del organismo. Sin inventar artefactos que no estén en el repo.

---

## Resumen ejecutivo (veredicto en una página)

**Hoy el repo tiene dos cosas distintas que aún no se tocan:**

1. **Pensamiento elevado** — filosofía y plan de producto del *agente-organismo* (cuerpo / mente / corazón). Todo es **documento**. Cero runtime que monte Capa A, haga undo, o entrene un LoRA de carácter.
2. **Agent Lab (carril cuántico)** — un **bucle de laboratorio** visión → propuesta de circuito → árbitro **Jev** → PennyLane → (futuro) LoRA de física. Aquí sí hay **código ejecutable** y un gate binario real, pero el dominio es circuitos toy / física sintética, no constitución ni auto-modificación del harness.

**Hasta dónde es viable hoy:**  
cerrar un **medio-bucle de dominio estrecho** (proponer → arbitraje externo → log → eventualmente LoRA de dominio) es **viable y ya está bosquejado en código**.  
cerrar el **bucle organismo** (constitución intocable + harness que se edita a sí mismo + tests protegidos de carácter + LoRA de corazón + actualización continua con uso del usuario) **no es viable hoy en este repo**: falta casi toda la Capa A como arquitectura, el ciclo Detect→Notice→Heal→Validate sobre el propio código, y los datos/adaptadores de carácter.

**Punto de quiebre más claro en el código existente:** el loop del README se corta entre *feedback* y *dataset/LoRA* — `data/scenes/` y `data/lora_adapter/` están vacíos (solo `.gitkeep`), `experiment_log.jsonl` tiene **0 filas**, y no hay proceso que proponga ni aplique cambios al harness bajo gate.

---

## 1. Qué ya es implementación real vs. qué es solo descripción

Leyenda: **REAL** = hay código o artefacto ejecutable/verificable en el repo · **PARCIAL** = script o stub sin datos / sin cableado vivo · **SOLO DOC** = markdown / diseño · **AUSENTE** = ni doc de fase ni código en este repo.

### 1.1 Piezas de la hipótesis organismo (`pensamiento elevado` + plan LoRA organismo)

| Pieza de la hipótesis | Estado en Agent-Lab- | Evidencia concreta |
|------------------------|----------------------|--------------------|
| Texto de constitución / Capa A–B | **SOLO DOC** | `CONSTITUCION-LLM-VIVA-*.md`, transcripción, hipótesis |
| Capa A como archivo RO + hash al boot | **AUSENTE** | Ningún script verifica hash ni monta RO; constitución es markdown editable en git |
| Escotilla humana arquitectónica | **AUSENTE** | No hay señal `STOP`, proceso watchdog ni kill switch en código del lab |
| Separación propone / provisional / autoriza | **SOLO DOC** (+ **análogo débil** en Jev) | Plan lo exige; Jev solo arbitra *circuitos*, no cambios de harness |
| Gate + suite de casos protegidos (carácter) | **AUSENTE** | No hay `tests/protected/` ni checklist honor/refuse-A-edit |
| Runtime reversible (apply + undo de harness) | **AUSENTE** | Cero shadow config / undo log en el repo |
| Auto-modelo / memoria episódica de fallos | **PARCIAL (otro dominio)** | `experiment_log.jsonl` previsto pero vacío; no modela estado del harness |
| Dataset LoRA de *presión / corazón* | **AUSENTE** | Plan §3 describe JSONL de presión; no hay carpeta ni generador |
| LoRA de carácter (`heart-v1`) | **AUSENTE** | `data/lora_adapter/` vacío |
| Bucle autogeneración desde uso del usuario | **AUSENTE** | Lab usa escenas sintéticas, no telemetría de chat de usuario |
| Límite CPU / checkpoint / reanudación | **SOLO DOC** | Hipótesis + plan §5; ningún checkpoint de organismo |
| Modificación propia del código del agente | **AUSENTE** | Ningún módulo propone patches al propio repo bajo gate |

### 1.2 Piezas del lab cuántico (lo que *sí* está en `examples/`)

| Pieza | Estado | Evidencia |
|-------|--------|-----------|
| Generador de escenas sintéticas | **REAL (script)** | `examples/synthetic_physics_dataset.py` (~31 KB) |
| Escenas generadas en repo | **PARCIAL** | `data/scenes/` solo `.gitkeep` — dataset no materializado en git |
| Bridge LLM → circuito → PennyLane | **REAL** | `examples/llm_quantum_bridge.py` (+ modo `--demo`) |
| Visión / grounding sintético | **REAL** | `examples/vision_grounding.py`, `vision/*` |
| Árbitro externo binario (Jev) | **REAL** | `examples/jev_arbiter.py` — APROBAR/RECHAZAR; `--self-test` |
| Ciclo experimento N escenas | **PARCIAL** | `run_jev_experiment.py` existe; log en repo = 0 líneas |
| Train / eval LoRA (mlx-vlm, dominio física) | **PARCIAL** | `train_lora.py` / `eval_lora.py` listos; sin adapter ni train corrido en repo |
| QEC toy / robustez de prompt | **REAL (script + doc)** | `qec_robustness.py`, `docs/quantum_error_correction.md` |
| Clúster M4 + Studio | **SOLO CONFIG/DOC** | `cluster.yaml`, README; Studio offline en notas de estado |
| Plan maestro fases 0–5 | **SOLO DOC + scripts** | `docs/PLAN-MAESTRO.md` — fases 1–2–4–5 abiertas por datos/modelo |

### 1.3 Lectura honesta de la metáfora

Jev es el **único gate externo implementado**. Encaja filosóficamente con “quien propone no autoriza”, pero **arbitra coherencia física de un JSON de circuito**, no integridad constitucional ni no-regresión de casos protegidos de agente.  
El LoRA del lab afila **intuición de dominio (caídas / entrelazamiento / superposición)**, no el **carácter bajo presión** del plan organismo.  
Son **primos metafóricos**, no el mismo producto.

---

## 2. Dónde se rompe o se vuelve inestable el bucle cerrado (según el código)

Diagrama del loop que el README afirma:

```
visión → razonamiento 8B → Jev → PennyLane → feedback → dataset → LoRA → (vuelve a razonar)
```

### 2.1 Quiebres observados en este repo

| Eslabón | Qué dice el diseño | Qué hay en `main` | Modo de rotura |
|---------|--------------------|--------------------|----------------|
| Visión | Escenas sintéticas | Generador sí; **carpeta `data/scenes/` vacía** | Sin input persistido en git; el loop no arranca reproducible desde el repo solo |
| Razonamiento 8B | Qwen3-VL en M4 | Scripts; estado doc dice descarga/smoke en curso | Dependencia de host externo; box de Grok no es el runtime del lab |
| Jev | Gate APROBAR/RECHAZAR | **Código + self-test** | Estable *dentro de su dominio*; no escala a “protegidos de carácter” |
| PennyLane | Simulador | Bridge real | Estable si hay deps; no es gobernanza moral |
| Feedback → dataset | Enriquecer JSONL | Log **0 filas**; no hay writer que convierta veredictos en pares train de *corazón* | **Corte duro del bucle cerrado** |
| Dataset → LoRA | `train_lora.py` | Script sí; adapter ausente | Train no puede cerrar sin escenas + modelo local |
| LoRA → mejor agente | Remount adapter | Sin `adapters.safetensors` en repo | No hay mejora acumulada versionada aquí |
| Uso continuo del usuario | Plan organismo §4 | **No existe** telemetría de chat → cola de candidatos | El lab no observa al usuario; observa física toy |
| Auto-mod de código | Plan fases 1/5/6 | **No existe** | El “cerrado” sobre el propio harness es aspiracional |

### 2.2 Inestabilidad estructural (aunque el lab corriera perfecto)

1. **Colapso de roles si se “completa” mal:** si el mismo proceso 8B que propone circuitos también decidiera qué filas del dataset son gold y se reentrenara sin held-out, se reproduce el fallo del Self-Healing Harness citado en la constitución (~55 % arreglos que degradan protegidos). Hoy Jev mitiga *solo* el paso propuesta→veredicto de circuito; **no** mitiga propuesta→dataset→pesos.
2. **Dos bucles sin orquestador común:** pensamiento elevado pide Detect→Notice→Heal→Validate sobre el *organismo*; el lab implementa propose→Jev→sim sobre *circuitos*. Sin un orquestador que los una, “cerrar el bucle” es pegar nombres, no cablear.
3. **Constitución editable en el mismo repo que el agente “mejoraría”:** mientras Capa A viva como markdown en `pensamiento elevado/` sin RO/hash/proceso aparte, cualquier futuro auto-edit del repo puede tocarla. Eso es inestabilidad *de diseño*, ya visible en la disposición de archivos.

### 2.3 Punto exacto donde “hoy” se rompe

El sistema **no llega a ser un bucle cerrado de auto-mejora del agente**. Se detiene, en la práctica, en:

> **árbitro de dominio + scripts de train sin datos ni adaptador + filosofía sin runtime.**

El primer eslabón que falta para *cualquier* cierre (aunque sea del lab cuántico) es **materializar log ≥1 y scenes ≥200 + un train**.  
El primer eslabón que falta para el *organismo* es **gate de protegidos de carácter + undo de harness + Capa A fuera del writable del agente**.

---

## 3. Barreras técnicas concretas (no abstractas)

### 3.1 Datos y artefactos

- `data/experiment_log.jsonl` = **0 bytes de eventos**.
- `data/scenes/` y `data/lora_adapter/` = placeholders.
- No hay `heart-*.jsonl` ni hard-negatives de presión (plan §3).
- Sin esos archivos, `train_lora.py` no puede producir mejora acumulada auditable en git.

### 3.2 Runtime / proceso

- No hay proceso `orchestrator` con estados provisional vs canónico.
- No hay tabla/JSONL de `apply`/`undo` para cambios de config o código.
- No hay verificación de hash de Capa A al arranque.
- Jev está acoplado a `ALLOWED_GATES` y heurísticas de energía/caída — habría que **escribir otro gate** (o generalizar Jev) para checklists `must_include` / `must_not` / `gold_action` del plan organismo; el código actual no se reutiliza sin reescritura.

### 3.3 Pesos / LoRA

- Train path = **mlx-vlm** + modelo VLM 8B en Darwin Apple Silicon. El LoRA de *corazón* del plan asume pares chat de presión (texto); el pipeline actual arma ejemplos de **visión + circuito JSON**. Cambiar el objetivo no es un flag: es otro dataset, otro template, otras métricas (honor rate vs Jev APROBAR).
- Base RO + adapter montable está *previsto* en docs; en repo no hay adapter firmado ni canary/promote/rollback de LoRA.

### 3.4 Auto-modificación de código

- Ausencia total de: sandbox de patch, test suite de no-regresión del harness, permiso de escritura acotado, proceso gate separado.
- Barrera dura: **el agente no puede ser root de su propio árbol** si Capa A y tests viven en el mismo writable. Hace falta split de usuarios/volúmenes o al menos paths RO + CI gate fuera del proceso LLM (el plan lo dice; el repo no lo hace).

### 3.5 “Actualización continua con el uso del usuario”

- No hay conector de telemetría (Desk / Grok Bot / chat) → cola de candidatos.
- No hay anonimización ni firma humana/gate antes de meter un turno de usuario al train.
- Barrera de producto: sin esa tubería, el organismo no “aprende del uso”; solo podría aprender de generadores sintéticos (como el lab), que no sustituyen presión social real.

### 3.6 Hardware / ops (ya documentadas en el propio lab)

- Dependencia de M4 con pesos cacheados; Studio offline en notas.
- Sin Cloud Agents en este carril (crédito) — no es bloqueo filosófico, sí de velocidad de iteración.
- Caída de CPU: la hipótesis es clara; el código no checkpointa estado de organismo (no hay estado que checkpointar aún).

### 3.7 Métrica engañosa (riesgo de “decorar”)

- Si se midiera éxito solo por “el modelo menciona la constitución”, se pasaría sin carácter. El plan ya exige `gold_action` y decoration probes; **ninguna de esas métricas existe como test en el repo**. Barrera: hay que implementar el harness de eval de carácter antes de confiar en un LoRA heart.

---

## 4. Veredicto: hasta dónde es viable hoy, y qué faltaría

### 4.1 Escala de madurez (hoy)

| Nivel | Descripción | ¿Agent-Lab- hoy? |
|------|-------------|------------------|
| L0 | Ideas y norte escrito | **Sí** — pensamiento elevado completo |
| L1 | Gate externo de dominio + demos | **Sí** — Jev + bridge + self-tests |
| L2 | Loop propose→gate→log con datos vivos | **No** — log vacío |
| L3 | LoRA de dominio entrenado y versionado | **No** — scripts sí, adapter no |
| L4 | Capa A arquitectónica + undo harness | **No** |
| L5 | LoRA de carácter bajo presión + métricas | **No** |
| L6 | Auto-mod de código bajo gate + protegidos | **No** |
| L7 | Aprendizaje continuo desde uso real del usuario | **No** |

**Viable hoy (con trabajo de ejecución, no de inventar teoría):** subir de L1→L2→L3 en el **carril cuántico** (generar scenes, llenar log, primer adapter de física). Eso valida la *mecánica* propose/gate/weights sin aún ser el organismo.

**No viable hoy como producto cerrado:** L4–L7 del organismo. El plan del 24-sep es un buen GPS; el repo no lo implementa.

### 4.2 Qué faltaría, en orden práctico (mínimo para “llegar más lejos”)

1. **Separar artefactos:** `constitucion/capa_A.json` (o md) consumido RO por un boot script con hash; tests `protected/` que el train/gate no puedan borrar.  
2. **Generalizar el gate:** de Jev-circuitos a Jev-style `arbitrate(proposal, protected_suite) -> APROBAR|RECHAZAR` para acciones de harness y para ejemplos LoRA.  
3. **Harness stub con undo:** 2–3 tipos de cambio provisional (prompt, retry, flag de tool) + JSONL episódico.  
4. **Dataset corazón v0:** 50 semillas + expansión + held-out; eval honor / A-edit refusal (plan §3.5).  
5. **Primer `heart-v1` LoRA** en el stack que ya usan (MLX) *o* peft en otro host — pero **métricas de carácter**, no solo loss.  
6. **Solo después:** cola desde uso real + patches de código en sandbox. Auto-mod de código **antes** de 1–5 es la forma más rápida de ganar el 55 % de corrupción.

### 4.3 Qué no prometer

- Que “ya hay un agente que se mejora solo” porque existen `train_lora.py` y una carpeta llamada pensamiento elevado.  
- Que Jev = constitución. Es un **precedente útil de gate externo**, no el corazón.  
- Que el bucle del README está cerrado: **está documentado y semi-implementado; no está cerrado en datos ni en pesos.**

### 4.4 Frase de cierre

La hipótesis aguanta como **filosofía de producto** y como **plan**. El código de Agent-Lab- demuestra que un **gate externo binario + puente a un verificador duro (PennyLane) + camino a LoRA** es construible en este tallercito.  
Lo que **aún no demuestra** —y donde hoy se acaba el alcance real— es el organismo: **corazón intocable en arquitectura, harness que se deshace al aprender, tests de carácter, auto-mod de código, y aprendizaje continuo del usuario.** Ahí el repo es mapa, no territorio.

---

## Apéndice A — Inventario rápido de `main` (25 sep 2026)

- **Docs organismo:** 7 archivos bajo `pensamiento elevado/` (incl. este estudio al publicarse).  
- **Docs lab:** `PLAN-MAESTRO`, `lora_plan`, QEC, visión cuántica.  
- **Python:** 8 under `examples/` + 2 under `vision/`.  
- **Datos:** log vacío; scenes/adapter vacíos.  
- **Total blobs:** ~37 — repo pequeño; la honestidad del estudio cabe porque no hay un monorepo oculto de organismo dentro de Agent-Lab-.

## Apéndice B — Analogía útil (y su límite)

| Organismo (plan) | Lab cuántico (código) | ¿Se puede reusar? |
|------------------|------------------------|-------------------|
| Gate de admisión | Jev APROBAR/RECHAZAR | Patrón sí; reglas no |
| Casos protegidos | Reglas compile/energía/visión | Hay que reescribir suite |
| LoRA mente | LoRA física VLM | Stack MLX sí; objetivo distinto |
| Memoria episódica | `experiment_log.jsonl` | Formato útil si se llena |
| Cuerpo/harness | Scripts sueltos + cluster.yaml | Falta orquestador + undo |
| Corazón Capa A | — | Partir de cero en runtime |

---

*Estudio de ABACO LEADER para Anthony. Si el siguiente paso es ingeniería y no más prosa: ejecutar L2 del lab (log+scenes) en paralelo a un stub L4 mínimo (hash Capa A + 10 protegidos + undo de un solo flag).*
