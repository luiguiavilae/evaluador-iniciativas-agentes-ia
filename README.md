# 🤖 Evaluador de Iniciativas de Agentes de IA

> **¿Tu iniciativa realmente necesita un agente de IA?**
> Descúbrelo con un cuestionario de 16 preguntas en 5 categorías, sustentado en frameworks de Anthropic, Google Cloud, AWS y McKinsey.

---

## ¿Para qué sirve?

Muchos equipos de empresa invierten tiempo, esfuerzo y recursos construyendo agentes de IA para problemas que podrían resolverse con automatizaciones simples, scripts o workflows. Este evaluador te ayuda a tomar una decisión informada **antes** de comprometer recursos.

El agente evaluador:
- Guía al usuario a través de **5 categorías de evaluación** con **16 preguntas**
- Calcula un **puntaje ponderado** basado en evidencia de la industria
- Entrega un **veredicto claro**: construir / evaluar alternativas / no construir
- Ofrece **alternativas concretas** si el agente no es la solución adecuada
- Genera un **reporte exportable** en Markdown (y PDF opcional)
- Guarda un **historial** de todas las evaluaciones realizadas

---

## Categorías de Evaluación

| # | Categoría | Peso | Qué evalúa |
|---|-----------|------|------------|
| 1 | 🔍 Naturaleza del Problema | 25% | Complejidad, no-linealidad, razonamiento requerido |
| 2 | 💼 Impacto en el Negocio | 25% | Frecuencia, tiempo ahorrado, tolerancia al error, alcance |
| 3 | ⚙️ Viabilidad Técnica | 20% | Datos disponibles, capacidad técnica, integraciones |
| 4 | 🔄 Complejidad vs. Alternativas | 20% | Necesidad de contexto, adaptabilidad, intentos previos |
| 5 | 🏢 Madurez Organizacional | 10% | Experiencia previa en IA, adopción del equipo |

---

## Umbrales de Decisión

```
 0% ─────────────── 45% ─────────────── 70% ────── 100%
 │                   │                   │
 └── 🔴 NO AGENTE    └── 🟡 ZONA GRIS   └── 🟢 SÍ AGENTE
```

- **≥ 70%**: Se recomienda construir el agente
- **45% – 69%**: Zona gris: explorar alternativas híbridas primero
- **< 45%**: No se recomienda el agente; se proponen alternativas

---

## Instalación y Uso

### Requisitos
- Python 3.8+
- Sin dependencias externas para la funcionalidad core

### Instalación

```bash
# Clonar o descargar el proyecto
cd Evaluador_de_agentes

# (Opcional) Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

# No requiere pip install para funcionalidad básica
# Para exportar PDF (opcional):
# pip install weasyprint markdown
```

### Ejecutar una evaluación

```bash
python main.py
```

### Ver historial de evaluaciones

```bash
python main.py --historial
```

---

## Estructura del Proyecto

```
Evaluador_de_agentes/
│
├── main.py                        # CLI principal – punto de entrada
│
├── core/
│   ├── __init__.py
│   ├── preguntas.py               # 16 preguntas organizadas en 5 categorías
│   └── evaluador.py               # Motor de scoring + generación de veredicto
│
├── utils/
│   ├── __init__.py
│   ├── reporte.py                 # Generador de reportes Markdown y PDF
│   └── persistencia.py            # Historial JSON + resumen CSV
│
├── data/
│   ├── historial_evaluaciones.json  # Historial completo (auto-generado)
│   └── resumen_evaluaciones.csv     # Resumen tabular (auto-generado)
│
├── reports/                       # Reportes generados (auto-creado)
│
├── requirements.txt
└── README.md
```

---

## Alternativas que propone el evaluador

Cuando la iniciativa **no amerita un agente**, el evaluador sugiere:

| Alternativa | Cuándo usarla |
|-------------|---------------|
| Script / Función Python | Proceso repetitivo, pasos fijos, datos estructurados |
| Workflow (n8n, Make, Zapier) | Múltiples pasos predecibles, sin IA necesaria |
| RPA (UiPath, Power Automate) | Automatizar interfaces gráficas sin API |
| LLM directo (sin agente) | Procesamiento de texto en un solo paso entrada-salida |
| Prompt Chaining | Varias transformaciones de texto con pasos definidos |
| Dashboard / BI | El objetivo es visualizar o analizar datos |
| Capacitación / Documentación | El problema es de conocimiento, no de tecnología |

---

## Marcos de Referencia

- [Anthropic: Building Effective Agents (2024)](https://www.anthropic.com/research/building-effective-agents)
- [Google Cloud: A Methodical Approach to Agent Evaluation](https://cloud.google.com/blog/topics/developers-practitioners/a-methodical-approach-to-agent-evaluation)
- [AWS: Agents vs Automation - A Strategic Guide](https://aws.amazon.com/executive-insights/content/agents-vs-automation-a-strategic-guide-for-business-leaders/)
- [Dataiku: How to Select High-Impact AI Agent Use Cases](https://www.dataiku.com/stories/blog/how-to-select-high-impact-ai-agent-use-cases)
- [McKinsey: Rethinking Decision Making to Unlock AI Potential](https://www.mckinsey.com/capabilities/operations/our-insights/when-can-ai-make-good-decisions-the-rise-of-ai-corporate-citizens)

---

*Evaluador de Iniciativas de Agentes de IA v1.0 · Lógica determinista · Sin costo de APIs · 100% Python estándar*
