"""
Generador de reportes en formato Markdown y PDF.
"""

import os
from datetime import datetime


def generar_markdown(evaluacion: dict) -> str:
    """
    Genera el contenido de un reporte en formato Markdown.

    Args:
        evaluacion: dict con todos los datos de la evaluación

    Returns:
        str: contenido Markdown del reporte
    """
    meta = evaluacion["meta"]
    resultados = evaluacion["resultados"]
    veredicto = evaluacion["veredicto"]
    puntaje = resultados["puntaje_global"]

    fecha_formateada = datetime.fromisoformat(meta["fecha"]).strftime("%d de %B de %Y, %H:%M")

    md = []
    md.append("# 🤖 Evaluación de Iniciativa de Agente de IA\n")
    md.append(f"> **Fecha:** {fecha_formateada}  \n")
    md.append(f"> **Iniciativa:** {meta['nombre_iniciativa']}  \n")
    md.append(f"> **Equipo / Empresa:** {meta['equipo']}  \n")
    md.append(f"> **Responsable:** {meta['responsable']}  \n\n")
    md.append("---\n\n")

    # ── Veredicto ────────────────────────────────────────────────────────────
    md.append("## Veredicto Final\n\n")
    md.append(f"### {veredicto['emoji']} {veredicto['nivel']}\n\n")
    md.append(f"**Puntaje Global: {puntaje}% / 100%**\n\n")
    md.append(_barra_progreso(puntaje) + "\n\n")
    md.append(f"{veredicto['sustento']}\n\n")

    # ── Alertas ───────────────────────────────────────────────────────────────
    if veredicto.get("alertas"):
        md.append("### ⚠️ Señales de Alerta Identificadas\n\n")
        for alerta in veredicto["alertas"]:
            md.append(f"- {alerta}\n")
        md.append("\n")

    md.append("---\n\n")

    # ── Resultados por categoría ──────────────────────────────────────────────
    md.append("## Resultados por Categoría\n\n")
    md.append("| Categoría | Puntaje | Porcentaje | Barra |\n")
    md.append("|-----------|---------|------------|-------|\n")
    for cat in resultados["categorias"]:
        barra = _barra_mini(cat["porcentaje"])
        md.append(f"| {cat['nombre']} | {cat['puntaje_obtenido']}/{cat['puntaje_maximo']} | {cat['porcentaje']}% | {barra} |\n")
    md.append("\n")

    # ── Detalle de respuestas ─────────────────────────────────────────────────
    md.append("## Detalle de Respuestas\n\n")
    for cat in resultados["categorias"]:
        md.append(f"### {cat['nombre']}\n\n")
        for i, preg in enumerate(cat["preguntas"], 1):
            md.append(f"**{i}. {preg['pregunta']}**  \n")
            md.append(f"✅ Respuesta elegida ({preg['respuesta']}): *{preg['texto_respuesta']}*  \n")
            md.append(f"📊 Puntaje: {preg['puntaje']} / {preg['puntaje_maximo']} puntos\n\n")

    md.append("---\n\n")

    # ── Recomendaciones de construcción ──────────────────────────────────────
    if veredicto.get("recomendaciones_construccion"):
        md.append("## ✅ Recomendaciones para Proceder\n\n")
        for rec in veredicto["recomendaciones_construccion"]:
            md.append(f"- {rec}\n")
        md.append("\n---\n\n")

    # ── Alternativas (si no se recomienda el agente) ──────────────────────────
    if veredicto.get("alternativas"):
        md.append("## 💡 Alternativas Recomendadas\n\n")
        md.append("Dado que un agente de IA no es la solución más adecuada para esta iniciativa, ")
        md.append("aquí hay alternativas que pueden resolver el problema de forma más eficiente:\n\n")

        for i, alt in enumerate(veredicto["alternativas"], 1):
            md.append(f"### {i}. {alt['nombre']}\n\n")
            md.append(f"**¿Qué es?** {alt['descripcion']}\n\n")
            md.append(f"**¿Cuándo usarla?** {alt['cuando']}\n\n")
            md.append(f"**Herramientas:** {', '.join(alt['herramientas'])}\n\n")

        md.append("---\n\n")

    # ── Referencias ───────────────────────────────────────────────────────────
    md.append("## 📚 Marcos de Referencia Utilizados\n\n")
    md.append("- [Anthropic: Building Effective Agents (2024)](https://www.anthropic.com/research/building-effective-agents)\n")
    md.append("- [Google Cloud: A Methodical Approach to Agent Evaluation](https://cloud.google.com/blog/topics/developers-practitioners/a-methodical-approach-to-agent-evaluation)\n")
    md.append("- [AWS: Agents vs Automation - A Strategic Guide](https://aws.amazon.com/executive-insights/content/agents-vs-automation-a-strategic-guide-for-business-leaders/)\n")
    md.append("- [Dataiku: How to Select High-Impact AI Agent Use Cases](https://www.dataiku.com/stories/blog/how-to-select-high-impact-ai-agent-use-cases)\n")
    md.append("- [McKinsey: Rethinking Decision Making to Unlock AI Potential](https://www.mckinsey.com/capabilities/operations/our-insights/when-can-ai-make-good-decisions-the-rise-of-ai-corporate-citizens)\n\n")
    md.append("---\n")
    md.append("*Reporte generado por el Evaluador de Iniciativas de Agentes de IA v1.0*\n")

    return "".join(md)


def guardar_markdown(evaluacion: dict, directorio_reportes: str) -> str:
    """
    Guarda el reporte Markdown en disco.

    Returns:
        str: ruta del archivo generado
    """
    os.makedirs(directorio_reportes, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_seguro = evaluacion["meta"]["nombre_iniciativa"].replace(" ", "_")[:30]
    nombre_archivo = f"reporte_{nombre_seguro}_{timestamp}.md"
    ruta = os.path.join(directorio_reportes, nombre_archivo)

    contenido = generar_markdown(evaluacion)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

    return ruta


def guardar_pdf(ruta_markdown: str) -> str:
    """
    Convierte el archivo Markdown a PDF usando md-to-pdf o weasyprint.
    Si no hay herramientas disponibles, informa al usuario.

    Returns:
        str: ruta del PDF generado, o mensaje de error
    """
    ruta_pdf = ruta_markdown.replace(".md", ".pdf")

    # Intentar con weasyprint (más común en entornos Python)
    try:
        import markdown
        from weasyprint import HTML, CSS

        with open(ruta_markdown, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Convertir Markdown a HTML
        html_content = markdown.markdown(
            md_content,
            extensions=["tables", "fenced_code", "nl2br"]
        )

        # CSS básico para el PDF
        css_style = CSS(string="""
            body {
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 { color: #1a1a2e; border-bottom: 3px solid #4a90d9; padding-bottom: 10px; }
            h2 { color: #16213e; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
            h3 { color: #0f3460; }
            table { border-collapse: collapse; width: 100%; margin: 15px 0; }
            th { background-color: #4a90d9; color: white; padding: 8px 12px; text-align: left; }
            td { padding: 6px 12px; border: 1px solid #ddd; }
            tr:nth-child(even) { background-color: #f8f9fa; }
            blockquote { border-left: 4px solid #4a90d9; padding-left: 15px; color: #555; margin: 10px 0; }
            code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 10pt; }
            hr { border: none; border-top: 1px solid #ddd; margin: 20px 0; }
        """)

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"><title>Evaluación de Agente</title></head>
        <body>{html_content}</body>
        </html>
        """

        HTML(string=full_html).write_pdf(ruta_pdf, stylesheets=[css_style])
        return ruta_pdf

    except ImportError:
        return None  # weasyprint no disponible


def _barra_progreso(porcentaje: float, ancho: int = 30) -> str:
    """Genera una barra de progreso en texto para Markdown."""
    llenos = int(porcentaje / 100 * ancho)
    vacios = ancho - llenos
    barra = "█" * llenos + "░" * vacios
    return f"`{barra}` **{porcentaje}%**"


def _barra_mini(porcentaje: float, ancho: int = 15) -> str:
    """Barra de progreso pequeña para tablas."""
    llenos = int(porcentaje / 100 * ancho)
    vacios = ancho - llenos
    return "█" * llenos + "░" * vacios
