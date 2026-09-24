# Visión: física cuántica como inspiración para mejorar el LLM

Este documento explica, en lenguaje cotidiano, **por qué** mezclamos escenas físicas, un VLM Thinking y un simulador cuántico toy — y cómo eso prepara un fine-tune con LoRA.

No estamos afirmando que el LLM “sea” un computador cuántico. Usamos ideas de la física como **metáforas operativas** y como **banco de pruebas** donde el modelo debe proponer algo verificable.

## Tres ideas que sí usan

### 1. Superposición → razonamiento paralelo

En un circuito, un qubit puede estar en una mezcla de estados antes de medir. En el lab, el **8B Thinking** puede barajar varias hipótesis sobre una escena (¿caída libre? ¿rebote? ¿fricción?) antes de comprometerse con un JSON de puertas.

Beneficio humano: menos “una sola historia inventada”; más candidatas que Jev y el simulador pueden filtrar.

### 2. Interferencia → amplificar lo coherente

En física, caminos que se alinean se refuerzan y los que chocan se cancelan. Aquí, **Jev** y el **simulador** hacen de filtro: si el circuito no compila, si niega la pérdida de energía cuando la escena rebota, o si describe un objeto quieto cuando la pelota cae, la propuesta se **rechaza**.

Beneficio humano: el dataset de fine-tune se llena de pares (escena → circuito) que sobrevivieron un filtro duro, no de texto bonito sin verificación.

### 3. Entrelazamiento → dependencias lejanas

Dos qubits entrelazados correlacionan medidas aunque estén “lejos” en el circuito. En el loop del clúster, la **M4** (visión grande) y la **Studio** (verificador chico) se tratan como nodos acoplados por Tailscale: una propone, la otra rankea / critica, y el feedback vuelve.

Beneficio humano: especialización por máquina (128 GB vs 36 GB) sin mandar datos a la nube.

## El árbitro Jev (sí / no)

Jev responde solo **APROBAR** o **RECHAZAR** con una línea de motivo. Reglas iniciales:

1. ¿El circuito **compila** en PennyLane (o Qiskit)?
2. ¿Respeta la **pérdida de energía** de la escena (rebotes)?
3. ¿La **descripción visual** cuadra con la salida del simulador?

Si falla cualquiera → RECHAZAR. Jev **no** otorga permisos ni “grants” de sistema; solo califica propuestas del experimento.

## Plan de fine-tune con LoRA

1. Generar cientos de escenas con `synthetic_physics_dataset.py` (ejes: gravedad, restitución, ruido visual).
2. Correr el loop visión → 8B → Jev → simulador.
3. Guardar en `data/experiment_log.jsonl` solo (o sobreponderar) las filas **APROBAR**.
4. Entrenar **LoRA** sobre el 8B (MLX) para que proponga circuitos más a menudo compilables y coherentes con la física de la escena.
5. Cuando la Studio esté online, usar 2B/4B Thinking como ranker de pares antes del LoRA.

Estado: generador sintético listo en `quantum-llm-lab`; primer ciclo de 5 escenas con pesos reales en la M4 en curso; LoRA = siguiente fase tras tener log limpio.

## Qué no prometemos

- No es un algoritmo cuántico de verdad en hardware QPU.
- No sustituye física profesional ni certificación de seguridad de plugins.
- Es un **laboratorio** para aprender el loop y producir datos verificables.
