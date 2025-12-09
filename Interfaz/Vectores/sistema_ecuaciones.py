import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np  # Para operaciones matriciales eficientes

COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

# sistema_ecuaciones.py

def formatear_matriz(A, b):
    """Devuelve un string con la matriz aumentada A|b formateada."""
    A_list = A.tolist() if isinstance(A, np.ndarray) else A
    b_list = b.tolist() if isinstance(b, np.ndarray) else b
    filas = []
    for i in range(len(A_list)):
        fila = " ".join(f"{A_list[i][j]:6.2f}" for j in range(len(A_list[0])))
        fila += " | " + f"{b_list[i]:6.2f}"
        filas.append("[ " + fila + " ]")
    return "\n".join(filas)

def clasificar_sistema(A, b):
    """Clasifica el sistema usando rangos de NumPy."""
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    Ab = np.column_stack((A_np, b_np))
    rango_A = np.linalg.matrix_rank(A_np)
    rango_Ab = np.linalg.matrix_rank(Ab)
    m = A_np.shape[1]

    if rango_A < rango_Ab:
        return "Inconsistente (sin solución)"
    elif rango_A == rango_Ab == m:
        return "Consistente: única solución"
    elif rango_A == rango_Ab < m:
        return "Consistente: infinitas soluciones"
    else:
        return "Clasificación no determinada"

def gauss(A, b):
    """Eliminación Gaussiana con paso a paso. Soporta matrices no cuadradas."""
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    n, m = A_np.shape
    pasos = []

    pasos.append("=== Eliminación Gaussiana ===")
    pasos.append("Matriz inicial (A|b):")
    pasos.append(formatear_matriz(A_np, b_np))

    for i in range(min(n, m)):
        col_abs = np.abs(A_np[i:, i])
        max_row = np.argmax(col_abs) + i
        if col_abs[max_row - i] < 1e-10:
            pasos.append(f"No se encontró pivote válido en columna {i+1}")
            continue

        if i != max_row:
            A_np[[i, max_row]] = A_np[[max_row, i]]
            b_np[[i, max_row]] = b_np[[max_row, i]]
            pasos.append(f"↔ Intercambio fila {i+1} con fila {max_row+1}")
            pasos.append(formatear_matriz(A_np, b_np))

        pivote = A_np[i, i]
        pasos.append(f"Pivote en posición ({i+1},{i+1}) = {pivote:.2f}")

        for j in range(i+1, n):
            factor = A_np[j, i] / pivote
            A_np[j, i:] -= factor * A_np[i, i:]
            b_np[j] -= factor * b_np[i]
            pasos.append(f"F{j+1} = F{j+1} - ({factor:.2f})*F{i+1}")
            pasos.append(formatear_matriz(A_np, b_np))

    x = np.zeros(m) if m == n else None
    if m == n:
        for i in reversed(range(n)):
            suma = np.dot(A_np[i, i+1:], x[i+1:])
            if abs(A_np[i, i]) < 1e-10:
                if abs(b_np[i] - suma) > 1e-10:
                    pasos.append(f"Inconsistencia detectada en fila {i+1}")
                    tipo, vb, vl = analizar_variables(A_np, b_np)
                    pasos.append(f"\nSistema: {tipo}")
                    pasos.append(f"Variables básicas: {', '.join(vb)}")
                    pasos.append(f"Variables libres: {', '.join(vl)}")
                    return pasos, None, tipo
                else:
                    pasos.append(f"Fila {i+1} dependiente → Infinitas soluciones")
                    tipo, vb, vl = analizar_variables(A_np, b_np)
                    pasos.append(f"\nSistema: {tipo}")
                    pasos.append(f"Variables básicas: {', '.join(vb)}")
                    pasos.append(f"Variables libres: {', '.join(vl)}")
                    return pasos, None, tipo
            x[i] = (b_np[i] - suma) / A_np[i, i]
            pasos.append(f"x{i+1} = {x[i]:.2f}")

    tipo, vb, vl = analizar_variables(A_np, b_np)
    pasos.append(f"\nSistema: {tipo}")
    pasos.append(f"Variables básicas: {', '.join(vb)}")
    pasos.append(f"Variables libres: {', '.join(vl)}")

    return pasos, x.tolist() if x is not None else None, tipo

def gauss_jordan(A, b):
    """Eliminación Gauss-Jordan con paso a paso. Soporta matrices no cuadradas."""
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    n, m = A_np.shape
    pasos = []

    pasos.append("=== Eliminación Gauss-Jordan ===")
    pasos.append("Matriz inicial (A|b):")
    pasos.append(formatear_matriz(A_np, b_np))

    for i in range(min(n, m)):
        pivote = A_np[i, i]
        if abs(pivote) < 1e-10:
            pasos.append(f"No se encontró pivote válido en columna {i+1}")
            continue

        A_np[i, :] /= pivote
        b_np[i] /= pivote
        pasos.append(f"Normalizar F{i+1} → pivote ({i+1},{i+1}) = 1")
        pasos.append(formatear_matriz(A_np, b_np))

        for k in range(n):
            if k != i:
                factor = A_np[k, i]
                A_np[k, :] -= factor * A_np[i, :]
                b_np[k] -= factor * b_np[i]
                pasos.append(f"F{k+1} = F{k+1} - ({factor:.2f})*F{i+1}")
                pasos.append(formatear_matriz(A_np, b_np))

    tipo, vb, vl = analizar_variables(A_np, b_np)
    pasos.append(f"\nSistema: {tipo}")
    pasos.append(f"Variables básicas: {', '.join(vb)}")
    pasos.append(f"Variables libres: {', '.join(vl)}")

    return pasos, b_np.tolist(), tipo

def forma_escalonada(A, b):
    """Forma escalonada: Produce matriz triangular superior con encabezado y pivotes."""
    pasos, _, clasificacion = gauss(A, b)
    # Agregar encabezado y pivotes
    pasos.insert(0, "=== Método Escalonado ===")
    posiciones_pivote = calcular_posiciones_pivote(np.array(A, dtype=float), np.array(b, dtype=float))
    pasos.append(f"Pivotes en columnas: {', '.join(map(str, posiciones_pivote))}")
    return pasos, None, clasificacion

def forma_escalonada_reducida(A, b):
    """Forma escalonada reducida: Produce identidad con encabezado y pivotes."""
    pasos, _, clasificacion = gauss_jordan(A, b)
    # Agregar encabezado y pivotes
    pasos.insert(0, "=== Método Escalonado Reducido ===")
    posiciones_pivote = calcular_posiciones_pivote(np.array(A, dtype=float), np.array(b, dtype=float))
    pasos.append(f"Pivotes en columnas: {', '.join(map(str, posiciones_pivote))}")
    return pasos, None, clasificacion

def analizar_variables(A, b):
    """
    Determina variables básicas y libres usando eliminación completa.
    """
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    n, m = A_np.shape
    Ab = np.column_stack((A_np, b_np))

    # Eliminación para encontrar posiciones de pivote
    posiciones_pivote = []
    for j in range(m):
        for i in range(len(posiciones_pivote), n):
            if abs(Ab[i, j]) > 1e-10:
                # Normalizar y eliminar
                Ab[i, :] /= Ab[i, j]
                for k in range(n):
                    if k != i:
                        Ab[k, :] -= Ab[k, j] * Ab[i, :]
                posiciones_pivote.append(j + 1)  # +1 para numeración humana
                break

    rango_A = len(posiciones_pivote)
    rango_Ab = np.linalg.matrix_rank(Ab)

    inconsistente = rango_A < rango_Ab
    if inconsistente:
        tipo = "Inconsistente (sin solución)"
        vb = []
        vl = [f"x{i+1}" for i in range(m)]
    else:
        if rango_A == m:
            tipo = "Consistente: única solución"
        else:
            tipo = "Consistente: infinitas soluciones"
        vb = [f"x{p}" for p in posiciones_pivote]
        vl = [f"x{i+1}" for i in range(m) if (i+1) not in posiciones_pivote]

    return tipo, vb, vl

def calcular_posiciones_pivote(A, b):
    """Calcula posiciones de pivotes para mostrar en escalonados."""
    Ab = np.column_stack((A, b))
    posiciones = []
    for j in range(A.shape[1]):
        for i in range(len(posiciones), A.shape[0]):
            if abs(Ab[i, j]) > 1e-10:
                posiciones.append(j + 1)
                break
    return posiciones