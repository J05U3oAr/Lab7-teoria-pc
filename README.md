# Lab 7 — Eliminación de producciones-ε

Programa en Python para cargar gramáticas libres de contexto desde archivos de
texto, validarlas y eliminar sus producciones-ε.

## Ejecución

```bash
python main.py gramatica_1.txt gramatica_2.txt gramatica_3.txt
```

Cada línea debe contener una producción. Se aceptan `->` y `→`; las
alternativas se separan con `|`. Por ejemplo:

```text
S -> 0A | 1B | BB
C -> S | e
```

También se aceptan `ε` y `epsilon` para representar la cadena vacía.

Si el símbolo inicial es anulable, el programa lo informa durante la
ejecución. Como el enunciado solicita un resultado sin ninguna producción-ε,
en ese caso el lenguaje resultante es `L(G) - {ε}`.

## Pruebas

```bash
python -m unittest discover -v
```

Las pruebas comprueban las tres gramáticas, el cálculo de símbolos anulables,
la validación de entradas incorrectas y la detención del programa ante errores.

## Video demostrativo

[Ver el video demostrativo en YouTube](https://youtu.be/rmliuVchmsM)

## Clases principales

- `Produccion`: representa una producción individual.
- `ValidadorProducciones`: valida líneas y separa sus alternativas.
- `Gramatica`: agrupa producciones y elimina duplicados.
- `CargadorGramatica`: lee archivos UTF-8.
- `EliminadorEpsilon`: encuentra símbolos anulables y genera las `2^m`
  combinaciones necesarias.
