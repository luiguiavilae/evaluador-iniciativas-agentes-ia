"""
Módulo de preguntas por categorías para la evaluación de iniciativas de agentes.

Basado en:
- Anthropic: "Building Effective Agents" (2024)
- Google Cloud: Agent Evaluation Framework
- AWS: Agents vs Automation Strategic Guide
- Dataiku: How to Select High-Impact AI Agent Use Cases
- McKinsey: When can AI make good decisions
- Gartner: AI Business Value Framework

Pesos por categoría (deben sumar 1.0):
  1. Naturaleza del Problema       → 0.22
  2. Indicadores de Negocio (KPIs) → 0.23  ← nueva categoría
  3. Impacto Operacional           → 0.20
  4. Viabilidad Técnica            → 0.18
  5. Complejidad vs. Alternativas  → 0.12
  6. Madurez Organizacional        → 0.05
"""

CATEGORIAS = [
    {
        "id": "problema",
        "nombre": "🔍 Categoría 1: Naturaleza del Problema",
        "descripcion": "Evaluamos qué tan complejo y adecuado es el problema para un agente de IA.",
        "peso": 0.22,
        "preguntas": [
            {
                "id": "p1_1",
                "texto": "¿El problema requiere tomar múltiples decisiones encadenadas que dependen una de la otra?",
                "opciones": [
                    ("A", "Sí, son muchos pasos interdependientes y difíciles de predeterminar", 4),
                    ("B", "Sí, pero los pasos son conocidos y predecibles de antemano", 2),
                    ("C", "No, es una sola decisión o una secuencia fija de pasos", 0),
                ],
                "ayuda": "Ej. de SÍ: Investigar un tema y redactar un informe adaptando el enfoque según hallazgos. Ej. de NO: Generar un resumen de un texto fijo."
            },
            {
                "id": "p1_2",
                "texto": "¿El proceso trabaja con información no estructurada o de múltiples fuentes heterogéneas?",
                "opciones": [
                    ("A", "Sí, combina texto libre, documentos, APIs, bases de datos, etc.", 4),
                    ("B", "Principalmente estructurada, pero con algo de texto libre", 2),
                    ("C", "No, todo viene de fuentes estructuradas y uniformes (CSV, BD, formularios)", 0),
                ],
                "ayuda": "Ej. de SÍ: Analizar correos + CRM + reportes PDF. Ej. de NO: Procesar filas de una hoja de cálculo."
            },
            {
                "id": "p1_3",
                "texto": "¿El proceso requiere razonamiento contextual o juicio adaptativo según la situación?",
                "opciones": [
                    ("A", "Sí, cada caso puede ser diferente y requiere adaptación", 4),
                    ("B", "Parcialmente, hay reglas pero con excepciones frecuentes", 2),
                    ("C", "No, siempre aplica las mismas reglas de forma determinista", 0),
                ],
                "ayuda": "Ej. de SÍ: Atención al cliente con problemas únicos. Ej. de NO: Validar si un número de cédula tiene el formato correcto."
            },
            {
                "id": "p1_4",
                "texto": "¿Es difícil o imposible definir todos los pasos del proceso de antemano (flujo abierto)?",
                "opciones": [
                    ("A", "Sí, el número de pasos varía y no se puede predeterminar todo", 4),
                    ("B", "El flujo principal es conocido, pero hay variaciones menores", 2),
                    ("C", "No, el proceso es completamente documentable como un diagrama de flujo fijo", 0),
                ],
                "ayuda": "Si puedes diagramar el proceso completo en Visio con todos los caminos posibles, posiblemente no necesitas un agente."
            },
        ]
    },
    {
        "id": "kpis",
        "nombre": "📈 Categoría 2: Indicadores de Negocio (KPIs)",
        "descripcion": "Evaluamos si la iniciativa tiene KPIs claros que el agente pueda impactar de forma medible. Sin un indicador de negocio definido, es imposible justificar la inversión ni medir el éxito.",
        "peso": 0.23,
        "preguntas": [
            {
                "id": "p2_1",
                "texto": "¿Puedes identificar al menos un KPI de negocio concreto que el agente mejoraría?",
                "opciones": [
                    ("A", "Sí, tenemos KPIs definidos y medibles (ej: tasa de conversión, tiempo de ciclo, NPS, costo por transacción)", 4),
                    ("B", "Tenemos una noción del beneficio pero aún no está formalizado como KPI medible", 2),
                    ("C", "No, el beneficio es difuso o principalmente cualitativo ('mejorar la experiencia')", 0),
                ],
                "ayuda": "Ej. de KPIs válidos: reducir el tiempo de onboarding de 5 días a 1, aumentar resolución en primer contacto del 60% al 85%, reducir costo de procesamiento de $12 a $3 por ticket."
            },
            {
                "id": "p2_2",
                "texto": "¿A qué tipo de indicador de negocio impacta principalmente esta iniciativa?",
                "opciones": [
                    ("A", "Ingresos o crecimiento (conversión, retención, upsell, nuevos clientes)", 4),
                    ("B", "Eficiencia operacional (reducción de costos, tiempo de proceso, errores)", 3),
                    ("C", "Experiencia del cliente o empleado (NPS, satisfacción, tiempo de respuesta)", 3),
                    ("D", "Cumplimiento o riesgo (reducción de incidentes, auditorías, penalizaciones)", 2),
                ],
                "ayuda": "Los agentes que impactan ingresos o eficiencia operacional directa tienen ROI más claro y aprobación más fácil. Impactos en experiencia o riesgo son igualmente válidos pero requieren más esfuerzo de medición."
            },
            {
                "id": "p2_3",
                "texto": "¿Sabes cuánto vale en términos económicos mejorar ese indicador?",
                "opciones": [
                    ("A", "Sí, tenemos una estimación de valor (ahorro en $ o % de mejora proyectada)", 4),
                    ("B", "Sabemos que es significativo pero no tenemos el número exacto", 2),
                    ("C", "No hemos calculado el valor económico del impacto", 0),
                ],
                "ayuda": "Ej: 'Automatizar este proceso ahorraría 3 horas/día × $25/hora × 250 días = $18.750 anuales'. Sin este cálculo es difícil priorizar el agente sobre otras iniciativas."
            },
            {
                "id": "p2_4",
                "texto": "¿En cuánto tiempo esperarías ver el impacto en esos indicadores?",
                "opciones": [
                    ("A", "En semanas desde el despliegue (impacto inmediato y medible)", 4),
                    ("B", "En 1 a 3 meses (impacto a corto plazo)", 3),
                    ("C", "En 3 a 12 meses (impacto a mediano plazo)", 2),
                    ("D", "No está claro cuándo o cómo se vería el impacto", 0),
                ],
                "ayuda": "Iniciativas con impacto incierto o muy lejano en el tiempo tienen mayor riesgo de ser canceladas antes de demostrar valor."
            },
        ]
    },
    {
        "id": "impacto",
        "nombre": "💼 Categoría 3: Impacto Operacional",
        "descripcion": "Medimos el valor operativo real que generaría el agente en el día a día del equipo.",
        "peso": 0.20,
        "preguntas": [
            {
                "id": "p3_1",
                "texto": "¿Con qué frecuencia ocurre este proceso o necesidad en tu equipo?",
                "opciones": [
                    ("A", "Muchas veces al día o de forma continua", 4),
                    ("B", "Varias veces a la semana", 3),
                    ("C", "Una o pocas veces al mes", 1),
                    ("D", "Raramente (pocas veces al año o de forma esporádica)", 0),
                ],
                "ayuda": "Un agente para procesos muy infrecuentes raramente justifica la inversión en construcción y mantenimiento."
            },
            {
                "id": "p3_2",
                "texto": "¿Cuánto tiempo humano consume actualmente este proceso por ocurrencia?",
                "opciones": [
                    ("A", "Más de 2 horas por ocurrencia", 4),
                    ("B", "Entre 30 minutos y 2 horas", 3),
                    ("C", "Entre 5 y 30 minutos", 1),
                    ("D", "Menos de 5 minutos", 0),
                ],
                "ayuda": "El ahorro potencial debe justificar el costo de construcción, pruebas y mantenimiento del agente."
            },
            {
                "id": "p3_3",
                "texto": "¿Cuál es el impacto de un error en este proceso?",
                "opciones": [
                    ("A", "Bajo: errores son fáciles de detectar y corregir sin consecuencias graves", 4),
                    ("B", "Medio: errores tienen consecuencias moderadas pero recuperables", 3),
                    ("C", "Alto: un error tiene consecuencias graves (financieras, legales, seguridad)", 0),
                ],
                "ayuda": "IMPORTANTE: Alta tolerancia al error favorece el agente. En procesos críticos (médicos, financieros, legales) se requiere supervisión humana constante."
            },
            {
                "id": "p3_4",
                "texto": "¿Cuántas personas en tu organización se beneficiarían del agente?",
                "opciones": [
                    ("A", "Toda la empresa o un departamento grande (+50 personas)", 4),
                    ("B", "Un equipo mediano (10-50 personas)", 3),
                    ("C", "Un equipo pequeño (2-10 personas)", 2),
                    ("D", "Solo yo o una persona", 0),
                ],
                "ayuda": "El alcance del impacto es clave para justificar la inversión."
            },
        ]
    },
    {
        "id": "viabilidad_tecnica",
        "nombre": "⚙️ Categoría 4: Viabilidad Técnica",
        "descripcion": "Evaluamos si existen las condiciones técnicas para construir y operar el agente.",
        "peso": 0.18,
        "preguntas": [
            {
                "id": "p4_1",
                "texto": "¿Los datos necesarios para que el agente trabaje están disponibles y accesibles?",
                "opciones": [
                    ("A", "Sí, los datos están digitalizados, organizados y accesibles", 4),
                    ("B", "Parcialmente, algunos datos requieren limpieza o digitalización", 2),
                    ("C", "No, los datos son principalmente manuales, en papel o muy dispersos", 0),
                ],
                "ayuda": "Sin datos de calidad y accesibles, cualquier sistema de IA fracasará independientemente de su sofisticación."
            },
            {
                "id": "p4_2",
                "texto": "¿El equipo tiene o puede adquirir las capacidades técnicas para construir y mantener el agente?",
                "opciones": [
                    ("A", "Sí, tenemos desarrolladores con experiencia o acceso a ellos", 4),
                    ("B", "Tenemos capacidades básicas pero necesitaríamos apoyo externo puntual", 2),
                    ("C", "No, no tenemos capacidades técnicas y dependería completamente de terceros", 0),
                ],
                "ayuda": "Un agente sin equipo técnico para mantenerlo se convierte en deuda tecnológica."
            },
            {
                "id": "p4_3",
                "texto": "¿El proceso puede integrarse con sistemas existentes (APIs, bases de datos, herramientas)?",
                "opciones": [
                    ("A", "Sí, los sistemas existentes tienen APIs o integraciones disponibles", 4),
                    ("B", "Parcialmente, algunas integraciones existen pero otras requieren desarrollo", 2),
                    ("C", "No, los sistemas son cerrados, heredados o sin posibilidad de integración", 0),
                ],
                "ayuda": "Un agente sin conectividad con los sistemas donde viven los datos no puede operar efectivamente."
            },
        ]
    },
    {
        "id": "complejidad_alternativas",
        "nombre": "🔄 Categoría 5: Complejidad vs. Alternativas",
        "descripcion": "Determinamos si el agente es la solución más adecuada o si existe algo más simple y efectivo.",
        "peso": 0.12,
        "preguntas": [
            {
                "id": "p5_1",
                "texto": "¿Ya intentaron resolver este problema con automatizaciones simples (macros, scripts, RPA, workflows)?",
                "opciones": [
                    ("A", "Sí, lo intentamos y quedaron casos no resueltos que requieren más inteligencia", 4),
                    ("B", "No lo hemos intentado aún con automatización simple", 1),
                    ("C", "Sí, funcionó parcialmente pero decidimos no optimizarlo", 0),
                ],
                "ayuda": "Anthropic recomienda: 'Empieza simple. Solo añade complejidad cuando sea necesario.'"
            },
            {
                "id": "p5_2",
                "texto": "¿El proceso requiere interacción de múltiples turnos o conversación contextual con el usuario?",
                "opciones": [
                    ("A", "Sí, necesita mantener contexto a lo largo de una conversación o sesión", 4),
                    ("B", "Ocasionalmente requiere clarificaciones, pero es principalmente de una vía", 2),
                    ("C", "No, es un proceso de entrada-salida única (input → output)", 0),
                ],
                "ayuda": "Procesos de entrada-salida única raramente necesitan un agente completo."
            },
            {
                "id": "p5_3",
                "texto": "¿La solución necesita adaptarse en tiempo real a información nueva o cambiante?",
                "opciones": [
                    ("A", "Sí, debe responder a cambios inesperados durante la ejecución", 4),
                    ("B", "Los cambios son predecibles y podrían manejarse con reglas if-else", 2),
                    ("C", "No, el proceso siempre sigue el mismo camino independientemente del contexto", 0),
                ],
                "ayuda": "Si todos los caminos posibles se pueden anticipar, un árbol de decisión o workflow es suficiente."
            },
        ]
    },
    {
        "id": "organizacion",
        "nombre": "🏢 Categoría 6: Madurez y Cultura Organizacional",
        "descripcion": "Evaluamos si la organización está lista para adoptar y confiar en un agente de IA.",
        "peso": 0.05,
        "preguntas": [
            {
                "id": "p6_1",
                "texto": "¿La organización tiene experiencia previa con herramientas de automatización o IA?",
                "opciones": [
                    ("A", "Sí, usamos herramientas de automatización/IA activamente", 4),
                    ("B", "Tenemos experiencias puntuales o estamos comenzando", 2),
                    ("C", "No, es nuestra primera iniciativa de este tipo", 0),
                ],
                "ayuda": "Organizaciones sin experiencia previa en automatización suelen tener dificultades de adopción y mantenimiento."
            },
            {
                "id": "p6_2",
                "texto": "¿Los usuarios finales del proceso están dispuestos a trabajar con o supervisar un agente de IA?",
                "opciones": [
                    ("A", "Sí, hay entusiasmo y disposición por parte del equipo", 4),
                    ("B", "Hay resistencia moderada pero manejable con capacitación", 2),
                    ("C", "Hay resistencia alta o el proceso involucra clientes externos que no aceptarían un agente", 0),
                ],
                "ayuda": "El factor humano es crítico: un agente sin adopción es un proyecto fallido."
            },
        ]
    },
]

def obtener_total_preguntas():
    """Retorna el número total de preguntas en todas las categorías."""
    return sum(len(cat["preguntas"]) for cat in CATEGORIAS)

def obtener_puntaje_maximo_categoria(categoria):
    """Retorna el puntaje máximo posible para una categoría."""
    return sum(max(op[2] for op in p["opciones"]) for p in categoria["preguntas"])
