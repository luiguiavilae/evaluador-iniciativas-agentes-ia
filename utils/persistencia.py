"""
Sistema de persistencia para evaluaciones realizadas.
Guarda historial en JSON y exporta resumen a CSV.
"""

import csv
import json
import os
from datetime import datetime


ARCHIVO_JSON = "data/historial_evaluaciones.json"
ARCHIVO_CSV = "data/resumen_evaluaciones.csv"


def cargar_historial(base_dir: str) -> list:
    """Carga el historial de evaluaciones desde JSON."""
    ruta = os.path.join(base_dir, ARCHIVO_JSON)
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def guardar_evaluacion(evaluacion: dict, base_dir: str) -> None:
    """
    Guarda una evaluación completa en el historial JSON
    y actualiza el CSV de resumen.
    """
    # ── Guardar JSON completo ──────────────────────────────────────────────────
    os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
    ruta_json = os.path.join(base_dir, ARCHIVO_JSON)

    historial = cargar_historial(base_dir)
    historial.append(evaluacion)

    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

    # ── Actualizar CSV de resumen ──────────────────────────────────────────────
    ruta_csv = os.path.join(base_dir, ARCHIVO_CSV)
    encabezados = [
        "fecha", "responsable", "equipo", "iniciativa",
        "puntaje_global", "veredicto", "construir_agente",
        "alertas_count"
    ]

    fila = {
        "fecha": evaluacion["meta"]["fecha"],
        "responsable": evaluacion["meta"]["responsable"],
        "equipo": evaluacion["meta"]["equipo"],
        "iniciativa": evaluacion["meta"]["nombre_iniciativa"],
        "puntaje_global": evaluacion["resultados"]["puntaje_global"],
        "veredicto": evaluacion["veredicto"]["nivel"],
        "construir_agente": "Sí" if evaluacion["veredicto"]["construir_agente"] else "No",
        "alertas_count": len(evaluacion["veredicto"].get("alertas", [])),
    }

    archivo_existe = os.path.exists(ruta_csv)
    with open(ruta_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=encabezados)
        if not archivo_existe:
            writer.writeheader()
        writer.writerow(fila)


def mostrar_historial(base_dir: str) -> None:
    """Muestra un resumen del historial de evaluaciones en consola."""
    historial = cargar_historial(base_dir)

    if not historial:
        print("\n  No hay evaluaciones previas registradas.\n")
        return

    print(f"\n  {'─'*70}")
    print(f"  📋 HISTORIAL DE EVALUACIONES ({len(historial)} registros)")
    print(f"  {'─'*70}")
    print(f"  {'#':<4} {'Iniciativa':<28} {'Equipo':<18} {'Puntaje':>8}  {'Veredicto'}")
    print(f"  {'─'*70}")

    for i, ev in enumerate(historial, 1):
        meta = ev.get("meta", {})
        res = ev.get("resultados", {})
        ver = ev.get("veredicto", {})

        nombre = meta.get("nombre_iniciativa", "—")[:26]
        equipo = meta.get("equipo", "—")[:16]
        puntaje = res.get("puntaje_global", 0)
        emoji = ver.get("emoji", "")
        nivel = ver.get("nivel", "—")[:30]

        print(f"  {i:<4} {nombre:<28} {equipo:<18} {puntaje:>6.1f}%  {emoji} {nivel}")

    print(f"  {'─'*70}\n")
