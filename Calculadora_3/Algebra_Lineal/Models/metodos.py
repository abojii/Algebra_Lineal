# metodos.py
# Funciones para resolver sistemas 2x2 y 3x3 por sustitución y eliminación
# Incluye paso a paso
# Ahora incluye métodos generales para cualquier tamaño
from sistema_2x2 import sustitucion_2x2 as s2x2_sustitucion, eliminacion_2x2 as s2x2_eliminacion
from sistema_3x3 import (
    sustitucion_3x3 as s3x3_sustitucion,
    eliminacion_3x3 as s3x3_eliminacion,
    gauss_jordan as s3x3_gauss_jordan,
    gauss as s3x3_gauss
)
import entrada
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

# Funciones generales para cualquier tamaño de sistema

def escalonada_matriz(M_aug, mostrar_pasos=True, mostrar_pivotes=False):
    """
    Convierte la matriz aumentada a forma escalonada (row echelon form) usando eliminación Gaussiana.
    """
    M = copy.deepcopy(M_aug)
    filas = len(M)
    columnas = len(M[0])
    paso = 1

    for i in range(min(filas, columnas - 1)):
        # Encontrar pivote
        pivote_fila = i
        for k in range(i + 1, filas):
            if abs(M[k][i]) > abs(M[pivote_fila][i]):
                pivote_fila = k

        # Intercambiar filas si es necesario
        if pivote_fila != i:
            M[i], M[pivote_fila] = M[pivote_fila], M[i]
            if mostrar_pasos:
                print(f"Paso {paso}: Intercambio de filas {i+1} y {pivote_fila+1}")
                entrada.imprimir_matriz(M)
                paso += 1

        # Verificar si el pivote es cero (no invertible, pero continuamos)
        if M[i][i] == 0:
            if mostrar_pasos:
                print(f"Paso {paso}: Pivote en fila {i+1}, columna {i+1} es cero. Continuando...")
                paso += 1
            continue

        if mostrar_pivotes:
            print(f"Pivote encontrado en fila {i+1}, columna {i+1}: {M[i][i]}")

        # Eliminación hacia abajo
        for k in range(i + 1, filas):
            factor = M[k][i] / M[i][i]
            for j in range(columnas):
                M[k][j] -= factor * M[i][j]
            if mostrar_pasos:
                print(f"Paso {paso}: Eliminación en fila {k+1} usando fila {i+1} (factor: {factor})")
                entrada.imprimir_matriz(M)
                paso += 1

    return M

def escalonada_reducida_matriz(M_aug, mostrar_pasos=True, mostrar_pivotes=False):
    """
    Convierte la matriz aumentada a forma escalonada reducida (reduced row echelon form) usando Gauss-Jordan.
    """
    M = escalonada_matriz(M_aug, mostrar_pasos, mostrar_pivotes)
    filas = len(M)
    columnas = len(M[0])
    paso = 1 if not mostrar_pasos else (min(filas, columnas - 1) * 2 + 1)  # Continuar numeración

    # Eliminación hacia arriba
    for i in range(min(filas, columnas - 1) - 1, -1, -1):
        if M[i][i] == 0:
            continue
        # Hacer pivote 1
        pivote = M[i][i]
        for j in range(columnas):
            M[i][j] /= pivote
        if mostrar_pasos:
            print(f"Paso {paso}: Normalizar fila {i+1} (dividir por {pivote})")
            entrada.imprimir_matriz(M)
            paso += 1

        # Eliminación hacia arriba
        for k in range(i - 1, -1, -1):
            factor = M[k][i]
            for j in range(columnas):
                M[k][j] -= factor * M[i][j]
            if mostrar_pasos:
                print(f"Paso {paso}: Eliminación hacia arriba en fila {k+1} usando fila {i+1} (factor: {factor})")
                entrada.imprimir_matriz(M)
                paso += 1

    return M

def gauss(M_aug, mostrar_pasos=True, mostrar_pivotes=False):
    """
    Método de Gauss: forma escalonada + back substitution para resolver el sistema.
    """
    M = escalonada_matriz(M_aug, mostrar_pasos, mostrar_pivotes)
    filas = len(M)
    columnas = len(M[0])
    n = filas

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        if M[i][i] == 0:
            if M[i][-1] != 0:
                return None  # Sistema inconsistente
            else:
                x[i] = 0  # Variable libre, asumimos 0
                continue
        suma = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (M[i][-1] - suma) / M[i][i]

    return x

def format_num(num):
    if isinstance(num, float):
        return f"{num:.2f}"
    return str(num)

def format_matrix(M):
    # Format all numbers in matrix to 2 decimals for printing
    formatted = []
    for row in M:
        formatted_row = [format_num(x) for x in row]
        formatted.append(formatted_row)
    return formatted

def print_matrix_with_format(M):
    # Print matrix with formatted numbers aligned
    cols = len(M[0])
    widths = [max(len(str(M[i][j])) for i in range(len(M))) for j in range(cols)]
    for fila in M:
        cuerpo = "  ".join(str(x).rjust(widths[j]) for j, x in enumerate(fila[:-1]))
        print(f"[ {cuerpo} | {str(fila[-1]).rjust(widths[-1])} ]")

def gauss_jordan_general(M_aug, mostrar_pasos=True, mostrar_pivotes=False):
    """
    Método de Gauss-Jordan: forma escalonada reducida + extraer solución.
    Muestra paso a paso con formato de matriz y operaciones.
    """
    M = [row[:] for row in M_aug]  # deep copy
    filas = len(M)
    columnas = len(M[0])
    paso = 1

    if mostrar_pasos:
        print("Matriz inicial:")
        print_matrix_with_format(format_matrix(M))

    for i in range(filas):
        # Encontrar pivote
        pivote = M[i][i]
        if abs(pivote) < 1e-12:
            print(f"Pivote en fila {i+1}, columna {i+1} es cero o muy pequeño, puede no tener solución única.")
            continue

        # Mostrar pivote
        if mostrar_pivotes:
            print(f"Pivote encontrado en fila {i+1}, columna {i+1}: {format_num(pivote)}")

        # Normalizar fila para hacer pivote 1
        factor = 1 / pivote
        M[i] = [x * factor for x in M[i]]
        if mostrar_pasos:
            print(f"\nPaso {paso}. Normalizar pivote de F{i+1} (col. {i+1}):")
            print(f"F{i+1} <- (1/{format_num(pivote)}) * F{i+1}")
            print_matrix_with_format(format_matrix(M))
            paso += 1

        # Limpiar columna i arriba y abajo
        for j in range(filas):
            if j != i:
                factor = M[j][i]
                if abs(factor) > 1e-12:
                    M[j] = [M[j][k] - factor * M[i][k] for k in range(columnas)]
                    if mostrar_pasos:
                        op_sign = "-" if factor > 0 else "+"
                        factor_abs = abs(factor)
                        print(f"\nPaso {paso}. Limpiar columna {i+1} en fila {j+1}:")
                        print(f"F{j+1} <- F{j+1} {op_sign} {format_num(factor_abs)} * F{i+1}")
                        print_matrix_with_format(format_matrix(M))
                        paso += 1

    # Extraer solución
    x = []
    for i in range(filas):
        x.append(round(M[i][-1], 2))

    return x

def matriz_rango(M):
    """
    Calcula el rango de una matriz M en forma escalonada.
    El rango es el número de filas no nulas.
    """
    rango = 0
    for fila in M:
        if any(abs(x) > 1e-12 for x in fila):
            rango += 1
    return rango
