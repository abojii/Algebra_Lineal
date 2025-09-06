# metodos.py
# Funciones para resolver sistemas 2x2 y 3x3 por sustitución y eliminación
# Incluye paso a paso
from sistema_2x2 import sustitucion_2x2 as s2x2_sustitucion, eliminacion_2x2 as s2x2_eliminacion
from sistema_3x3 import (
    sustitucion_3x3 as s3x3_sustitucion,
    eliminacion_3x3 as s3x3_eliminacion,
    gauss_jordan as s3x3_gauss_jordan,
    gauss as s3x3_gauss
)

def sustitucion_2x2(*args):
    return s2x2_sustitucion(*args)

def eliminacion_2x2(*args):
    return s2x2_eliminacion(*args)

def sustitucion_3x3(*args):
    return s3x3_sustitucion(*args)

def eliminacion_3x3(*args):
    return s3x3_eliminacion(*args)

def gauss_jordan(*args):
    return s3x3_gauss_jordan(*args)

def gauss(*args):
    return s3x3_gauss(*args)
