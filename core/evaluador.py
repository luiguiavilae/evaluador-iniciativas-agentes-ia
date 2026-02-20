"""
Motor de evaluación determinista para iniciativas de agentes de IA.

Implementa un sistema de scoring ponderado por categorías con umbrales de decisión
basados en los frameworks de Anthropic, Google Cloud, AWS y McKinsey.
"""

from .preguntas import CATEGORIAS, obtener_puntaje_maximo_categoria


# ─── Umbrales de decisión ──────────────────────────────────────────────────────
UMBRAL_AGENTE_CLARO = 70          # >= 70%  → Construir agente
UMBRAL_EVALUAR_ALTERNATIVAS = 45  # 45-69% → Explorar alternativas híbridas
# < 45%  → No construir agente (solución alternativa)

# ─── Alternativas según categorías débiles ────────────────────────────────────
ALTERNATIVAS = {
    "proceso_simple": {
        "nombre": "Script / Función Python o automatización simple",
        "descripcion": "Para procesos con pasos fijos y datos estructurados, un script bien escrito es más confiable, predecible y barato de mantener que un agente.",
        "cuando": "El proceso es repetitivo, tiene pasos conocidos y datos estructurados.",
        "herramientas": ["Python scripts", "Bash scripts", "Scheduled tasks (cron)", "Google Apps Script"]
    },
    "workflow": {
        "nombre": "Workflow / Orquestador de automatización",
        "descripcion": "Herramientas de workflow permiten encadenar pasos con lógica condicional sin necesidad de IA generativa.",
        "cuando": "El proceso tiene múltiples pasos pero el flujo es predecible y documentable.",
        "herramientas": ["n8n", "Make (Integromat)", "Zapier", "Apache Airflow", "Prefect", "Microsoft Power Automate"]
    },
    "rpa": {
        "nombre": "RPA (Automatización Robótica de Procesos)",
        "descripcion": "RPA replica acciones humanas en interfaces gráficas sin necesidad de APIs. Ideal para procesos legacy.",
        "cuando": "Necesitas automatizar interacciones con software que no tiene API.",
        "herramientas": ["UiPath", "Automation Anywhere", "Blue Prism", "Power Automate Desktop"]
    },
    "llm_simple": {
        "nombre": "Llamada directa a LLM (sin agente)",
        "descripcion": "Una sola llamada a un modelo de lenguaje con un prompt bien diseñado puede resolver el 80% de los casos sin necesidad de arquitectura de agente.",
        "cuando": "El problema requiere procesamiento de lenguaje natural pero en un solo paso de entrada-salida.",
        "herramientas": ["Prompt engineering avanzado", "Groq API (gratuito)", "Google Gemini API (gratuito)", "Ollama (local)"]
    },
    "prompt_chaining": {
        "nombre": "Prompt Chaining / Pipeline de LLM",
        "descripcion": "Encadenar múltiples llamadas a LLM con salidas predefinidas entre pasos. Más predecible que un agente y sin la sobrecarga de gestionar herramientas autónomas.",
        "cuando": "El proceso requiere varias transformaciones de texto/información con pasos definidos.",
        "herramientas": ["Python + LangChain básico", "Flujos secuenciales con cualquier LLM API gratuita"]
    },
    "dashboard_bi": {
        "nombre": "Dashboard / Herramienta de Business Intelligence",
        "descripcion": "Si la necesidad es visibilizar datos o generar reportes, un dashboard interactivo es más robusto, transparente y auditable que un agente.",
        "cuando": "El objetivo final es analizar o visualizar datos, no tomar acciones autónomas.",
        "herramientas": ["Metabase (gratuito)", "Apache Superset (gratuito)", "Google Looker Studio (gratuito)", "Power BI"]
    },
    "capacitacion": {
        "nombre": "Capacitación y documentación del proceso",
        "descripcion": "A veces el problema no es tecnológico sino de conocimiento. Una buena base de conocimiento o guía step-by-step puede ser más efectiva.",
        "cuando": "El problema se origina en falta de conocimiento o inconsistencia en cómo se ejecuta el proceso.",
        "herramientas": ["Notion", "Confluence", "Loom (videos de proceso)", "SOPs documentados"]
    },
    "definir_kpis": {
        "nombre": "Definición de KPIs y caso de negocio primero",
        "descripcion": "Antes de construir cualquier solución tecnológica, el equipo debe definir qué indicadores medirá, cuál es la línea base actual y cuánto vale mejorarlos. Sin esto, cualquier iniciativa (agente o no) carece de criterio de éxito.",
        "cuando": "No están claros los indicadores de negocio que la iniciativa debe mover.",
        "herramientas": ["Business Case Canvas", "OKRs", "DACI framework", "Hoja de cálculo de ROI simple"]
    },
}


def calcular_puntaje(respuestas: dict) -> dict:
    """
    Calcula el puntaje total y por categoría basado en las respuestas del usuario.

    Args:
        respuestas: dict con {pregunta_id: (letra_opcion, puntaje)}

    Returns:
        dict con resultados detallados por categoría y puntaje global
    """
    resultados_categorias = []
    puntaje_global_ponderado = 0.0

    for categoria in CATEGORIAS:
        puntaje_obtenido = 0
        puntaje_maximo = obtener_puntaje_maximo_categoria(categoria)
        detalles_preguntas = []

        for pregunta in categoria["preguntas"]:
            pid = pregunta["id"]
            if pid in respuestas:
                letra, puntaje = respuestas[pid]
                puntaje_obtenido += puntaje
                # Encontrar texto de opción elegida
                texto_opcion = next(
                    (op[1] for op in pregunta["opciones"] if op[0] == letra), ""
                )
                detalles_preguntas.append({
                    "pregunta": pregunta["texto"],
                    "respuesta": letra,
                    "texto_respuesta": texto_opcion,
                    "puntaje": puntaje,
                    "puntaje_maximo": max(op[2] for op in pregunta["opciones"])
                })

        porcentaje_cat = (puntaje_obtenido / puntaje_maximo * 100) if puntaje_maximo > 0 else 0
        puntaje_global_ponderado += porcentaje_cat * categoria["peso"]

        resultados_categorias.append({
            "id": categoria["id"],
            "nombre": categoria["nombre"],
            "puntaje_obtenido": puntaje_obtenido,
            "puntaje_maximo": puntaje_maximo,
            "porcentaje": round(porcentaje_cat, 1),
            "peso": categoria["peso"],
            "preguntas": detalles_preguntas
        })

    return {
        "puntaje_global": round(puntaje_global_ponderado, 1),
        "categorias": resultados_categorias
    }


def generar_veredicto(puntaje_global: float, resultados_categorias: list) -> dict:
    """
    Genera el veredicto final, sustento y recomendaciones según el puntaje.

    Returns:
        dict con veredicto, nivel, sustento, alertas y alternativas recomendadas
    """
    # ── Identificar categorías débiles ────────────────────────────────────────
    cats_debiles = [c for c in resultados_categorias if c["porcentaje"] < 40]
    cats_nombre_debiles = [c["nombre"] for c in cats_debiles]

    # ── Señales de alerta específicas ─────────────────────────────────────────
    alertas = _detectar_alertas(resultados_categorias)

    # ── Veredicto por umbral ───────────────────────────────────────────────────
    if puntaje_global >= UMBRAL_AGENTE_CLARO:
        veredicto = _veredicto_si(puntaje_global, alertas)
    elif puntaje_global >= UMBRAL_EVALUAR_ALTERNATIVAS:
        veredicto = _veredicto_hibrido(puntaje_global, cats_debiles, alertas)
    else:
        veredicto = _veredicto_no(puntaje_global, cats_debiles, alertas)

    return veredicto


def _detectar_alertas(resultados_categorias: list) -> list:
    """Detecta señales de alerta específicas basadas en respuestas críticas."""
    alertas = []

    # Mapa: {pregunta_id: {respuesta: mensaje_alerta}}
    ALERTAS_MAPA = {
        "p2_1": {  # KPI definido
            "C": "⚠️  ALERTA DE ESTRATEGIA: No hay un KPI concreto que el agente deba impactar. Sin un indicador de éxito definido, no podrás medir el retorno ni justificar la inversión. Define primero qué métrica vas a mover."
        },
        "p2_3": {  # Valor económico del KPI
            "C": "⚠️  ALERTA DE ROI: No se ha calculado el valor económico del impacto. Sin este dato es imposible priorizar esta iniciativa frente a otras o aprobar presupuesto."
        },
        "p2_4": {  # Tiempo para ver impacto en KPIs
            "D": "⚠️  ALERTA DE VALOR: No está claro cuándo ni cómo se vería el impacto en los indicadores. Iniciativas sin horizonte de valor definido tienen alta probabilidad de ser canceladas."
        },
        "p3_3": {  # Tolerancia al error (antes p2_3)
            "C": "⚠️  ALERTA CRÍTICA: El proceso tiene alto impacto ante errores. Un agente autónomo puede generar consecuencias graves. Se requiere supervisión humana constante o descartar el agente."
        },
        "p4_1": {  # Disponibilidad de datos (antes p3_1)
            "C": "⚠️  ALERTA DE DATOS: Sin datos digitalizados y accesibles, ningún sistema de IA funcionará. Resuelve primero la calidad y acceso a datos."
        },
        "p4_2": {  # Capacidad técnica (antes p3_2)
            "C": "⚠️  ALERTA TÉCNICA: Sin capacidad técnica interna, el agente generará dependencia total de terceros y riesgo operacional alto."
        },
        "p6_2": {  # Resistencia del equipo (antes p5_2)
            "C": "⚠️  ALERTA DE ADOPCIÓN: Alta resistencia del equipo puede hacer fracasar el proyecto. Gestionar el cambio antes de construir."
        },
    }

    # Construir índice de texto → id de pregunta
    texto_a_id = {}
    for p_cat in CATEGORIAS:
        for p in p_cat["preguntas"]:
            texto_a_id[p["texto"]] = p["id"]

    for cat in resultados_categorias:
        for preg in cat["preguntas"]:
            pregunta_id = texto_a_id.get(preg["pregunta"])
            if pregunta_id and pregunta_id in ALERTAS_MAPA:
                respuesta = preg["respuesta"]
                if respuesta in ALERTAS_MAPA[pregunta_id]:
                    alertas.append(ALERTAS_MAPA[pregunta_id][respuesta])

    return alertas


def _veredicto_si(puntaje: float, alertas: list) -> dict:
    if puntaje >= 85:
        nivel = "AGENTE ALTAMENTE RECOMENDADO"
        emoji = "🟢"
        sustento = (
            f"Con un puntaje de {puntaje}%, esta iniciativa presenta las características ideales para un agente de IA. "
            "El problema es genuinamente complejo, con múltiples pasos interdependientes, datos no estructurados y "
            "necesidad de razonamiento adaptativo. El impacto en el negocio es significativo (alta frecuencia, "
            "tiempo invertido considerable, amplio alcance organizacional) y la organización cuenta con las "
            "condiciones técnicas y culturales para adoptarlo. Según el framework de Anthropic ('Building Effective Agents'), "
            "este es exactamente el tipo de problema donde los agentes añaden valor real que los workflows simples no pueden ofrecer."
        )
    else:
        nivel = "AGENTE RECOMENDADO"
        emoji = "🟢"
        sustento = (
            f"Con un puntaje de {puntaje}%, esta iniciativa tiene sólidos fundamentos para construir un agente. "
            "Hay complejidad real en el proceso, impacto de negocio justificable y condiciones técnicas adecuadas. "
            "Se recomienda comenzar con un prototipo acotado (MVP), validar en producción con supervisión humana "
            "y escalar progresivamente. Siguiendo el principio de Google Cloud: 'define el éxito antes de construir'."
        )

    return {
        "nivel": nivel,
        "emoji": emoji,
        "construir_agente": True,
        "sustento": sustento,
        "recomendaciones_construccion": [
            "Comenzar con un MVP (Producto Mínimo Viable) acotado en alcance",
            "Definir métricas claras de éxito antes de comenzar (tasa de error, tiempo ahorrado, adopción)",
            "Implementar supervisión humana en el loop durante las primeras semanas",
            "Usar herramientas gratuitas: Ollama (local) o Groq API para el LLM base",
            "Documentar todos los casos de borde y failures desde el inicio",
            "Planear un ciclo de evaluación y mejora continua (al menos mensual)",
        ],
        "alertas": alertas,
        "alternativas": []
    }


def _veredicto_hibrido(puntaje: float, cats_debiles: list, alertas: list) -> dict:
    nivel = "ZONA GRIS: EVALÚA ANTES DE CONSTRUIR"
    emoji = "🟡"

    cats_nombres = [c["nombre"] for c in cats_debiles]
    debilidades_texto = ", ".join(cats_nombres) if cats_nombres else "algunas dimensiones clave"

    sustento = (
        f"Con un puntaje de {puntaje}%, la iniciativa muestra potencial pero tiene debilidades importantes en: "
        f"{debilidades_texto}. Antes de comprometer recursos en un agente completo, se recomienda validar "
        "con una solución más simple (workflow, prompt chaining o LLM directo) para verificar que la complejidad "
        "de un agente es realmente necesaria. Como señala Anthropic: 'Aumenta la complejidad solo cuando las "
        "soluciones más simples demuestren ser insuficientes.'"
    )

    alternativas_recomendadas = _seleccionar_alternativas(cats_debiles)

    return {
        "nivel": nivel,
        "emoji": emoji,
        "construir_agente": False,
        "sustento": sustento,
        "recomendaciones_construccion": [
            "Validar primero con un workflow simple o prompt chaining durante 4-6 semanas",
            "Medir si la solución simple resuelve el 80% del problema",
            "Solo si quedan casos no resueltos, entonces construir el agente",
            "Resolver las brechas identificadas (datos, capacidad técnica, adopción) antes de escalar",
        ],
        "alertas": alertas,
        "alternativas": alternativas_recomendadas
    }


def _veredicto_no(puntaje: float, cats_debiles: list, alertas: list) -> dict:
    nivel = "NO SE RECOMIENDA CONSTRUIR UN AGENTE"
    emoji = "🔴"

    cats_nombres = [c["nombre"] for c in cats_debiles]
    debilidades_texto = ", ".join(cats_nombres) if cats_nombres else "múltiples dimensiones clave"

    sustento = (
        f"Con un puntaje de {puntaje}%, la iniciativa no justifica la inversión en un agente de IA en este momento. "
        f"Las debilidades son significativas en: {debilidades_texto}. "
        "Construir un agente en estas condiciones representaría un desperdicio de tiempo, esfuerzo y recursos, "
        "con alta probabilidad de fracaso técnico o de adopción. La evidencia de la industria muestra que el 99% "
        "de las implementaciones de agentes que fracasan lo hacen porque el problema no requería esa solución "
        "(Bain, 2024: solo 1% de implementaciones de agentes son consideradas 'maduras'). "
        "Existen alternativas más simples, económicas y confiables para resolver tu problema."
    )

    alternativas_recomendadas = _seleccionar_alternativas(cats_debiles)

    return {
        "nivel": nivel,
        "emoji": emoji,
        "construir_agente": False,
        "sustento": sustento,
        "recomendaciones_construccion": [],
        "alertas": alertas,
        "alternativas": alternativas_recomendadas
    }


def _seleccionar_alternativas(cats_debiles: list) -> list:
    """Selecciona las alternativas más relevantes según las categorías débiles."""
    alternativas_seleccionadas = []
    ids_debiles = {c["id"] for c in cats_debiles}

    # KPIs indefinidos → primero definir caso de negocio
    if "kpis" in ids_debiles:
        alternativas_seleccionadas.append(ALTERNATIVAS["definir_kpis"])

    # Siempre recomendar soluciones simples como punto de partida
    alternativas_seleccionadas.append(ALTERNATIVAS["llm_simple"])

    if "problema" in ids_debiles:
        # Problema no complejo → workflow o script simple
        alternativas_seleccionadas.append(ALTERNATIVAS["workflow"])
        alternativas_seleccionadas.append(ALTERNATIVAS["proceso_simple"])

    if "impacto" in ids_debiles:
        # Bajo impacto operacional → capacitación o dashboard
        alternativas_seleccionadas.append(ALTERNATIVAS["dashboard_bi"])
        alternativas_seleccionadas.append(ALTERNATIVAS["capacitacion"])

    if "viabilidad_tecnica" in ids_debiles:
        # Sin datos o capacidad técnica → RPA o workflow sin código
        alternativas_seleccionadas.append(ALTERNATIVAS["rpa"])

    if "complejidad_alternativas" in ids_debiles:
        # Proceso simple → prompt chaining o script
        alternativas_seleccionadas.append(ALTERNATIVAS["prompt_chaining"])
        alternativas_seleccionadas.append(ALTERNATIVAS["proceso_simple"])

    # Eliminar duplicados manteniendo orden
    vistas = set()
    resultado = []
    for alt in alternativas_seleccionadas:
        if alt["nombre"] not in vistas:
            vistas.add(alt["nombre"])
            resultado.append(alt)

    return resultado[:4]  # Máximo 4 alternativas
