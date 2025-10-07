# metodos.py
# Funciones para resolver sistemas 2x2 y 3x3 por sustitución y eliminación
# Incluye paso a paso
from Models.sistema_2x2 import sustitucion_2x2 as s2x2_sustitucion, eliminacion_2x2 as s2x2_eliminacion
from Models.sistema_3x3 import (
    sustitucion_3x3 as s3x3_sustitucion,
    eliminacion_3x3 as s3x3_eliminacion,
    gauss_jordan as s3x3_gauss_jordan,
    gauss as s3x3_gauss
)
import copy

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

def determinant(matrix):
    # Calculate determinant of square matrix recursively
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    det = 0
    for c in range(n):
        minor = [row[:c] + row[c+1:] for row in matrix[1:]]
        det += ((-1)**c) * matrix[0][c] * determinant(minor)
    return det

def row_reduce(matrix):
    # Perform row reduction to row echelon form
    mat = copy.deepcopy(matrix)
    rows = len(mat)
    cols = len(mat[0])
    lead = 0
    for r in range(rows):
        if lead >= cols:
            return mat
        i = r
        while mat[i][lead] == 0:
            i += 1
            if i == rows:
                i = r
                lead += 1
                if lead == cols:
                    return mat
        mat[i], mat[r] = mat[r], mat[i]
        lv = mat[r][lead]
        mat[r] = [mrx / lv for mrx in mat[r]]
        for i in range(rows):
            if i != r:
                lv = mat[i][lead]
                mat[i] = [iv - lv*rv for rv, iv in zip(mat[r], mat[i])]
        lead += 1
    return mat

def rank(matrix):
    # Calculate rank by counting non-zero rows in row echelon form
    rref = row_reduce(matrix)
    rank = 0
    for row in rref:
        if any(abs(x) > 1e-10 for x in row):
            rank += 1
    return rank

def are_vectors_dependent(vectors):
    """
    Determine if vectors are linearly dependent.
    vectors: list of vectors as columns (list of lists)
    Returns True if dependent, False if independent.
    """
    if not vectors:
        return False  # empty set considered independent

    # Transpose vectors to rows for matrix operations
    matrix = [list(row) for row in zip(*vectors)]
    rows = len(matrix)
    cols = len(matrix[0])

    if rows == cols:
        det = determinant(matrix)
        if abs(det) < 1e-10:
            return True  # dependent
        else:
            return False  # independent
    else:
        r = rank(matrix)
        # Fix: if number of vectors (cols) > dimension (rows), always dependent
        if cols > rows:
            return True
        if r < min(rows, cols):
            return True
        else:
            return False
