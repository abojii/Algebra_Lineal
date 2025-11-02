# solverMatrizInversa.py

from fractions import Fraction

def gauss_jordan_inverse(A):
    """
    Calcula la inversa de una matriz A mediante el método de Gauss-Jordan.
    Usa fracciones exactas para mantener precisión simbólica.
    Retorna la inversa y una lista de pasos del procedimiento.
    """
    n = len(A)

    # Convertimos todos los elementos a fracción
    A = [[Fraction(val) for val in row] for row in A]
    I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    augmented = [A[i] + I[i] for i in range(n)]

    steps = []
    steps.append("Matriz aumentada inicial [A | I]:")
    steps.append(matrix_to_string(augmented))

    for i in range(n):
        pivot_row = -1
        for k in range(i, n):
            if augmented[k][i] != 0:
                pivot_row = k
                break
        if pivot_row == -1:
            steps.append(f"No se encontró pivote en la columna {i+1}. La matriz no es invertible.")
            return None, steps

        if pivot_row != i:
            augmented[i], augmented[pivot_row] = augmented[pivot_row], augmented[i]
            steps.append(f"Intercambio de filas {i+1} y {pivot_row+1}:")
            steps.append(matrix_to_string(augmented))

        pivot = augmented[i][i]
        for j in range(2 * n):
            augmented[i][j] /= pivot
        steps.append(f"Dividir fila {i+1} por {pivot} para hacer el pivote 1:")
        steps.append(matrix_to_string(augmented))

        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(2 * n):
                    augmented[k][j] -= factor * augmented[i][j]
                steps.append(f"Eliminar entrada en fila {k+1} usando fila {i+1} (factor {factor}):")
                steps.append(matrix_to_string(augmented))

    inverse = [row[n:] for row in augmented]
    steps.append("Matriz inversa obtenida:")
    steps.append(matrix_to_string(inverse))
    return inverse, steps


def check_theoretical_properties(A, inverse):
    """
    Verifica las propiedades teóricas (c, d, e) de la matriz A.
    Devuelve una lista de interpretaciones en texto.
    """
    props = []
    if inverse:
        props.append("1. La matriz tiene n pivotes: Sí. Es invertible.")
        props.append("2. La ecuación Ax = 0 tiene solo la solución trivial: Sí. A es invertible.")
        props.append("3. Las columnas de A son linealmente independientes: Sí. A es invertible.")
    else:
        props.append("1. La matriz tiene n pivotes: No. No es invertible.")
        props.append("2. La ecuación Ax = 0 tiene soluciones no triviales: Sí. A no es invertible.")
        props.append("3. Las columnas de A son linealmente dependientes: Sí. A no es invertible.")
    return props


def matrix_to_string(matrix):
    """
    Convierte una matriz en string (usando fracciones) para mostrar en la interfaz.
    """
    return '\n'.join(['\t'.join([str(x) for x in row]) for row in matrix])
