# vector_space_properties.py
# Paquete de funciones para verificar propiedades algebraicas de espacios vectoriales
# Asume matrices como listas de listas, escalares como float

def matrix_equal(m1, m2, tol=1e-10):
    if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
        return False
    for i in range(len(m1)):
        for j in range(len(m1[0])):
            if abs(m1[i][j] - m2[i][j]) > tol:
                return False
    return True

def add_matrices(m1, m2):
    return [[m1[i][j] + m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))]

def scalar_mult(scalar, m):
    return [[scalar * m[i][j] for j in range(len(m[0]))] for i in range(len(m))]

def zero_matrix(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def verify_a(A, B):
    """
    Verifica a) A + B = B + A
    Parámetros: A, B (matrices del mismo tamaño)
    Retorna: (cumple: bool, pasos: str)
    """
    steps = "**Verificando propiedad: a) A + B = B + A**\n\n"
    steps += f"- Matriz A: {A}\n"
    steps += f"- Matriz B: {B}\n\n"
    
    steps += "**Cálculo de A + B (izquierda):**\n"
    left = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = A[i][j] + B[i][j]
            steps += f"  A[{i}][{j}] + B[{i}][{j}] = {A[i][j]} + {B[i][j]} = {val}\n"
            row.append(val)
        left.append(row)
    steps += f"Resultado: {left}\n\n"
    
    steps += "**Cálculo de B + A (derecha):**\n"
    right = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = B[i][j] + A[i][j]
            steps += f"  B[{i}][{j}] + A[{i}][{j}] = {B[i][j]} + {A[i][j]} = {val}\n"
            row.append(val)
        right.append(row)
    steps += f"Resultado: {right}\n\n"
    
    cumple = matrix_equal(left, right)
    steps += f"**Comparación:**\n"
    steps += f"- Izquierda: {left}\n"
    steps += f"- Derecha: {right}\n"
    steps += f"- {'Cumple' if cumple else 'No cumple'}\n"
    return cumple, steps

def verify_b(A, B, C):
    """
    Verifica b) (A + B) + C = A + (B + C)
    Parámetros: A, B, C (matrices del mismo tamaño)
    Retorna: (cumple: bool, pasos: str)
    """
    steps = "**Verificando propiedad: b) (A + B) + C = A + (B + C)**\n\n"
    steps += f"- Matriz A: {A}\n"
    steps += f"- Matriz B: {B}\n"
    steps += f"- Matriz C: {C}\n\n"
    
    steps += "**Cálculo de A + B (primer paso):**\n"
    AB = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = A[i][j] + B[i][j]
            steps += f"  A[{i}][{j}] + B[{i}][{j}] = {A[i][j]} + {B[i][j]} = {val}\n"
            row.append(val)
        AB.append(row)
    steps += f"Resultado A + B: {AB}\n\n"
    
    steps += "**Cálculo de (A + B) + C (izquierda):**\n"
    left = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = AB[i][j] + C[i][j]
            steps += f"  (A+B)[{i}][{j}] + C[{i}][{j}] = {AB[i][j]} + {C[i][j]} = {val}\n"
            row.append(val)
        left.append(row)
    steps += f"Resultado: {left}\n\n"
    
    steps += "**Cálculo de B + C (primer paso):**\n"
    BC = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = B[i][j] + C[i][j]
            steps += f"  B[{i}][{j}] + C[{i}][{j}] = {B[i][j]} + {C[i][j]} = {val}\n"
            row.append(val)
        BC.append(row)
    steps += f"Resultado B + C: {BC}\n\n"
    
    steps += "**Cálculo de A + (B + C) (derecha):**\n"
    right = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = A[i][j] + BC[i][j]
            steps += f"  A[{i}][{j}] + (B+C)[{i}][{j}] = {A[i][j]} + {BC[i][j]} = {val}\n"
            row.append(val)
        right.append(row)
    steps += f"Resultado: {right}\n\n"
    
    cumple = matrix_equal(left, right)
    steps += f"**Comparación:**\n"
    steps += f"- Izquierda: {left}\n"
    steps += f"- Derecha: {right}\n"
    steps += f"- {'Cumple' if cumple else 'No cumple'}\n"
    return cumple, steps

def verify_c(A):
    """
    Verifica c) A + 0 = A
    Parámetros: A (matriz)
    Retorna: (cumple: bool, pasos: str)
    """
    rows, cols = len(A), len(A[0])
    zero = zero_matrix(rows, cols)
    steps = "**Verificando propiedad: c) A + 0 = A**\n\n"
    steps += f"- Matriz A: {A}\n"
    steps += f"- Matriz cero (0): {zero}\n\n"
    
    steps += "**Cálculo de A + 0 (izquierda):**\n"
    left = []
    for i in range(rows):
        row = []
        for j in range(cols):
            val = A[i][j] + 0
            steps += f"  A[{i}][{j}] + 0 = {A[i][j]} + 0 = {val}\n"
            row.append(val)
        left.append(row)
    steps += f"Resultado: {left}\n\n"
    
    right = A
    steps += f"**Derecha (A):** {right}\n\n"
    
    cumple = matrix_equal(left, right)
    steps += f"**Comparación:**\n"
    steps += f"- Izquierda: {left}\n"
    steps += f"- Derecha: {right}\n"
    steps += f"- {'Cumple' if cumple else 'No cumple'}\n"
    return cumple, steps

def verify_d(A, B, r):
    """
    Verifica d) r(A + B) = rA + rB
    Parámetros: A, B (matrices del mismo tamaño), r (escalar)
    Retorna: (cumple: bool, pasos: str)
    """
    steps = "**Verificando propiedad: d) r(A + B) = rA + rB**\n\n"
    steps += f"- Matriz A: {A}\n"
    steps += f"- Matriz B: {B}\n"
    steps += f"- Escalar r: {r}\n\n"
    
    steps += "**Cálculo de A + B (primer paso):**\n"
    AB = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = A[i][j] + B[i][j]
            steps += f"  A[{i}][{j}] + B[{i}][{j}] = {A[i][j]} + {B[i][j]} = {val}\n"
            row.append(val)
        AB.append(row)
    steps += f"Resultado A + B: {AB}\n\n"
    
    steps += "**Cálculo de r(A + B) (izquierda):**\n"
    left = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = r * AB[i][j]
            steps += f"  r * (A+B)[{i}][{j}] = {r} * {AB[i][j]} = {val}\n"
            row.append(val)
        left.append(row)
    steps += f"Resultado: {left}\n\n"
    
    steps += "**Cálculo de rA (primer paso):**\n"
    rA = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = r * A[i][j]
            steps += f"  r * A[{i}][{j}] = {r} * {A[i][j]} = {val}\n"
            row.append(val)
        rA.append(row)
    steps += f"Resultado rA: {rA}\n\n"
    
    steps += "**Cálculo de rB (segundo paso):**\n"
    rB = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = r * B[i][j]
            steps += f"  r * B[{i}][{j}] = {r} * {B[i][j]} = {val}\n"
            row.append(val)
        rB.append(row)
    steps += f"Resultado rB: {rB}\n\n"
    
    steps += "**Cálculo de rA + rB (derecha):**\n"
    right = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = rA[i][j] + rB[i][j]
            steps += f"  rA[{i}][{j}] + rB[{i}][{j}] = {rA[i][j]} + {rB[i][j]} = {val}\n"
            row.append(val)
        right.append(row)
    steps += f"Resultado: {right}\n\n"
    
    cumple = matrix_equal(left, right)
    steps += f"**Comparación:**\n"
    steps += f"- Izquierda: {left}\n"
    steps += f"- Derecha: {right}\n"
    steps += f"- {'Cumple' if cumple else 'No cumple'}\n"
    return cumple, steps

def verify_e(A, r, s):
    """
    Verifica e) (r + s)A = rA + sA
    Parámetros: A (matriz), r, s (escalares)
    Retorna: (cumple: bool, pasos: str)
    """
    steps = "**Verificando propiedad: e) (r + s)A = rA + sA**\n\n"
    steps += f"- Matriz A: {A}\n"
    steps += f"- Escalar r: {r}\n"
    steps += f"- Escalar s: {s}\n\n"
    
    steps += "**Cálculo de (r + s)A (izquierda):**\n"
    rs = r + s
    steps += f"Primero, r + s = {r} + {s} = {rs}\n"
    left = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = rs * A[i][j]
            steps += f"  (r+s) * A[{i}][{j}] = {rs} * {A[i][j]} = {val}\n"
            row.append(val)
        left.append(row)
    steps += f"Resultado: {left}\n\n"
    
    steps += "**Cálculo de rA (primer paso):**\n"
    rA = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = r * A[i][j]
            steps += f"  r * A[{i}][{j}] = {r} * {A[i][j]} = {val}\n"
            row.append(val)
        rA.append(row)
    steps += f"Resultado rA: {rA}\n\n"
    
    steps += "**Cálculo de sA (segundo paso):**\n"
    sA = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = s * A[i][j]
            steps += f"  s * A[{i}][{j}] = {s} * {A[i][j]} = {val}\n"
            row.append(val)
        sA.append(row)
    steps += f"Resultado sA: {sA}\n\n"
    
    steps += "**Cálculo de rA + sA (derecha):**\n"
    right = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = rA[i][j] + sA[i][j]
            steps += f"  rA[{i}][{j}] + sA[{i}][{j}] = {rA[i][j]} + {sA[i][j]} = {val}\n"
            row.append(val)
        right.append(row)
    steps += f"Resultado: {right}\n\n"
    
    cumple = matrix_equal(left, right)
    steps += f"**Comparación:**\n"
    steps += f"- Izquierda: {left}\n"
    steps += f"- Derecha: {right}\n"
    steps += f"- {'Cumple' if cumple else 'No cumple'}\n"
    return cumple, steps

def verify_f(A, r, s):
    """
    Verifica f) r(sA) = (rs)A
    Parámetros: A (matriz), r, s (escalares)
    Retorna: (cumple: bool, pasos: str)
    """
    steps = "**Verificando propiedad: f) r(sA) = (rs)A**\n\n"
    steps += f"- Matriz A: {A}\n"
    steps += f"- Escalar r: {r}\n"
    steps += f"- Escalar s: {s}\n\n"
    
    steps += "**Cálculo de sA (primer paso):**\n"
    sA = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = s * A[i][j]
            steps += f"  s * A[{i}][{j}] = {s} * {A[i][j]} = {val}\n"
            row.append(val)
        sA.append(row)
    steps += f"Resultado sA: {sA}\n\n"
    
    steps += "**Cálculo de r(sA) (izquierda):**\n"
    left = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = r * sA[i][j]
            steps += f"  r * sA[{i}][{j}] = {r} * {sA[i][j]} = {val}\n"
            row.append(val)
        left.append(row)
    steps += f"Resultado: {left}\n\n"
    
    steps += "**Cálculo de (rs)A (derecha):**\n"
    rs = r * s
    steps += f"Primero, r * s = {r} * {s} = {rs}\n"
    right = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            val = rs * A[i][j]
            steps += f"  (r*s) * A[{i}][{j}] = {rs} * {A[i][j]} = {val}\n"
            row.append(val)
        right.append(row)
    steps += f"Resultado: {right}\n\n"
    
    cumple = matrix_equal(left, right)
    steps += f"**Comparación:**\n"
    steps += f"- Izquierda: {left}\n"
    steps += f"- Derecha: {right}\n"
    steps += f"- {'Cumple' if cumple else 'No cumple'}\n"
    return cumple, steps
