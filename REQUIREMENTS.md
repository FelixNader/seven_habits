# Requisitos y especificaciones de 7 Hábitos

Estado: **fase experimental inicial**  
Versión de la app: `0.0.1`  
Última revisión: 2026-09-28

Este documento distingue entre requisitos declarados por el código, requisitos
del entorno Frappe y supuestos que todavía deben validarse. La aplicación no
debe considerarse lista para producción hasta completar la matriz de
compatibilidad y las pruebas indicadas al final.

## 1. Qué es esta aplicación

`seven_habits` es una app para Frappe que modela un ciclo personal de:

```text
alineación → compromiso → planificación → captura de hechos
→ interpretación → revisión y aprendizaje
```

Su propósito es distinguir el tiempo planificado de la realidad observada y
conservar la trazabilidad de las correcciones. La app se organiza como un
monolito modular con estos contextos lógicos:

- Alignment: roles, misión, metas, proyectos y hábitos.
- Commitment: decisiones que la persona asume.
- Scheduling: tareas, eventos y asignaciones temporales.
- Activity Ledger: hechos observados y correcciones.
- Interpretation: clasificación y significado posterior.
- Review / Learning: reflexión y decisiones de ajuste.

## 2. Estado experimental

La aplicación está en una fase experimental inicial. Esto significa que:

- el modelo de dominio puede cambiar;
- no se garantiza compatibilidad hacia atrás entre migraciones tempranas;
- no se garantiza todavía la cobertura completa del flujo MVP;
- no se recomienda instalarla en producción sin respaldo y entorno de prueba;
- los nombres, campos y DocTypes pueden cambiar antes de una versión estable.

## 3. Requisitos declarados actualmente

Estos requisitos aparecen en los archivos de empaquetado de la app:

| Requisito | Declaración actual |
| --- | --- |
| Nombre de paquete | `seven_habits` |
| Versión | `0.0.1` |
| Python | `>=3.10` |
| Dependencia Python | `frappe` sin rango de versión |
| Licencia | MIT |
| Sistema de build | `setuptools>=61` |

La instalación recomendada se realiza con Bench (`bench get-app`), no con
`pip install` aislado. Bench debe resolver Frappe dentro del entorno del bench.

## 4. Plataforma objetivo

La especificación funcional se ha diseñado para:

- Frappe Framework v16.
- ERPNext v16 como entorno de referencia del bench.
- Python 3.10 o superior, sujeto a la versión de Frappe utilizada.
- Un sitio Frappe administrado por Bench.

La app no declara actualmente `required_apps = ["erpnext"]`. Por diseño, debe
funcionar como app de Frappe sin depender de DocTypes propios de ERPNext. Esta
afirmación debe verificarse con una instalación limpia de Frappe sin ERPNext.
Si alguna funcionalidad termina utilizando ERPNext, habrá que declarar esa
dependencia explícitamente.

## 5. Requisitos del entorno

El entorno que ejecuta la app debe proporcionar los servicios normales de un
bench Frappe compatible:

- Frappe instalado y operativo.
- Un sitio creado y accesible.
- Base de datos soportada por la versión de Frappe.
- Redis, workers y scheduler configurados cuando el bench los requiera.
- Node.js y herramientas de frontend si se compilan assets.
- Acceso de administración al sitio para instalar la app y ejecutar migraciones.

Las versiones exactas de MariaDB/PostgreSQL, Redis, Node.js y Yarn dependen de
la versión de Frappe y deben tomarse de la documentación de esa versión. No se
duplican aquí para evitar declarar una matriz no verificada.

## 6. Instalación experimental

Desde el directorio de un bench compatible:

```bash
bench get-app https://github.com/<usuario>/seven_habits.git
bench --site <sitio> install-app seven_habits
bench --site <sitio> migrate
bench build --app seven_habits
```

Después de instalar, validar el acceso al Desk y revisar los logs del sitio.
En desarrollo local, el sitio de referencia es `development.localhost`.

Para retirar la app de un sitio experimental:

```bash
bench --site <sitio> uninstall-app seven_habits
```

Hacer un backup antes de desinstalar. La desinstalación puede eliminar datos de
los DocTypes de la app.

## 7. Qué incluye el MVP funcional previsto

- Roles, misión, metas, proyectos y hábitos.
- Compromisos independientes del tiempo.
- Tareas y eventos como materializaciones de compromisos.
- Asignaciones de tiempo y agenda como proyección del plan.
- Captura rápida de hechos observados.
- Correcciones de hechos con trazabilidad.
- Interpretación posterior de los hechos.
- Revisión, reflexión y decisiones de ajuste.
- Vistas de agenda, timeline y comparación plan vs. realidad.

## 8. Qué queda fuera por ahora

- Compatibilidad garantizada con varias ramas de Frappe.
- Compatibilidad garantizada con varias ramas de ERPNext.
- Recurrencia avanzada.
- Integraciones externas de calendario, correo o IA.
- Automatización inteligente extensa.
- Multiempresa o flujos complejos de permisos.
- Un marketplace o instalador gráfico.
- Garantía de migraciones estables entre versiones `0.x`.

## 9. Seguridad y operación experimental

- Usar un entorno de desarrollo o staging.
- Hacer backup antes de instalar, migrar o desinstalar.
- No guardar secretos, contraseñas ni tokens en el repositorio.
- Revisar permisos de los DocTypes antes de exponer el sitio a usuarios reales.
- No asumir que una captura o una corrección es inmutable hasta validar las
  reglas de servidor correspondientes.
- Revisar logs después de cada migración.

## 10. Matriz de compatibilidad pendiente

Antes de declarar una versión estable, validar al menos:

| Combinación | Estado |
| --- | --- |
| Frappe v16 + Python soportado por v16 | Objetivo inicial |
| ERPNext v16 + Frappe v16 | Entorno de referencia |
| Frappe v15 | No validado |
| Frappe v17 | No validado |
| Frappe sin ERPNext | Pendiente de prueba explícita |
| Instalación limpia desde GitHub | Pendiente de prueba reproducible |

## 11. Validación mínima antes de publicar una versión estable

1. Instalar en un bench limpio.
2. Instalar en un sitio vacío y ejecutar migraciones.
3. Crear y consultar cada DocType del MVP.
4. Ejecutar el flujo compromiso → planificación → captura → revisión.
5. Verificar permisos de lectura, creación, edición y corrección.
6. Confirmar que no se requieren DocTypes de ERPNext si la app se anuncia como
   independiente.
7. Añadir pruebas automatizadas y documentar los comandos de test.
8. Repetir la instalación desde un tag/versionado, no solo desde `main`.

## 12. Declaración recomendada para GitHub

> **Experimental / pre-alpha.** 7 Hábitos es una aplicación Frappe en diseño y
> validación temprana. Está orientada inicialmente a Frappe/ERPNext v16 y Python
> 3.10+. Puede requerir ajustes de esquema o migración entre versiones 0.x.
> Úsala en desarrollo o staging, con backups, hasta que se publique una matriz
> de compatibilidad y una suite de pruebas estable.
