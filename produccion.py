"""Modelo de una producción individual de una gramática libre de contexto."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Produccion:
    """Representa una producción de la forma ``no_terminal -> cuerpo``.

    Una instancia representa una sola alternativa. Por ejemplo, la línea
    ``S -> 0A | 1B`` se convierte en dos objetos ``Produccion`` distintos.
    La producción vacía se almacena internamente como ``"ε"``.
    """

    izquierda: str
    derecha: str

    SIMBOLO_EPSILON = "ε"
    ALIAS_EPSILON = frozenset({"ε", "e", "epsilon"})

    def __post_init__(self) -> None:
        """Normaliza los valores y valida la forma básica de la producción."""
        izquierda = self.izquierda.strip()
        derecha = self.derecha.strip()

        if len(izquierda) != 1 or not izquierda.isupper():
            raise ValueError(
                "El lado izquierdo debe ser un único no terminal en mayúscula."
            )

        if not derecha:
            raise ValueError("El lado derecho no puede estar vacío; use ε.")

        if derecha in self.ALIAS_EPSILON or derecha.lower() == "epsilon":
            derecha = self.SIMBOLO_EPSILON

        object.__setattr__(self, "izquierda", izquierda)
        object.__setattr__(self, "derecha", derecha)

    @property
    def es_epsilon(self) -> bool:
        """Indica si la producción genera la cadena vacía."""
        return self.derecha == self.SIMBOLO_EPSILON

    def contiene(self, simbolo: str) -> bool:
        """Indica si el cuerpo contiene el símbolo indicado."""
        return simbolo in self.derecha

    def __str__(self) -> str:
        """Devuelve la producción en un formato legible."""
        return f"{self.izquierda} → {self.derecha}"
