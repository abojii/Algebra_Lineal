#sistema_ecuaciones.py
from copy import deepcopy 

def formatear_matriz(A, b):
    """Devuelve un string con la matriz aumentada A|b formateada."""
    filas = []
    for i in range(len(A)):
        fila = " ".join(f"{A[i][j]:6.2f}" for j in range(len(A[0])))
        fila += " | " + f"{b[i]:6.2f}"
        filas.append("[ " + fila + " ]")
    return "\n".join(filas)

def clasificar_sistema(A, b):
    """Clasifica el sistema en única solución, infinitas o ninguna solución."""
    n = len(A)
    m = len(A[0])
    Ab = [A[i] + [b[i]] for i in range(n)]  # Matriz aumentada

    def rango(matriz):
        M = deepcopy(matriz)
        filas = len(M)
        cols = len(M[0])
        r = 0
        for j in range(cols):
            pivote = None
            for i in range(r, filas):
                if abs(M[i][j]) > 1e-10:
                    pivote = i
                    break
            if pivote is not None:
                M[r], M[pivote] = M[pivote], M[r]
                piv = M[r][j]
                M[r] = [x / piv for x in M[r]]
                for i in range(filas):
                    if i != r and abs(M[i][j]) > 1e-10:
                        factor = M[i][j]
                        M[i] = [M[i][k] - factor * M[r][k] for k in range(cols)]
                r += 1
        return r

    rango_A = rango(A)
    rango_Ab = rango(Ab)

    if rango_A < rango_Ab:
        return "Inconsistente (sin solución)"
    elif rango_A == rango_Ab == m:
        return "Consistente: única solución"
    elif rango_A == rango_Ab < m:
        return "Consistente: infinitas soluciones"
    else:
        return "Clasificación no determinada"


def gauss(A, b):
    """Eliminación Gaussiana con paso a paso y clasificación."""
    A = deepcopy(A)
    b = deepcopy(b)
    n = len(A)
    pasos = []

    pasos.append("=== Eliminación Gaussiana ===")
    pasos.append("Matriz inicial (A|b):")
    pasos.append(formatear_matriz(A, b))

    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if abs(A[max_row][i]) < 1e-10:
            pasos.append(f"No se encontró pivote válido en columna {i+1}")
            continue

        if i != max_row:
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            pasos.append(f"↔ Intercambio fila {i+1} con fila {max_row+1}")
            pasos.append(formatear_matriz(A, b))

        pivote = A[i][i]
        pasos.append(f"Pivote en posición ({i+1},{i+1}) = {pivote:.2f}")

        for j in range(i+1, n):
            factor = A[j][i] / pivote
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
            pasos.append(f"F{j+1} = F{j+1} - ({factor:.2f})*F{i+1}")
            pasos.append(formatear_matriz(A, b))

    x = [0 for _ in range(n)]
    for i in reversed(range(n)):
        suma = sum(A[i][j] * x[j] for j in range(i+1, n))
        if abs(A[i][i]) < 1e-10:
            if abs(b[i] - suma) > 1e-10:
                pasos.append(f"Inconsistencia detectada en fila {i+1}")
                tipo, vb, vl = analizar_variables(A, b)
                pasos.append(f"\nSistema: {tipo}")
                pasos.append(f"Variables básicas: {', '.join(vb)}")
                pasos.append(f"Variables libres: {', '.join(vl)}")
                return pasos, None, tipo
            else:
                pasos.append(f"Fila {i+1} dependiente → Infinitas soluciones")
                tipo, vb, vl = analizar_variables(A, b)
                pasos.append(f"\nSistema: {tipo}")
                pasos.append(f"Variables básicas: {', '.join(vb)}")
                pasos.append(f"Variables libres: {', '.join(vl)}")
                return pasos, None, tipo
        x[i] = (b[i] - suma) / A[i][i]
        pasos.append(f"x{i+1} = {x[i]:.2f}")

    tipo, vb, vl = analizar_variables(A, b)
    pasos.append(f"\nSistema: {tipo}")
    pasos.append(f"Variables básicas: {', '.join(vb)}")
    pasos.append(f"Variables libres: {', '.join(vl)}")

    return pasos, x, tipo

   
def gauss_jordan(A, b):
    """Eliminación Gauss-Jordan con paso a paso."""
    A = deepcopy(A)
    b = deepcopy(b)
    n = len(A)
    pasos = []

    pasos.append("=== Eliminación Gauss-Jordan ===")
    pasos.append("Matriz inicial (A|b):")
    pasos.append(formatear_matriz(A, b))

    for i in range(n):
        pivote = A[i][i]
        if abs(pivote) < 1e-10:
            pasos.append(f"No se encontró pivote válido en columna {i+1}")
            continue

        for j in range(n):
            A[i][j] /= pivote
        b[i] /= pivote
        pasos.append(f"Normalizar F{i+1} → pivote ({i+1},{i+1}) = 1")
        pasos.append(formatear_matriz(A, b))

        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
                pasos.append(f"F{k+1} = F{k+1} - ({factor:.2f})*F{i+1}")
                pasos.append(formatear_matriz(A, b))

    tipo, vb, vl = analizar_variables(A, b)
    pasos.append(f"\nSistema: {tipo}")
    pasos.append(f"Variables básicas: {', '.join(vb)}")
    pasos.append(f"Variables libres: {', '.join(vl)}")

    return pasos, b, tipo
    




def forma_escalonada(A, b):
    """Forma escalonada con paso a paso."""
    pasos, _, clasificacion = gauss(A, b)
    return pasos, None, clasificacion


def forma_escalonada_reducida(A, b):
    """Forma escalonada reducida con paso a paso."""
    pasos, _, clasificacion = gauss_jordan(A, b)
    return pasos, None, clasificacion


def analizar_variables(A, b):
    """
    Determina variables básicas y libres, consistencia y tipo de solución.
    """
    n = len(A)
    m = len(A[0])  # número de variables
    Ab = [A[i] + [b[i]] for i in range(n)]  # matriz aumentada

    # Convertimos a forma escalonada para contar pivotes
    M = deepcopy(Ab)
    filas = len(M)
    cols = len(M[0])
    r = 0
    posiciones_pivote = []

    for j in range(cols - 1):  # excluye columna de términos independientes
        pivote = None
        for i in range(r, filas):
            if abs(M[i][j]) > 1e-10:
                pivote = i
                break
        if pivote is not None:
            M[r], M[pivote] = M[pivote], M[r]
            factor = M[r][j]
            M[r] = [x / factor for x in M[r]]
            for i in range(filas):
                if i != r and abs(M[i][j]) > 1e-10:
                    f = M[i][j]
                    M[i] = [M[i][k] - f * M[r][k] for k in range(cols)]
            posiciones_pivote.append(j)
            r += 1

    # Determinar consistencia
    inconsistente = False
    for fila in M:
        if all(abs(x) < 1e-10 for x in fila[:-1]) and abs(fila[-1]) > 1e-10:
            inconsistente = True
            break

    if inconsistente:
        tipo = "Inconsistente (sin solución)"
        vb = []
        vl = [f"x{i+1}" for i in range(m)]
    else:
        if len(posiciones_pivote) == m:
            tipo = "Consistente: única solución"
        else:
            tipo = "Consistente: infinitas soluciones"
        vb = [f"x{i+1}" for i in posiciones_pivote]
        vl = [f"x{i+1}" for i in range(m) if i not in posiciones_pivote]

    return tipo, vb, vl

