# matrix_transpose_properties.py
# Paquete de funciones para verificar propiedades de la transpuesta de matrices
# Asume matrices como listas de listas, escalares como float

def transpose(matrix):
    """Calcula la transpuesta de una matriz."""
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def add_matrices(m1, m2):
    return [[m1[i][j] + m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))]

def multiply_matrices(m1, m2):
    """Multiplica dos matrices (A x B)."""
    m = len(m1)
    n = len(m1[0])
    p = len(m2[0])
    result = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += m1[i][k] * m2[k][j]
    return result

def scalar_mult(scalar, m):
    return [[scalar * m[i][j] for j in range(len(m[0]))] for i in range(len(m))]

def matrix_equal(m1, m2, tol=1e-10):
    if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
        return False
    for i in range(len(m1)):
        for j in range(len(m1[0])):
            if abs(m1[i][j] - m2[i][j]) > tol:
                return False
    return True

def verify_transpose_double(A):
    """
    Verifica (A^T)^T = A
    Parámetros: A (matriz)
    Retorna: (cumple: bool, pasos: str)
    """
    steps = "**Verificando propiedad: (A^T)^T = A**\n\n"
    steps += f"- Matriz A: {A}\n\n"
    
    steps += "**Cálculo de A^T (transpuesta de A):**\n"
    AT = transpose(A)
    steps += f"A^T = {AT}\n\n"
    
    steps += "**Cálculo de (A^T)^T (transpuesta de A^T):**\n"
    ATT = transpose(AT)
    steps += f"(A^T)^T = {ATT}\n\n"
    
    right = A
    steps += f"**Derecha (A):** {right}\n\n"
    
    cumple = matrix_equal(ATT, right)
    steps += f"**Comparación:**\n"
    steps += f"- Izquierda: {ATT}\n"
    steps += f"- Derecha: {right}\n"
    steps += f"- {'Cumple' if cumple else 'No cumple'}\n"
    return cumple, steps

def verify_transpose_sum(A, B):
    """
    Verifica (A + B)^T = A^T + B^T
    Parámetros: A, B (matrices del mismo tamaño)
    Retorna: (cumple: bool, pasos: str)
    """
    steps = "**Verificando propiedad: (A + B)^T = A^T + B^T**\n\n"
    steps += f"- Matriz A: {A}\n"
    steps += f"- Matriz B: {B}\n\n"
    
    steps += "**Cálculo de A + B (primer paso):**\n"
    AB = add_matrices(A, B)
    steps += f"A + B = {AB}\n\n"
    
    steps += "**Cálculo de (A + B)^T (izquierda):**\n"
    left = transpose(AB)
    steps += f"(A + B)^T = {left}\n\n"
    
    steps += "**Cálculo de A^T (primer paso):**\n"
    AT = transpose(A)
    steps += f"A^T = {AT}\n\n"
    
    steps += "**Cálculo de B^T (segundo paso):**\n"
    BT = transpose(B)
    steps += f"B^T = {BT}\n\n"
    
    steps += "**Cálculo de A^T + B^T (derecha):**\n"
    right = add_matrices(AT, BT)
    steps += f"A^T + B^T = {right}\n\n"
    
    cumple = matrix_equal(left, right)
    steps += f"**Comparación:**\n"
    steps += f"- Izquierda: {left}\n"
    steps += f"- Derecha: {right}\n"
    steps += f"- {'Cumple' if cumple else 'No cumple'}\n"
    return cumple, steps

def verify_transpose_product(A, B):
    """
    Verifica (AB)^T = B^T A^T
    Parámetros: A, B (matrices compatibles para multiplicación)
    Retorna: (cumple: bool, pasos: str)
    """
    steps = "**Verificando propiedad: (AB)^T = B^T A^T**\n\n"
    steps += f"- Matriz A: {A}\n"
    steps += f"- Matriz B: {B}\n\n"
    
    steps += "**Cálculo de AB (primer paso):**\n"
    AB = multiply_matrices(A, B)
    steps += f"AB = {AB}\n\n"
    
    steps += "**Cálculo de (AB)^T (izquierda):**\n"
    left = transpose(AB)
    steps += f"(AB)^T = {left}\n\n"
    
    steps += "**Cálculo de A^T (primer paso):**\n"
    AT = transpose(A)
    steps += f"A^T = {AT}\n\n"
    
    steps += "**Cálculo de B^T (segundo paso):**\n"
    BT = transpose(B)
    steps += f"B^T = {BT}\n\n"
    
    steps += "**Cálculo de B^T A^T (derecha):**\n"
    right = multiply_matrices(BT, AT)
    steps += f"B^T A^T = {right}\n\n"
    
    cumple = matrix_equal(left, right)
    steps += f"**Comparación:**\n"
    steps += f"- Izquierda: {left}\n"
    steps += f"- Derecha: {right}\n"
    steps += f"- {'Cumple' if cumple else 'No cumple'}\n"
    return cumple, steps

def verify_transpose_scalar(A, k):
    """
    Verifica (kA)^T = k A^T
    Parámetros: A (matriz), k (escalar)
    Retorna: (cumple: bool, pasos: str)
    """
    steps = "**Verificando propiedad: (kA)^T = k A^T**\n\n"
    steps += f"- Matriz A: {A}\n"
    steps += f"- Escalar k: {k}\n\n"
    
    steps += "**Cálculo de kA (primer paso):**\n"
    kA = scalar_mult(k, A)
    steps += f"kA = {kA}\n\n"
    
    steps += "**Cálculo de (kA)^T (izquierda):**\n"
    left = transpose(kA)
    steps += f"(kA)^T = {left}\n\n"
    
    steps += "**Cálculo de A^T (primer paso):**\n"
    AT = transpose(A)
    steps += f"A^T = {AT}\n\n"
    
    steps += "**Cálculo de k A^T (derecha):**\n"
    right = scalar_mult(k, AT)
    steps += f"k A^T = {right}\n\n"
    
    cumple = matrix_equal(left, right)
    steps += f"**Comparación:**\n"
    steps += f"- Izquierda: {left}\n"
    steps += f"- Derecha: {right}\n"
    steps += f"- {'Cumple' if cumple else 'No cumple'}\n"
    return cumple, steps

def verify_transpose_scalar_sum(A, B, r):
    """
    Verifica (r(A + B))^T = r(A^T + B^T)
    Parámetros: A, B (matrices del mismo tamaño), r (escalar)
    Retorna: (cumple: bool, pasos: str)
    """
    steps = "**Verificando propiedad: (r(A + B))^T = r(A^T + B^T)**\n\n"
    steps += f"- Matriz A: {A}\n"
    steps += f"- Matriz B: {B}\n"
    steps += f"- Escalar r: {r}\n\n"
    
    steps += "**Cálculo de A + B (primer paso):**\n"
    AB = add_matrices(A, B)
    steps += f"A + B = {AB}\n\n"
    
    steps += "**Cálculo de r(A + B) (segundo paso):**\n"
    rAB = scalar_mult(r, AB)
    steps += f"r(A + B) = {rAB}\n\n"
    
    steps += "**Cálculo de (r(A + B))^T (izquierda):**\n"
    left = transpose(rAB)
    steps += f"(r(A + B))^T = {left}\n\n"
    
    steps += "**Cálculo de A^T (primer paso):**\n"
    AT = transpose(A)
    steps += f"A^T = {AT}\n\n"
    
    steps += "**Cálculo de B^T (segundo paso):**\n"
    BT = transpose(B)
    steps += f"B^T = {BT}\n\n"
    
    steps += "**Cálculo de A^T + B^T (tercer paso):**\n"
    ATBT = add_matrices(AT, BT)
    steps += f"A^T + B^T = {ATBT}\n\n"
    
    steps += "**Cálculo de r(A^T + B^T) (derecha):**\n"
    right = scalar_mult(r, ATBT)
    steps += f"r(A^T + B^T) = {right}\n\n"
    
    cumple = matrix_equal(left, right)
    steps += f"**Comparación:**\n"
    steps += f"- Izquierda: {left}\n"
    steps += f"- Derecha: {right}\n"
    steps += f"- {'Cumple' if cumple else 'No cumple'}\n"
    return cumple, steps