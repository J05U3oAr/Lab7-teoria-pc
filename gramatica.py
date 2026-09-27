"""Estructura de datos para una gramática libre de contexto."""

from __future__ import annotations

from collections.abc import Iterable

from produccion import Produccion


class Gramatica:
    """Agrupa producciones y conserva el orden en que fueron declaradas."""

    def __init__(
        self,
        producciones: Iterable[Produccion] = (),
        simbolo_inicial: str | None = None,
    ) -> None:
        self._producciones: list[Produccion] = []
        self._claves: set[tuple[str, str]] = set()

        for produccion in producciones:
            self.agregar(produccion)

        if simbolo_inicial is None:
            self._simbolo_inicial = (
                self._producciones[0].izquierda if self._producciones else None
            )
        elif self._producciones and simbolo_inicial not in self.no_terminales:
            raise ValueError(
                "El símbolo inicial debe aparecer como lado izquierdo "
                "de alguna producción."
            )
        else:
            self._simbolo_inicial = simbolo_inicial

    @property
    def producciones(self) -> tuple[Produccion, ...]:
        """Devuelve las producciones sin permitir modificaciones directas."""
        return tuple(self._producciones)

    @property
    def simbolo_inicial(self) -> str | None:
        return self._simbolo_inicial

    @property
    def no_terminales(self) -> tuple[str, ...]:
        """Devuelve los no terminales en orden de aparición."""
        resultado: list[str] = []
        vistos: set[str] = set()

        for produccion in self._producciones:
            if produccion.izquierda not in vistos:
                resultado.append(produccion.izquierda)
                vistos.add(produccion.izquierda)

        return tuple(resultado)

    def agregar(self, produccion: Produccion) -> None:
        """Agrega una producción si todavía no existe."""
        if not isinstance(produccion, Produccion):
            raise TypeError("Solo se pueden agregar objetos Produccion.")

        clave = (produccion.izquierda, produccion.derecha)
        if clave not in self._claves:
            self._producciones.append(produccion)
            self._claves.add(clave)

    def producciones_de(self, no_terminal: str) -> tuple[Produccion, ...]:
        """Devuelve las producciones cuyo lado izquierdo coincide."""
        return tuple(
            produccion
            for produccion in self._producciones
            if produccion.izquierda == no_terminal
        )

    def sin_epsilon(self) -> "Gramatica":
        """Crea una copia de la gramática omitiendo producciones-ε."""
        return Gramatica(
            (
                produccion
                for produccion in self._producciones
                if not produccion.es_epsilon
            ),
            self._simbolo_inicial,
        )

    def __str__(self) -> str:
        """Formatea las alternativas agrupadas por no terminal."""
        lineas: list[str] = []
        for no_terminal in self.no_terminales:
            alternativas = " | ".join(
                produccion.derecha
                for produccion in self.producciones_de(no_terminal)
            )
            lineas.append(f"{no_terminal} → {alternativas}")
        return "\n".join(lineas)
