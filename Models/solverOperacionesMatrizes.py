
"""from Models.solverHomogeneo import create_matrix
from Models.solverMatrizInversa import matrix_to_string


def _validate_rectangular(mat):

    if not mat:
        raise ValueError("La matriz no puede estar vacía.")
    ncols = len(mat[0])
    if any(len(row) != ncols for row in mat):
        raise ValueError("La matriz no es rectangular (filas con longitudes distintas).")

def _same_shape(A, B):

    _validate_rectangular(A)
    _validate_rectangular(B)
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Las matrices A y B deben tener el mismo tamaño m x n.")

def add_matrices(A, B, explain=False, precision=4):
    
    _same_shape(A, B)
    m, n = len(A), len(A[0])
    C = create_matrix(m, n)
    pasos = []
    if explain:
        pasos.append("Suma A + B definida: ambas son m x n del mismo tamaño.")
    for i in range(m):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
            if explain:
                pasos.append(f"c[{i+1},{j+1}] = {A[i][j]} + {B[i][j]} = {C[i][j]}")
    if explain:
        pasos.append("Resultado:\n" + matrix_to_string(C, precision=precision))
        return C, "\n".join(pasos)
    return C

def sub_matrices(A, B, explain=False, precision=4):
    
    _same_shape(A, B)
    m, n = len(A), len(A[0])
    C = create_matrix(m, n)
    pasos = []
    if explain:
        pasos.append("Resta A - B definida: ambas son m x n del mismo tamaño.")
    for i in range(m):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
            if explain:
                pasos.append(f"c[{i+1},{j+1}] = {A[i][j]} - {B[i][j]} = {C[i][j]}")
    if explain:
        pasos.append("Resultado:\n" + matrix_to_string(C, precision=precision))
        return C, "\n".join(pasos)
    return C"""