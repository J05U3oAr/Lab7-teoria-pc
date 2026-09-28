"""Pruebas funcionales para la eliminación de producciones-ε."""

from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from cargador_gramatica import CargadorGramatica
from eliminador_epsilon import EliminadorEpsilon
from gramatica import Gramatica
from main import ejecutar
from produccion import Produccion
from validador_producciones import ValidadorProducciones


class PruebasProduccionYValidacion(unittest.TestCase):
    def test_normaliza_alias_de_epsilon(self) -> None:
        for alias in ("ε", "e", "epsilon", "EPSILON"):
            with self.subTest(alias=alias):
                self.assertTrue(Produccion("S", alias).es_epsilon)

    def test_acepta_flechas_y_alternativas(self) -> None:
        producciones = ValidadorProducciones.validar_linea(
            "S → 0A | 1B | BB"
        )
        self.assertEqual(
            ["0A", "1B", "BB"],
            [produccion.derecha for produccion in producciones],
        )

    def test_rechaza_lineas_mal_formadas(self) -> None:
        lineas_invalidas = (
            "S => A",
            "s -> A",
            "S -> A || B",
            "S -> A$",
            "S -> εA",
            "S -> epsilonA",
        )
        for linea in lineas_invalidas:
            with self.subTest(linea=linea):
                with self.assertRaises(ValueError):
                    ValidadorProducciones.validar_linea(linea)


class PruebasGramatica(unittest.TestCase):
    def test_elimina_duplicados(self) -> None:
        gramatica = Gramatica(
            [Produccion("S", "a"), Produccion("S", "a")]
        )
        self.assertEqual(1, len(gramatica.producciones))

    def test_conserva_simbolo_inicial_aunque_quede_sin_reglas(self) -> None:
        gramatica = Gramatica(
            [Produccion("S", "ε"), Produccion("A", "a")]
        )
        resultado = gramatica.sin_epsilon()
        self.assertEqual("S", resultado.simbolo_inicial)
        self.assertEqual((Produccion("A", "a"),), resultado.producciones)


class PruebasEliminacionEpsilon(unittest.TestCase):
    RESULTADOS_ESPERADOS = (
        {
            "S": {"0A", "0", "1B", "1", "BB", "B"},
            "A": {"C"},
            "B": {"S", "A"},
            "C": {"S"},
        },
        {
            "S": {"aAa", "aa", "bBb", "bb"},
            "A": {"C", "a"},
            "B": {"C", "b"},
            "C": {"CDE", "DE", "CE", "E"},
            "D": {"A", "B", "ab"},
        },
        {
            "S": {"ASA", "SA", "AS", "S", "aB", "a"},
            "A": {"B", "S"},
            "B": {"b"},
        },
    )

    def setUp(self) -> None:
        self.cargador = CargadorGramatica()
        self.eliminador = EliminadorEpsilon()

    def test_resultados_de_las_tres_gramaticas(self) -> None:
        for numero, esperado in enumerate(self.RESULTADOS_ESPERADOS, start=1):
            with self.subTest(gramatica=numero):
                original = self.cargador.cargar(f"gramatica_{numero}.txt")
                resultado = self.eliminador.eliminar(original)
                real = {
                    no_terminal: {
                        produccion.derecha
                        for produccion in resultado.producciones_de(no_terminal)
                    }
                    for no_terminal in resultado.no_terminales
                }
                self.assertEqual(esperado, real)
                self.assertFalse(
                    any(
                        produccion.es_epsilon
                        for produccion in resultado.producciones
                    )
                )

    def test_programa_se_detiene_ante_archivo_invalido(self) -> None:
        with tempfile.TemporaryDirectory() as directorio:
            archivo = Path(directorio) / "invalida.txt"
            archivo.write_text("S -> a\nesta linea es invalida\n", encoding="utf-8")

            salida = io.StringIO()
            errores = io.StringIO()
            with redirect_stdout(salida), redirect_stderr(errores):
                codigo = ejecutar([archivo])

            self.assertEqual(1, codigo)
            self.assertIn("línea 2", errores.getvalue())


if __name__ == "__main__":
    unittest.main()
