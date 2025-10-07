# Test para verificar la función es_homogeneo con el ejercicio 1 de la última imagen

import sys
from io import StringIO
from sistema import es_homogeneo
import sys
from io import StringIO

def test_sistema_no_homogeneo():
    matriz = [
        [1, 4, -5, 0],
        [2, -1, 8, 9]
    ]
    es_homog = es_homogeneo(matriz)
    print("Test 1 - Sistema no homogéneo:", "Correcto" if not es_homog else "Incorrecto")

def test_sistema_homogeneo_2x2():
    matriz = [
        [1, 2, 0],
        [3, 4, 0]
    ]
    es_homog = es_homogeneo(matriz)
    print("Test 2 - Sistema homogéneo 2x2:", "Correcto" if es_homog else "Incorrecto")

def test_sistema_homogeneo_3x3():
    matriz = [
        [1, 0, 2, 0],
        [0, 1, 3, 0],
        [4, 5, 6, 0]
    ]
    es_homog = es_homogeneo(matriz)
    print("Test 3 - Sistema homogéneo 3x3:", "Correcto" if es_homog else "Incorrecto")

def test_sistema_no_homogeneo_3x3():
    matriz = [
        [1, 0, 2, 0],
        [0, 1, 3, 0],
        [4, 5, 6, 1]
    ]
    es_homog = es_homogeneo(matriz)
    print("Test 4 - Sistema no homogéneo 3x3:", "Correcto" if not es_homog else "Incorrecto")

def test_sistema_vacio():
    matriz = []
    es_homog = es_homogeneo(matriz)
    print("Test 5 - Sistema vacío:", "Correcto" if not es_homog else "Incorrecto")

def test_sistema_invalido():
    matriz = [[1]]
    es_homog = es_homogeneo(matriz)
    print("Test 6 - Sistema inválido:", "Correcto" if not es_homog else "Incorrecto")

if __name__ == "__main__":
    test_sistema_no_homogeneo()
    test_sistema_homogeneo_2x2()
    test_sistema_homogeneo_3x3()
    test_sistema_no_homogeneo_3x3()
    test_sistema_vacio()
    test_sistema_invalido()
