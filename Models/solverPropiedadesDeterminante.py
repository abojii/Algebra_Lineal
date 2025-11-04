# Models/solverPropDeterminantes.py

def determinante_cofactores(matriz):
    """Calcula el determinante por cofactores de manera recursiva."""
    n = len(matriz)
    if n == 1:
        return matriz[0][0]
    if n == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
    
    det = 0
    for j in range(n):
        cofactor = (-1) ** j * matriz[0][j] * determinante_cofactores([fila[:j] + fila[j+1:] for fila in matriz[1:]])
        det += cofactor
    return det

def es_cero_fila_o_columna(matriz):
    pasos = "🔎 Paso a paso:\n"
    pasos += "Concepto: Si una fila o columna es nula (todos ceros), el determinante es cero porque la matriz no es invertible.\n\n"
    for i, fila in enumerate(matriz):
        pasos += f"→ Verificando fila {i+1}: {fila}\n"
        if all(x == 0 for x in fila):
            pasos += f"✅ Todos los elementos son 0 ⇒ fila {i+1} nula ⇒ det(A) = 0\n"
            return True, pasos
    for j in range(len(matriz[0])):
        columna = [fila[j] for fila in matriz]
        pasos += f"→ Verificando columna {j+1}: {columna}\n"
        if all(x == 0 for x in columna):
            pasos += f"✅ Todos los elementos son 0 ⇒ columna {j+1} nula ⇒ det(A) = 0\n"
            return True, pasos
    pasos += "❌ No se encontraron filas ni columnas nulas. El determinante podría no ser cero.\n"
    return False, pasos

def son_iguales_o_proporcionales(matriz):
    pasos = "🔎 Paso a paso:\n"
    pasos += "Concepto: Si dos filas son iguales o proporcionales, la matriz tiene filas linealmente dependientes, por lo que det(A) = 0.\n\n"
    n = len(matriz)
    for i in range(n):
        for j in range(i+1, n):
            fila1, fila2 = matriz[i], matriz[j]
            pasos += f"→ Comparando fila {i+1}: {fila1} con fila {j+1}: {fila2}\n"
            if fila1 == fila2:
                pasos += f"✅ Son iguales ⇒ filas dependientes ⇒ det(A) = 0\n"
                return True, pasos
            try:
                razones = [fila2[k]/fila1[k] if fila1[k] != 0 else None for k in range(n)]
                razones = [r for r in razones if r is not None]
                pasos += f"   Razones calculadas: {razones}\n"
                if len(set(razones)) == 1:
                    pasos += f"✅ Proporcionales (misma razón {set(razones).pop()}) ⇒ filas dependientes ⇒ det(A) = 0\n"
                    return True, pasos
            except ZeroDivisionError:
                continue
    pasos += "❌ No hay filas iguales ni proporcionales. El determinante podría no ser cero.\n"
    return False, pasos

def intercambio_signo(m_original, m_modificada):
    pasos = "🔎 Paso a paso:\n"
    pasos += "Concepto: Intercambiar dos filas cambia el signo del determinante (propiedad de antisimetría).\n\n"
    pasos += f"Matriz original:\n{mostrar_matriz(m_original)}\n"
    det_original = determinante_cofactores(m_original)
    pasos += f"Determinante original: det(A) = {det_original}\n\n"
    
    pasos += f"Matriz con filas intercambiadas:\n{mostrar_matriz(m_modificada)}\n"
    det_modificada = determinante_cofactores(m_modificada)
    pasos += f"Determinante modificada: det(A') = {det_modificada}\n\n"
    
    if det_modificada == -det_original:
        pasos += f"✅ Se cumple: det(A') = -det(A) ⇒ {det_modificada} = -{det_original}\n"
        return True, pasos
    else:
        pasos += f"❌ No se cumple: {det_modificada} ≠ -{det_original}\n"
        return False, pasos

def multiplicacion_escalar(matriz, k):
    pasos = "🔎 Paso a paso:\n"
    pasos += f"Concepto: Multiplicar una fila por escalar k hace que det(kA) = k^n × det(A), donde n es el tamaño.\n\n"
    n = len(matriz)
    pasos += f"Matriz original A:\n{mostrar_matriz(matriz)}\n"
    det_a = determinante_cofactores(matriz)
    pasos += f"Determinante original: det(A) = {det_a}\n\n"
    
    # Generar kA (multiplicar toda la matriz por k para simplicidad; ajusta si es solo una fila)
    ka = [[k * elem for elem in fila] for fila in matriz]
    pasos += f"Matriz escalada kA (k={k}):\n{mostrar_matriz(ka)}\n"
    det_ka = determinante_cofactores(ka)
    pasos += f"Determinante escalada: det(kA) = {det_ka}\n"
    esperado = k ** n * det_a
    pasos += f"Esperado: k^n × det(A) = {k}^{n} × {det_a} = {esperado}\n\n"
    
    if abs(det_ka - esperado) < 1e-6:  # Tolerancia para floats
        pasos += f"✅ Se cumple: det(kA) ≈ {esperado}\n"
        return True, pasos
    else:
        pasos += f"❌ No se cumple: {det_ka} ≠ {esperado}\n"
        return False, pasos

def propiedad_multiplicativa(a, b, det_func):
    pasos = "🔎 Paso a paso:\n"
    pasos += "Concepto: Para matrices cuadradas, det(AB) = det(A) × det(B).\n\n"
    pasos += f"→ Calculando det(A):\n"
    det_a = det_func(a)
    pasos += f"   det(A) = {det_a}\n"

    pasos += f"→ Calculando det(B):\n"
    det_b = det_func(b)
    pasos += f"   det(B) = {det_b}\n"

    pasos += f"→ Calculando AB:\n"
    ab = multiplicar_matrices(a, b)
    pasos += f"{mostrar_matriz(ab)}\n"

    pasos += f"→ Calculando det(AB):\n"
    det_ab = det_func(ab)
    pasos += f"   det(AB) = {det_ab}\n"

    if abs(det_ab - det_a * det_b) < 1e-6:  # Tolerancia
        pasos += f"✅ Se cumple: det(AB) = det(A) × det(B) ⇒ {det_ab} ≈ {det_a} × {det_b}\n"
        return True, pasos
    else:
        pasos += f"❌ No se cumple: {det_ab} ≠ {det_a} × {det_b} = {det_a * det_b}\n"
        return False, pasos

def suma_multiplo_fila(matriz, k, fila_origen, fila_destino):
    pasos = "🔎 Paso a paso:\n"
    pasos += "Concepto: Sumar un múltiplo de una fila a otra no cambia el determinante (operación elemental).\n\n"
    n = len(matriz)
    pasos += f"Matriz original A:\n{mostrar_matriz(matriz)}\n"
    det_a = determinante_cofactores(matriz)
    pasos += f"Determinante original: det(A) = {det_a}\n\n"
    
    # Generar nueva matriz: fila_destino += k * fila_origen
    nueva = [fila[:] for fila in matriz]
    for j in range(n):
        nueva[fila_destino][j] += k * matriz[fila_origen][j]
    
    pasos += f"Operación: Fila {fila_destino+1} ← Fila {fila_destino+1} + {k} × Fila {fila_origen+1}\n"
    pasos += f"Matriz modificada:\n{mostrar_matriz(nueva)}\n"
    det_nueva = determinante_cofactores(nueva)
    pasos += f"Determinante modificada: det(A') = {det_nueva}\n\n"
    
    if abs(det_nueva - det_a) < 1e-6:  # Tolerancia
        pasos += f"✅ Se cumple: det(A') = det(A) ⇒ {det_nueva} ≈ {det_a}\n"
        return True, pasos
    else:
        pasos += f"❌ No se cumple: {det_nueva} ≠ {det_a}\n"
        return False, pasos

def multiplicar_matrices(a, b):
    n = len(a)
    resultado = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                resultado[i][j] += a[i][k] * b[k][j]
    return resultado

def mostrar_matriz(m):
    return '\n'.join(['  ' + str(fila) for fila in m])