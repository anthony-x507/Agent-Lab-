# Constitución LLM viva — inspiración profunda de Anthony (2026-09-24)

Fuente: ideas de Anthony + reflexión de otra IA. Guardar como norte de diseño Abaco / Leader. No borrar.

## Principio fundamental
El sistema que aprende **no** es el mismo que decide qué aprendizaje persiste.
Separación de poderes: (1) propone, (2) ejecuta provisional, (3) gate externo decide persistencia.
Auto-autorización = lo que la constitución debe impedir.
Evidencia citada: Self-Healing Harness (arXiv:2609.24130) — de 383 propuestas rechazadas, 55% mejoraban el fallo pero degradaban un caso protegido.

## Constitución de dos niveles
- **Capa A — Núcleo inmutable** (architectural, no solo prompt): escotilla humana, reversibilidad de toda modificación, auditabilidad. El sistema no puede desactivarlas.
- **Capa B — Principios operativos evolutivos** (COCOA-style): se revisan con desempeño; B no puede modificar A.

## Dos escalas de tiempo (PACE)
- Rápida: prompts / instrucciones (bajo riesgo, satura pronto).
- Lenta: lógica de control (parsers, validadores, reintentos) solo tras estancamiento de prompts + held-out validation.

## Bucle dual (SIA)
- Rápido: harness (edición reversible, replay).
- Lento: pesos / adaptadores ortogonales (intuición de dominio sin olvidar base).
Harness = agéntico; pesos = intuición que ningún prompt instila.

## Siete componentes
1. Sustrato congelado (base model RO)
2. Runtime reversible (toda mod tiene inversa; gate rechaza → revert)
3. Auto-modelado explícito (estado harness, fallos, reglas activas)
4. Gate de admisión (replay protegidos; delta + en fallo y no − en protegido)
5. Constitución A+B
6. Bucle dual harness + pesos
7. Orquestación por especificaciones (misma partitura, roles distintos)

## Cómo aprende (niño / Detect→Notice→Heal→Validate)
Observa fallo → propone → ejecuta provisional → valida protegidos → persiste o revierte.
Conciencia = auto-modelado funcional reportable, no misterio.

## Frase fundacional
Es un runtime que se deshace a sí mismo cada vez que aprende, y en ese deshacerse, se conserva.
Acción propone/ejecuta · Gobernanza (gate+constitución) arbitra · Memoria (adaptadores + episódica) conserva sin olvidar.
Puede aprender y aventurarse; no puede desactivar escotillas. Puede evolucionar B; no tocar A. Puede proponer; no autorizar.
