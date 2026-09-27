"""Punto de entrada del laboratorio de teoría de la computación."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cargador_gramatica import CargadorGramatica
from eliminador_epsilon import EliminadorEpsilon


def configurar_salida() -> None:
    """Permite mostrar correctamente flechas y ε en la consola."""
    for salida in (sys.stdout, sys.stderr):
        if hasattr(salida, "reconfigure"):
            salida.reconfigure(encoding="utf-8")


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Elimina producciones-ε de archivos de gramáticas CFG."
    )
    parser.add_argument(
        "archivos",
        nargs="+",
        type=Path,
        help="Uno o más archivos de texto con las producciones.",
    )
    return parser


def ejecutar(archivos: list[Path]) -> int:
    cargador = CargadorGramatica()
    eliminador = EliminadorEpsilon()

    for archivo in archivos:
        print(f"\n{'=' * 72}\nArchivo: {archivo}\n{'=' * 72}")
        try:
            gramatica = cargador.cargar(archivo)
        except (FileNotFoundError, ValueError) as error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 1

        print("Gramática original:")
        print(gramatica)
        resultado, pasos = eliminador.eliminar_con_pasos(gramatica)

        print("\nEjecución del algoritmo:")
        for numero, paso in enumerate(pasos, start=1):
            print(f"{numero}. {paso}")

        print("\nGramática resultante sin producciones-ε:")
        print(resultado if resultado.producciones else "(sin producciones)")

    return 0


def main() -> int:
    configurar_salida()
    argumentos = construir_parser().parse_args()
    return ejecutar(argumentos.archivos)


if __name__ == "__main__":
    raise SystemExit(main())
