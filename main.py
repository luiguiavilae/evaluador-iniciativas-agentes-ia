#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║        🤖 EVALUADOR DE INICIATIVAS DE AGENTES DE IA v1.0                   ║
║                                                                              ║
║  ¿Tu iniciativa realmente necesita un agente? Descúbrelo aquí.              ║
║                                                                              ║
║  Basado en frameworks de: Anthropic · Google Cloud · AWS · McKinsey         ║
╚══════════════════════════════════════════════════════════════════════════════╝

Uso:
    python main.py           → Iniciar nueva evaluación
    python main.py --historial → Ver evaluaciones previas
"""

import argparse
import os
import sys
from datetime import datetime

# Añadir el directorio raíz al path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from core.preguntas import CATEGORIAS
from core.evaluador import calcular_puntaje, generar_veredicto
from utils.reporte import guardar_markdown, guardar_pdf, generar_markdown
from utils.persistencia import guardar_evaluacion, mostrar_historial

# ── Colores ANSI para terminal ─────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
VERDE   = "\033[92m"
AMARILLO = "\033[93m"
ROJO    = "\033[91m"
AZUL    = "\033[94m"
CYAN    = "\033[96m"
BLANCO  = "\033[97m"
GRIS    = "\033[90m"


def limpiar():
    os.system("clear" if os.name == "posix" else "cls")


def separador(char="─", ancho=70, color=GRIS):
    print(f"{color}{char * ancho}{RESET}")


def titulo_seccion(texto: str):
    print(f"\n{BOLD}{AZUL}{texto}{RESET}")
    separador()


def imprimir_banner():
    limpiar()
    banner = f"""
{BOLD}{AZUL}╔══════════════════════════════════════════════════════════════════════╗
║        🤖  EVALUADOR DE INICIATIVAS DE AGENTES DE IA  v1.0          ║
║                                                                      ║
║  ¿Tu iniciativa realmente necesita un agente?                        ║
║  Responde {CYAN}16 preguntas{AZUL} y obtén un diagnóstico fundamentado.          ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}

{DIM}  Basado en: Anthropic · Google Cloud · AWS · McKinsey · Dataiku{RESET}
"""
    print(banner)


def recoger_metadatos() -> dict:
    """Solicita al usuario los datos básicos de la iniciativa."""
    titulo_seccion("📋 INFORMACIÓN DE LA INICIATIVA")
    print(f"{DIM}  Antes de comenzar, cuéntanos un poco sobre tu iniciativa.{RESET}\n")

    nombre = input(f"  {BOLD}Nombre de la iniciativa:{RESET} ").strip()
    while not nombre:
        print(f"  {ROJO}Por favor ingresa un nombre para la iniciativa.{RESET}")
        nombre = input(f"  {BOLD}Nombre de la iniciativa:{RESET} ").strip()

    equipo = input(f"  {BOLD}Equipo o empresa:{RESET} ").strip() or "No especificado"
    responsable = input(f"  {BOLD}Tu nombre / responsable:{RESET} ").strip() or "Anónimo"

    print(f"\n  {DIM}Describe brevemente el problema que quieres resolver con el agente:{RESET}")
    descripcion = input(f"  {BOLD}Descripción:{RESET} ").strip() or "No especificada"

    return {
        "nombre_iniciativa": nombre,
        "equipo": equipo,
        "responsable": responsable,
        "descripcion": descripcion,
        "fecha": datetime.now().isoformat()
    }


def hacer_pregunta(pregunta: dict, num_pregunta: int, total: int) -> tuple:
    """
    Presenta una pregunta al usuario y retorna (letra, puntaje).
    """
    print(f"\n  {BOLD}{CYAN}Pregunta {num_pregunta}/{total}{RESET}")
    print(f"  {BOLD}{pregunta['texto']}{RESET}")

    if "ayuda" in pregunta:
        print(f"  {DIM}💡 {pregunta['ayuda']}{RESET}")

    print()
    for letra, texto, _ in pregunta["opciones"]:
        print(f"    {BOLD}{AMARILLO}[{letra}]{RESET} {texto}")

    print()
    opciones_validas = {op[0].upper() for op in pregunta["opciones"]}

    while True:
        respuesta = input(f"  {BOLD}Tu respuesta [{'/'.join(sorted(opciones_validas))}]:{RESET} ").strip().upper()
        if respuesta in opciones_validas:
            puntaje = next(op[2] for op in pregunta["opciones"] if op[0] == respuesta)
            return respuesta, puntaje
        else:
            print(f"  {ROJO}Opción inválida. Por favor elige: {', '.join(sorted(opciones_validas))}{RESET}")


def ejecutar_cuestionario() -> dict:
    """
    Ejecuta el cuestionario completo por categorías.

    Returns:
        dict de {pregunta_id: (letra, puntaje)}
    """
    respuestas = {}
    total_preguntas = sum(len(cat["preguntas"]) for cat in CATEGORIAS)
    contador = 0

    for categoria in CATEGORIAS:
        print(f"\n\n{BOLD}{AZUL}{'═' * 70}{RESET}")
        print(f"{BOLD}{AZUL}  {categoria['nombre']}{RESET}")
        print(f"{BOLD}{AZUL}{'═' * 70}{RESET}")
        print(f"  {DIM}{categoria['descripcion']}{RESET}")

        for pregunta in categoria["preguntas"]:
            contador += 1
            letra, puntaje = hacer_pregunta(pregunta, contador, total_preguntas)
            respuestas[pregunta["id"]] = (letra, puntaje)

    return respuestas


def mostrar_barra_progreso_terminal(porcentaje: float, ancho: int = 35) -> str:
    """Genera una barra de progreso coloreada para terminal."""
    llenos = int(porcentaje / 100 * ancho)
    vacios = ancho - llenos

    if porcentaje >= 70:
        color = VERDE
    elif porcentaje >= 45:
        color = AMARILLO
    else:
        color = ROJO

    barra = f"{color}{'█' * llenos}{DIM}{'░' * vacios}{RESET}"
    return barra


def mostrar_resultados(resultados: dict, veredicto: dict):
    """Presenta los resultados de forma visual en la terminal."""
    puntaje = resultados["puntaje_global"]

    limpiar()
    print(f"\n{BOLD}{AZUL}{'═' * 70}{RESET}")
    print(f"{BOLD}{AZUL}  📊 RESULTADOS DE LA EVALUACIÓN{RESET}")
    print(f"{BOLD}{AZUL}{'═' * 70}{RESET}\n")

    # ── Veredicto principal ───────────────────────────────────────────────────
    if veredicto["construir_agente"]:
        color_veredicto = VERDE
    elif puntaje >= 45:
        color_veredicto = AMARILLO
    else:
        color_veredicto = ROJO

    print(f"  {BOLD}{color_veredicto}{veredicto['emoji']} {veredicto['nivel']}{RESET}")
    print(f"\n  {BOLD}Puntaje Global: {color_veredicto}{puntaje}% / 100%{RESET}")
    print(f"  {mostrar_barra_progreso_terminal(puntaje)}  {color_veredicto}{puntaje:.1f}%{RESET}")

    # ── Sustento ──────────────────────────────────────────────────────────────
    print(f"\n{BOLD}  📝 Sustento:{RESET}")
    # Wrap texto largo
    palabras = veredicto["sustento"].split()
    linea = "  "
    for palabra in palabras:
        if len(linea) + len(palabra) > 72:
            print(linea)
            linea = "  " + palabra + " "
        else:
            linea += palabra + " "
    if linea.strip():
        print(linea)

    # ── Alertas ───────────────────────────────────────────────────────────────
    if veredicto.get("alertas"):
        print(f"\n{BOLD}{AMARILLO}  Señales de alerta:{RESET}")
        for alerta in veredicto["alertas"]:
            print(f"\n  {AMARILLO}{alerta}{RESET}")

    # ── Resultados por categoría ──────────────────────────────────────────────
    print(f"\n\n{BOLD}  📋 Resultados por Categoría:{RESET}")
    separador()

    for cat in resultados["categorias"]:
        barra = mostrar_barra_progreso_terminal(cat["porcentaje"], ancho=25)
        print(f"\n  {cat['nombre']}")
        print(f"  {barra}  {cat['porcentaje']:.1f}%  ({cat['puntaje_obtenido']}/{cat['puntaje_maximo']} pts)")

    # ── Recomendaciones ───────────────────────────────────────────────────────
    if veredicto.get("recomendaciones_construccion"):
        print(f"\n\n{BOLD}{VERDE}  ✅ Recomendaciones para proceder:{RESET}")
        separador(color=VERDE)
        for rec in veredicto["recomendaciones_construccion"]:
            print(f"  {VERDE}→{RESET} {rec}")

    # ── Alternativas ──────────────────────────────────────────────────────────
    if veredicto.get("alternativas"):
        print(f"\n\n{BOLD}{CYAN}  💡 Alternativas Recomendadas:{RESET}")
        separador(color=CYAN)
        for i, alt in enumerate(veredicto["alternativas"], 1):
            print(f"\n  {BOLD}{CYAN}{i}. {alt['nombre']}{RESET}")
            print(f"  {alt['descripcion']}")
            print(f"  {DIM}📦 Herramientas: {', '.join(alt['herramientas'])}{RESET}")

    print(f"\n{BOLD}{AZUL}{'═' * 70}{RESET}\n")


def preguntar_exportar(evaluacion: dict) -> tuple:
    """Pregunta al usuario si desea exportar el reporte y lo genera."""
    print(f"\n  {BOLD}¿Deseas exportar el reporte de esta evaluación?{RESET}")
    print(f"  {AMARILLO}[M]{RESET} Exportar como Markdown (.md)")
    print(f"  {AMARILLO}[P]{RESET} Exportar como Markdown + intentar PDF")
    print(f"  {AMARILLO}[N]{RESET} No exportar ahora")

    opcion = input(f"\n  Tu opción [M/P/N]: ").strip().upper()

    directorio_reportes = os.path.join(BASE_DIR, "reports")
    ruta_md = None
    ruta_pdf = None

    if opcion in ("M", "P"):
        ruta_md = guardar_markdown(evaluacion, directorio_reportes)
        print(f"\n  {VERDE}✅ Reporte Markdown guardado en:{RESET}")
        print(f"  {DIM}{ruta_md}{RESET}")

        if opcion == "P":
            print(f"\n  {DIM}Intentando generar PDF (requiere weasyprint + markdown)...{RESET}")
            ruta_pdf = guardar_pdf(ruta_md)
            if ruta_pdf:
                print(f"  {VERDE}✅ PDF guardado en:{RESET}")
                print(f"  {DIM}{ruta_pdf}{RESET}")
            else:
                print(f"  {AMARILLO}⚠️  PDF no disponible. Instala: pip install weasyprint markdown{RESET}")
                print(f"  {DIM}El reporte Markdown ya está guardado y puede convertirse manualmente.{RESET}")

    return ruta_md, ruta_pdf


def main():
    parser = argparse.ArgumentParser(
        description="Evaluador de Iniciativas de Agentes de IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py               → Iniciar nueva evaluación
  python main.py --historial   → Ver evaluaciones anteriores
        """
    )
    parser.add_argument(
        "--historial",
        action="store_true",
        help="Mostrar el historial de evaluaciones anteriores"
    )
    args = parser.parse_args()

    if args.historial:
        imprimir_banner()
        mostrar_historial(BASE_DIR)
        return

    # ── FLUJO PRINCIPAL ────────────────────────────────────────────────────────
    imprimir_banner()

    print(f"  {DIM}Este evaluador te ayudará a determinar si tu iniciativa realmente{RESET}")
    print(f"  {DIM}amerita construir un agente de IA, o si existe una solución más{RESET}")
    print(f"  {DIM}simple, económica y efectiva para tu problema.{RESET}")
    print(f"\n  {BOLD}El cuestionario toma aproximadamente 5-10 minutos.{RESET}")
    print(f"\n  {DIM}Presiona {BOLD}Enter{RESET}{DIM} para comenzar o {BOLD}Ctrl+C{RESET}{DIM} para salir.{RESET}")

    try:
        input()
    except KeyboardInterrupt:
        print(f"\n  {DIM}Evaluación cancelada. ¡Hasta pronto!{RESET}\n")
        sys.exit(0)

    # 1. Metadatos
    meta = recoger_metadatos()

    # 2. Cuestionario
    try:
        print(f"\n\n  {BOLD}Comenzando el cuestionario...{RESET}")
        print(f"  {DIM}(Puedes presionar Ctrl+C en cualquier momento para cancelar){RESET}")
        respuestas = ejecutar_cuestionario()
    except KeyboardInterrupt:
        print(f"\n\n  {AMARILLO}⚠️  Evaluación interrumpida por el usuario.{RESET}\n")
        sys.exit(0)

    # 3. Calcular resultados
    resultados = calcular_puntaje(respuestas)
    veredicto = generar_veredicto(
        resultados["puntaje_global"],
        resultados["categorias"]
    )

    # 4. Ensamblar evaluación completa
    evaluacion = {
        "meta": meta,
        "respuestas": {k: list(v) for k, v in respuestas.items()},
        "resultados": resultados,
        "veredicto": veredicto
    }

    # 5. Guardar en historial
    guardar_evaluacion(evaluacion, BASE_DIR)

    # 6. Mostrar resultados en pantalla
    mostrar_resultados(resultados, veredicto)

    # 7. Exportar reporte
    preguntar_exportar(evaluacion)

    print(f"\n  {BOLD}{VERDE}¡Evaluación completada!{RESET}")
    print(f"  {DIM}Puedes ver el historial con: python main.py --historial{RESET}\n")


if __name__ == "__main__":
    main()
