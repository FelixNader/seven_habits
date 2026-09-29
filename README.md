# 7 Hábitos

Aplicación Frappe para convertir propósito en acción y aprender de la diferencia entre lo que se planificó y lo que realmente ocurrió.

> La agenda es una hipótesis; la bitácora es evidencia.

## ¿Por qué existe esta app?

Las herramientas tradicionales de productividad suelen mezclar en una misma lista el propósito, las tareas, el calendario, los resultados y las interpretaciones posteriores. Eso hace difícil responder:

- ¿Qué estoy intentando cuidar o conseguir?
- ¿Qué he decidido atender?
- ¿Qué tiempo reservé para ello?
- ¿Qué ocurrió realmente?
- ¿Qué aprendí y qué debo ajustar?

7 Hábitos propone un sistema personal que conecta esas preguntas sin confundir sus significados. No intenta completar toda la filosofía de *Los 7 hábitos de la gente altamente efectiva* en una pantalla; construye un núcleo pequeño, extensible y verificable para alinear propósito, compromisos, tiempo y aprendizaje.

## Idea central

```text
Propósito y dirección
        ↓
Compromisos que decido atender
        ↓
Tiempo que planifico
        ↓
Hechos que registro
        ↓
Interpretación y revisión
        ↓
Nuevas decisiones
```

La diferencia entre el plan y la realidad no es un error que haya que ocultar: es información valiosa para decidir mejor.

## Principios de diseño

1. **La agenda es una hipótesis.** Programar algo no demuestra que haya ocurrido.
2. **La bitácora es evidencia.** Registra hechos observados, no intenciones.
3. **Capturar precede a clasificar.** Registrar un hecho debe requerir pocos campos; la clasificación puede hacerse después.
4. **La historia es trazable.** Una corrección conserva el hecho original y su motivo; no se reescribe silenciosamente.
5. **Un compromiso no tiene tiempo propio.** El compromiso expresa una decisión; la asignación temporal pertenece a Scheduling.
6. **Tarea y evento son formas de materializar un compromiso.** Una tarea administra trabajo; un evento representa un intervalo fijado por acuerdos o restricciones externas.
7. **Roles, metas/proyectos y hábitos son dimensiones ortogonales.** Orientan un compromiso, pero no forman una jerarquía obligatoria.
8. **La prioridad no es el propósito.** Eisenhower ayuda a priorizar; roles, metas y hábitos aportan dirección y sentido.

## Arquitectura

La app se implementa como un monolito modular dentro de Frappe. Los contextos están separados lógicamente, sin introducir microservicios ni integraciones distribuidas innecesarias para el MVP.

```text
seven_habits/
├── alignment/        # Roles, misión, metas, proyectos y hábitos
├── commitment/       # Decisiones que el usuario asume
├── scheduling/       # Tareas, eventos y asignaciones de tiempo
├── ledger/           # Hechos observados y correcciones trazables
├── interpretation/   # Significado y clasificación posterior
└── review/           # Reflexión, aprendizaje y ajustes
```

### Contextos delimitados

| Contexto | Pregunta de dominio | Responsabilidad |
| --- | --- | --- |
| Alignment | ¿Qué importa y hacia dónde quiero dirigir mi vida? | Roles, misión, metas, proyectos y hábitos. |
| Commitment | ¿De qué he decidido hacerme cargo? | Compromisos y sus estados. |
| Scheduling | ¿Cuándo y cómo se asigna tiempo? | Tareas, eventos y bloques planificados. |
| Activity Ledger | ¿Qué ocurrió realmente? | Hechos y correcciones trazables. |
| Interpretation | ¿Qué significa lo observado? | Clasificación y relaciones posteriores. |
| Review / Learning | ¿Qué aprendí y qué cambio? | Reflexión y decisiones de ajuste. |

## Flujo MVP de extremo a extremo

```text
Dimensiones de enfoque
        ↓ orientan
Compromiso
        ↓ se materializa como
Task / Event
        ↓ recibe
Asignación temporal → Agenda (planificado)
        ↓ se contrasta con
Activity Fact → Bitácora (realidad)
        ↓ se analiza mediante
Interpretation
        ↓ cierra el ciclo con
Review / Adjustment Decision
```

| Plan | Realidad |
| --- | --- |
| Tiempo reservado o esperado | Hechos observados |
| Puede tener varias asignaciones para una tarea | Puede diferir del plan |
| No prueba ejecución | Conserva trazabilidad |

## Decisiones arquitectónicas relevantes

### De jerarquía a dimensiones

Una actividad puede pertenecer al mismo tiempo a un rol profesional, un proyecto y un hábito. Por eso no existe un único “padre”: son dimensiones de enfoque que orientan, no contenedores jerárquicos.

### De actividad a compromiso

“Actividad” era demasiado específico como centro del modelo. **Compromiso** representa cualquier cosa que la persona decide atender: preparar una propuesta, asistir a una reunión, llamar a un cliente o reservar tiempo para estudiar.

### De agenda como lista a agenda como plan

La agenda no es la fuente de la verdad. Es una proyección del tiempo planificado. Una tarea puede recibir varios bloques sin dejar de ser la misma tarea.

### De captura enriquecida a captura rápida

La captura inicial debe funcionar incluso con datos incompletos:

```text
09:10 ERP
11:32 ERP fin
```

La clasificación, el vínculo con compromisos y la interpretación se completan después, cuando hay tiempo y contexto.

## Relación con Los 7 Hábitos

- **Ser proactivo:** registrar hechos y decisiones propias.
- **Comenzar con un fin en mente:** usar misión, roles, metas y hábitos como dirección.
- **Poner primero lo primero:** separar importancia/urgencia del propósito y hacer visible el tiempo real.
- **Pensar Ganar/Ganar:** conservar compromisos y acuerdos explícitos.
- **Primero entender, luego ser entendido:** distinguir hechos de interpretaciones.
- **Sinergizar:** relacionar varias dimensiones con un compromiso sin jerarquía artificial.
- **Afilar la sierra:** cerrar el ciclo con reflexión, revisión y ajustes.

## Alcance del MVP

- modelos de alineación, compromisos, tareas y eventos;
- agenda como proyección del tiempo planificado;
- captura rápida de hechos;
- correcciones con trazabilidad;
- interpretación posterior;
- revisión mínima y decisiones de ajuste;
- vistas de agenda, línea de tiempo y comparación plan vs. realidad.

Quedan fuera del MVP inicial la recurrencia avanzada, la automatización inteligente extensa, las integraciones distribuidas y la cobertura completa de todos los rituales de los 7 Hábitos.

## Estado del proyecto

**Experimental / pre-alpha.** La app está en fase inicial de construcción sobre
Frappe/ERPNext v16. Este repositorio contiene el modelo y los DocTypes del
núcleo; la implementación se valida por contextos y por el flujo completo, no
por cantidad de pantallas. No se recomienda instalarla en producción todavía.

## Desarrollo local

La app vive dentro de un bench Frappe. Desde el directorio del bench:

```bash
bench --site development.localhost install-app seven_habits
bench --site development.localhost migrate
```

Para iniciar el entorno local desde el proyecto contenedor, consulta las instrucciones de desarrollo del bench y verifica que el sitio esté disponible en `http://development.localhost:8000`.

Los requisitos declarados, la compatibilidad conocida, el procedimiento de instalación experimental y las validaciones pendientes están documentados en [REQUIREMENTS.md](REQUIREMENTS.md).

## Documentación de diseño

El razonamiento completo está documentado en dos piezas complementarias:

- **Especificación MVP:** modelos, invariantes, API mínima, tests y orden de implementación.
- **Proceso arquitectónico:** evolución del modelo, hipótesis descartadas y principios derivados.

El README resume esas decisiones para quien llega al repositorio; los documentos de diseño conservan el detalle y el contexto de cada decisión.
