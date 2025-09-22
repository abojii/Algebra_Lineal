# vectores.py
# Operaciones en R^n: propiedades, combinación lineal y ecuación vectorial
import metodos

def leer_vector():
    entrada = input("Ingrese los componentes del vector separados por espacio: ")
    return [float(x) for x in entrada.split()]

def suma_vectores(u, v):
    return [u[i] + v[i] for i in range(len(u))]

def multiplicar_escalar(c, v):
    return [c * x for x in v]

def vector_cero(n):
    return [0] * n

def vector_opuesto(v):
    return [-x for x in v]

# -----------------------------
# 1. Propiedades algebraicas
# -----------------------------
def combinacion_lineal():
    print("\n=== Combinación lineal de vectores (DEBUG mejorado) ===")
    n = int(input("¿Cuántos vectores base ingresará? "))
    vectores = []
    for i in range(n):
        print(f"Vector base {i+1}:")
        v = leer_vector()
        vectores.append(v)

    objetivo = leer_vector()

    # Validar dimensiones
    dim = len(vectores[0])
    for i, v in enumerate(vectores):
        if len(v) != dim:
            print(f"Error: el vector {i+1} tiene dimensión {len(v)} distinta de {dim}.")
            return
    if len(objetivo) != dim:
        print(f"Error: el vector objetivo tiene dimensión {len(objetivo)} distinta de {dim}.")
        return

    # Construir matriz aumentada: cada fila corresponde a una componente (ecuación)
    M_aug = []
    for i in range(dim):
        fila = [vectores[j][i] for j in range(n)]  # coeficientes c1..cn en la ecuación i
        fila.append(objetivo[i])
        M_aug.append(fila)

    print("\nMatriz aumentada (cada fila = una ecuación):")
    for fila in M_aug:
        print(fila)

    # Llamada al solucionador general (tu metodos.gauss_jordan_general)
    solucion = metodos.gauss_jordan_general(M_aug, mostrar_pasos=True, mostrar_pivotes=False)

    if not solucion:
        print("\n❌ No se encontró solución (o el método devolvió lista vacía/None).")
        return

    print("\nCoeficientes encontrados:", solucion)

    # Verificar reconstrucción: b_recon = sum(ci * v_i)
    b_recon = [0.0] * dim
    for j, c in enumerate(solucion):
        for i in range(dim):
            b_recon[i] += c * vectores[j][i]

    # Mostrar verificación
    print("\nVector objetivo:", objetivo)
    print("Vector reconstruido a partir de los coeficientes:", [round(x, 6) for x in b_recon])

    # Comparar con tolerancia
    tol = 1e-6
    if all(abs(b_recon[i] - objetivo[i]) <= tol for i in range(dim)):
        print("\n✅ Verificación OK: el vector objetivo SÍ es combinación lineal.")
    else:
        print("\n❌ La solución NO reconstruye exactamente el objetivo. Datos de depuración:")
        print(" - Aumentada usada:", M_aug)
        print(" - Coeficientes:", solucion)
        print(" - Vector reconstruido:", b_recon)
        print("Comprueba orden de vectores (cada vector base debe ingresarse como columna).")

# -----------------------------
# 3. Ecuación vectorial
# -----------------------------
def ecuacion_vectorial():
    print("\n=== Ecuación vectorial ===")
    n = int(input("¿Cuántos vectores v ingresará? "))
    vectores = [leer_vector() for _ in range(n)]
    b = leer_vector()

    # Construir matriz aumentada
    M_aug = []
    for i in range(len(vectores[0])):
        fila = [vectores[j][i] for j in range(n)]
        fila.append(b[i])
        M_aug.append(fila)

    print("\nMatriz aumentada del sistema:")
    for fila in M_aug:
        print(fila)

    solucion = metodos.gauss_jordan_general(M_aug, mostrar_pasos=True, mostrar_pivotes=False)

    if solucion:
        print("\n✅ La ecuación vectorial tiene solución.")
        print("Coeficientes:", solucion)
    else:
        print("\n❌ La ecuación vectorial no tiene solución.")

# -----------------------------
# Menú principal de vectores
# -----------------------------
def menu_vectores():
    while True:
        print("\n===== OPERACIONES EN R^n =====")
        print("1. Verificar propiedades algebraicas")
        print("2. Combinación lineal de vectores")
        print("3. Ecuación vectorial")
        print("4. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # verificar_propiedades()  # Función no definida
            print("Función 'verificar_propiedades' no implementada.")
        elif opcion == "2":
            combinacion_lineal()
        elif opcion == "3":
            ecuacion_vectorial()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")