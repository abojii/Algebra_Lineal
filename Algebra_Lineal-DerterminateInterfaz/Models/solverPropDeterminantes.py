# Models/solverPropDeterminantes.py

def es_cero_fila_o_columna(matriz):
    pasos = "🔎 Paso a paso:\n"
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
    pasos += "❌ No se encontraron filas ni columnas nulas.\n"
    return False, pasos


def son_iguales_o_proporcionales(matriz):
    pasos = "🔎 Paso a paso:\n"
    n = len(matriz)
    for i in range(n):
        for j in range(i+1, n):
            fila1, fila2 = matriz[i], matriz[j]
            pasos += f"→ Comparando fila {i+1}: {fila1} con fila {j+1}: {fila2}\n"
            if fila1 == fila2:
                pasos += f"✅ Son iguales ⇒ det(A) = 0\n"
                return True, pasos
            try:
                razones = [fila2[k]/fila1[k] if fila1[k] != 0 else None for k in range(n)]
                razones = [r for r in razones if r is not None]
                pasos += f"   Razones: {razones}\n"
                if len(set(razones)) == 1:
                    pasos += f"✅ Proporcionales (misma razón) ⇒ det(A) = 0\n"
                    return True, pasos
            except ZeroDivisionError:
                continue
    pasos += "❌ No hay filas iguales ni proporcionales.\n"
    return False, pasos


def intercambio_signo(m_original, m_modificada):
    pasos = "🔎 Paso a paso:\n"
    pasos += f"Matriz original:\n{mostrar_matriz(m_original)}\n"
    pasos += f"Matriz con filas intercambiadas:\n{mostrar_matriz(m_modificada)}\n"
    pasos += "✅ Al intercambiar dos filas, el determinante cambia de signo.\n"
    return True, pasos


def fila_por_escalar(original, escalada):
    pasos = "🔎 Paso a paso:\n"
    n = len(original)
    for i in range(n):
        try:
            razones = []
            for j in range(n):
                if original[i][j] != 0:
                    razon = escalada[i][j] / original[i][j]
                    razones.append(razon)
            pasos += f"→ Fila {i+1}: razón entre elementos originales y escalados: {razones}\n"
            if len(set(razones)) == 1 and razones:
                k = razones[0]
                pasos += f"✅ Fila {i+1} fue multiplicada por escalar k = {k}\n"
                pasos += f"⇒ det(kA) = k × det(A)\n"
                return True, pasos
        except ZeroDivisionError:
            continue
    pasos += "❌ No se detectó una fila multiplicada por escalar.\n"
    return False, pasos


def propiedad_multiplicativa(a, b, det_func):
    pasos = "🔎 Paso a paso:\n"
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

    if det_ab == det_a * det_b:
        pasos += f"✅ Se cumple: det(AB) = det(A) × det(B) ⇒ {det_ab} = {det_a} × {det_b}\n"
        return True, pasos
    else:
        pasos += f"❌ No se cumple: {det_ab} ≠ {det_a} × {det_b} = {det_a * det_b}\n"
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
