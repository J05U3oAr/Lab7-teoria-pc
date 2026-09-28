"""Validación y conversión de líneas de una gramática."""

from __future__ import annotations

import re

from produccion import Produccion


class ValidadorProducciones:
    """Convierte una línea con alternativas en objetos ``Produccion``."""

    _PATRON_LINEA = re.compile(r"^\s*([A-Z])\s*(?:->|→)\s*(.*?)\s*$")
    _PATRON_CUERPO = re.compile(r"^[A-Za-z0-9ε]+$")

    @classmethod
    def validar_linea(
        cls, linea: str, numero_linea: int | None = None
    ) -> list[Produccion]:
        """Valida una línea y devuelve una producción por cada alternativa.

        Se aceptan las flechas ``->`` y ``→``. Los espacios dentro del cuerpo
        se ignoran para permitir formatos como ``S -> 0 A | 1 B``.
        """
        texto = linea.strip()
        ubicacion = f" en la línea {numero_linea}" if numero_linea else ""

        coincidencia = cls._PATRON_LINEA.fullmatch(texto)
        if coincidencia is None:
            raise ValueError(
                f"Producción inválida{ubicacion}: se esperaba 'A -> cuerpo'."
            )

        izquierda, cuerpo = coincidencia.groups()
        alternativas = cuerpo.split("|")
        if not cuerpo or any(not alternativa.strip() for alternativa in alternativas):
            raise ValueError(
                f"Producción inválida{ubicacion}: falta una alternativa."
            )

        producciones: list[Produccion] = []
        for alternativa in alternativas:
            derecha = re.sub(r"\s+", "", alternativa)

            if not cls._PATRON_CUERPO.fullmatch(derecha):
                raise ValueError(
                    f"Producción inválida{ubicacion}: símbolos no permitidos "
                    f"en '{alternativa.strip()}'."
                )

            if derecha in {"ε", "e"} or derecha.lower() == "epsilon":
                derecha = Produccion.SIMBOLO_EPSILON
            elif "ε" in derecha or "epsilon" in derecha.lower():
                raise ValueError(
                    f"Producción inválida{ubicacion}: ε debe aparecer sola "
                    "en una alternativa."
                )

            producciones.append(Produccion(izquierda, derecha))

        return producciones
