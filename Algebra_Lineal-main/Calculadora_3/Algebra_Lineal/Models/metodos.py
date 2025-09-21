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

def escalonada_matriz(M_aug, mostrar_pasos=True, mostrar_pivotes=False, tol=1e-12):
    """
    Convierte la matriz aumentada a forma escalonada (FE) con pivotado parcial.
    Maneja columnas con todos ceros avanzando de columna sin perder la fila actual.
    """
    M = copy.deepcopy(M_aug)
    m = len(M)
    n = len(M[0]) - 1  # número de variables
    paso = 1
    fila = 0
    col = 0

    while fila < m and col < n:
        # Buscar pivote (máximo absoluto) en la columna col, desde 'fila' hacia abajo
        piv = max(range(fila, m), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) <= tol:
            # Columna sin pivote (toda ~0): avanza de columna
            col += 1
            continue

        # Intercambio si hace falta
        if piv != fila:
            M[fila], M[piv] = M[piv], M[fila]
            if mostrar_pasos:
                print(f"Paso {paso}: Intercambio de filas {fila+1} y {piv+1}")
                print_matrix_with_format(format_matrix(M))
                paso += 1

        if mostrar_pivotes:
            print(f"Pivote encontrado en fila {fila+1}, columna {col+1}: {format_num(M[fila][col])}")

        # Eliminación hacia abajo
        for r in range(fila + 1, m):
            if abs(M[r][col]) <= tol:
                continue
            factor = M[r][col] / M[fila][col]
            for j in range(col, n + 1):
                M[r][j] -= factor * M[fila][j]
            if mostrar_pasos:
                print(f"Paso {paso}: Eliminación en fila {r+1} usando fila {fila+1} (factor: {format_num(factor)})")
                print_matrix_with_format(format_matrix(M))
                paso += 1

        fila += 1
        col += 1

    return M

def escalonada_reducida_matriz(M_aug, mostrar_pasos=True, mostrar_pivotes=False, tol=1e-12):
    """
    Convierte la matriz aumentada a forma escalonada reducida (FER) usando Gauss-Jordan,
    apoyándose en FE y detectando la columna pivote real de cada fila.
    """
    M = escalonada_matriz(M_aug, mostrar_pasos=mostrar_pasos, mostrar_pivotes=mostrar_pivotes, tol=tol)
    m = len(M)
    n = len(M[0]) - 1  # número de variables

    # Recorremos de abajo arriba
    for i in range(m - 1, -1, -1):
        # Buscar la primera columna no nula de la fila i (columna pivote de la fila)
        lead = None
        for j in range(n):
            if abs(M[i][j]) > tol:
                lead = j
                break
        if lead is None:
            continue  # fila completamente nula

        # Normalizar pivote a 1
        pivote = M[i][lead]
        if abs(pivote - 1.0) > tol:
            for j in range(lead, n + 1):
                M[i][j] /= pivote
            if mostrar_pasos:
                print(f"Normalizar fila {i+1} (dividir por {format_num(pivote)})")
                print_matrix_with_format(format_matrix(M))

        # Eliminar hacia arriba en la columna 'lead'
        for k in range(i - 1, -1, -1):
            factor = M[k][lead]
            if abs(factor) <= tol:
                continue
            for j in range(lead, n + 1):
                M[k][j] -= factor * M[i][j]
            if mostrar_pasos:
                print(f"Eliminación hacia arriba en fila {k+1} usando fila {i+1} (factor: {format_num(factor)})")
                print_matrix_with_format(format_matrix(M))

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

DECIMALES_DEF = 2  # cambia a 3 o 4 si quieres más decimales

def format_num(num, decimales=DECIMALES_DEF, zero_tol=1e-12):
    # Normaliza casi-ceros y evita '-0.00'
    if isinstance(num, (int, float)) and abs(num) < zero_tol:
        num = 0.0
    s = f"{float(num):.{decimales}f}"
    if s.startswith("-0."):
        s = s[1:]  # "-0.00" -> "0.00"
    return s

def format_matrix(M, decimales=DECIMALES_DEF, zero_tol=1e-12):
    return [[format_num(x, decimales, zero_tol) for x in fila] for fila in M]

def print_matrix_with_format(M_fmt):
    # M_fmt debe venir ya como strings formateadas (p. ej. format_matrix)
    cols = len(M_fmt[0])
    widths = [max(len(str(M_fmt[i][j])) for i in range(len(M_fmt))) for j in range(cols)]
    for fila in M_fmt:
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
# ojo piojo 
def _nombre_variables(n):
    return [f"x{j+1}" for j in range(n)]

def detectar_pivotes(R, n_vars, tol=1e-10):
    """
    Dada una matriz R (ya en FE o FER) de tamaño m x (n_vars+1),
    devuelve (pivot_cols, free_cols) por índice (0-basado).
    Estrategia: en cada fila, el primer coeficiente no ~0 en las primeras n_vars columnas
    marca una columna pivote.
    """
    pivot_cols = []
    for i in range(len(R)):
        for j in range(n_vars):
            if abs(R[i][j]) > tol:
                pivot_cols.append(j)
                break
    pivot_cols = sorted(set(pivot_cols))
    free_cols = [j for j in range(n_vars) if j not in pivot_cols]
    return pivot_cols, free_cols

def rango_coef_y_aumentada(R, n_vars, tol=1e-10):
    """
    Calcula:
      - rank(A): número de filas no nulas considerando solo las primeras n_vars columnas
      - rank([A|b]): número de filas no nulas considerando todas las columnas
    Supone que R es FE o FER (pero también funciona razonablemente si no lo es).
    """
    def fila_no_nula(row, cols):
        return any(abs(row[j]) > tol for j in cols)

    rank_A = 0
    rank_Aug = 0
    m = len(R)
    for i in range(m):
        if fila_no_nula(R[i], range(n_vars)):
            rank_A += 1
        if fila_no_nula(R[i], range(n_vars + 1)):
            rank_Aug += 1
    return rank_A, rank_Aug

def clasificar_sistema(R, n_vars, tol=1e-10):
    """
    Usa Rouché–Capelli con la matriz ya reducida R (FE o FER).
    Devuelve cadena: 'Única solución', 'Infinitas soluciones' o 'No tiene solución'.
    """
    # Chequeo inmediato de inconsistencia: [0 0 ... 0 | b] con b != 0
    for i in range(len(R)):
        if all(abs(R[i][j]) < tol for j in range(n_vars)) and abs(R[i][-1]) > tol:
            return "No tiene solución"

    rank_A, rank_Aug = rango_coef_y_aumentada(R, n_vars, tol)
    if rank_A != rank_Aug:
        return "No tiene solución"
    if rank_A == n_vars:
        return "Única solución"
    return "Infinitas soluciones"

def _imprime_listado_vars(indices, nombres):
    if not indices:
        return "—"
    return ", ".join(nombres[j] for j in indices)

def diagnostico_sistema(M_aug, forma="reducida", nombres=None, mostrar_pasos=True, tol=1e-10, mostrar_rangos=False):
    """
    Ejecuta FE o FER y muestra:
      - Variables pivote
      - Variables libres
      - Clasificación (única / infinitas / no tiene solución)
    NOTA: Los rangos NO se imprimen a menos que mostrar_rangos=True.
    """
    n_vars = len(M_aug[0]) - 1
    if nombres is None:
        nombres = [f"x{j+1}" for j in range(n_vars)]

    if forma.lower() in ("reducida", "fer"):
        R = escalonada_reducida_matriz(M_aug, mostrar_pasos=mostrar_pasos, mostrar_pivotes=False)
        etiqueta_forma = "Forma Escalonada Reducida (FER)"
    elif forma.lower() in ("escalonada", "fe"):
        R = escalonada_matriz(M_aug, mostrar_pasos=mostrar_pasos, mostrar_pivotes=False)
        etiqueta_forma = "Forma Escalonada (FE)"
    else:
        raise ValueError("forma debe ser 'reducida' (FER) o 'escalonada' (FE)")

    # Detectar pivotes y libres
    pivot_cols, free_cols = detectar_pivotes(R, n_vars, tol=tol)
    tipo = clasificar_sistema(R, n_vars, tol=tol)

    # Rangos (se calculan para el return; se imprimen solo si mostrar_rangos=True)
    rank_A, rank_Aug = rango_coef_y_aumentada(R, n_vars, tol=tol)

    # Imprimir resumen (SIN ranks por defecto)
    print("\n================ RESUMEN  ========================")
    print(f"Forma usada: {etiqueta_forma}")
    print(f"Variables pivote: {', '.join(nombres[j] for j in pivot_cols) if pivot_cols else '—'}")
    print(f"Variables libres: {', '.join(nombres[j] for j in free_cols) if free_cols else '—'}")
    print(f"Clasificación : {tipo}")
    if mostrar_rangos:
        print(f"rank(A) = {rank_A}, rank([A|b]) = {rank_Aug}, n = {n_vars}")
    print("=====================================================\n")

    return {
        "forma": etiqueta_forma,
        "matriz_final": R,
        "pivot_cols": pivot_cols,
        "free_cols": free_cols,
        "vars_pivote": [nombres[j] for j in pivot_cols],
        "vars_libres": [nombres[j] for j in free_cols],
        "tipo": tipo,
        "rank_A": rank_A,
        "rank_Aug": rank_Aug,
        "n_vars": n_vars,
    }