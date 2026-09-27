"""Algoritmo para eliminar producciones-ε de una gramática."""

from __future__ import annotations

from gramatica import Gramatica
from produccion import Produccion


class EliminadorEpsilon:
    """Genera las producciones necesarias al eliminar producciones-ε."""

    def encontrar_nulables(self, gramatica: Gramatica) -> set[str]:
        """Encuentra los no terminales que pueden producir la cadena vacía."""
        nulables = {
            produccion.izquierda
            for produccion in gramatica.producciones
            if produccion.es_epsilon
        }

        cambio = True
        while cambio:
            cambio = False
            for produccion in gramatica.producciones:
                if produccion.es_epsilon or produccion.izquierda in nulables:
                    continue

                if all(simbolo in nulables for simbolo in produccion.derecha):
                    nulables.add(produccion.izquierda)
                    cambio = True

        return nulables

    def eliminar(self, gramatica: Gramatica) -> Gramatica:
        """Devuelve una gramática equivalente sin producciones-ε.

        Para cada producción se generan las combinaciones correspondientes a
        omitir o conservar cada aparición de un símbolo nullable. La variante
        cuyo cuerpo queda vacío se omite para que el resultado no contenga
        producciones-ε.
        """
        nulables = self.encontrar_nulables(gramatica)
        resultado: list[Produccion] = []
        claves: set[tuple[str, str]] = set()

        for produccion in gramatica.producciones:
            if produccion.es_epsilon:
                continue

            posiciones_nulables = [
                posicion
                for posicion, simbolo in enumerate(produccion.derecha)
                if simbolo in nulables
            ]

            cantidad_combinaciones = 1 << len(posiciones_nulables)
            for mascara in range(cantidad_combinaciones):
                cuerpo = "".join(
                    simbolo
                    for posicion, simbolo in enumerate(produccion.derecha)
                    if posicion not in posiciones_nulables
                    or not (mascara & (1 << posiciones_nulables.index(posicion)))
                )

                if not cuerpo:
                    continue

                nueva = Produccion(produccion.izquierda, cuerpo)
                clave = (nueva.izquierda, nueva.derecha)
                if clave not in claves:
                    resultado.append(nueva)
                    claves.add(clave)

        return Gramatica(resultado, gramatica.simbolo_inicial)
