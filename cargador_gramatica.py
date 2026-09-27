"""Carga gramáticas desde archivos de texto."""

from __future__ import annotations

from pathlib import Path

from gramatica import Gramatica
from validador_producciones import ValidadorProducciones


class CargadorGramatica:
    """Lee y valida un archivo que contiene una producción por línea."""

    def cargar(self, ruta: str | Path) -> Gramatica:
        """Carga una gramática UTF-8 y reporta errores con su ubicación."""
        archivo = Path(ruta)
        if not archivo.is_file():
            raise FileNotFoundError(f"No existe el archivo de gramática: {archivo}")

        producciones = []
        for numero_linea, linea in enumerate(
            archivo.read_text(encoding="utf-8").splitlines(), start=1
        ):
            texto = linea.strip()
            if not texto or texto.startswith("#"):
                continue

            try:
                producciones.extend(
                    ValidadorProducciones.validar_linea(texto, numero_linea)
                )
            except ValueError as error:
                raise ValueError(f"{archivo.name}: {error}") from error

        if not producciones:
            raise ValueError(f"El archivo {archivo.name} no contiene producciones.")

        return Gramatica(producciones)
