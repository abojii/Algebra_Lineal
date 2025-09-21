# Calculadora de sistema de ecuaciones lineales
# entrada.py
# Funciones para solicitar coeficientes de sistemas 2x2 y 3x3
def solicitar_coeficientes_2x2(return_ab: bool = False):

    print("Ingrese los coeficientes para el sistema 2x2:")
    a1 = float(input("a1 (coeficiente de x en la ecuación 1): "))
    b1 = float(input("b1 (coeficiente de y en la ecuación 1): "))
    c1 = float(input("c1 (término independiente ecuación 1): "))
    a2 = float(input("a2 (coeficiente de x en la ecuación 2): "))
    b2 = float(input("b2 (coeficiente de y en la ecuación 2): "))
    c2 = float(input("c2 (término independiente ecuación 2): "))
    if return_ab:
            A = [[a1, b1],
                [a2, b2]]
            b = [[c1],
                [c2]]
            return A, b

    M_aug = [[a1, b1, c1],
            [a2, b2, c2]]
    return M_aug
def solicitar_coeficientes_3x3(return_ab: bool = False):
    print("Ingrese los coeficientes para el sistema 3x3:")
    a1 = float(input("a1 (coeficiente de x en la ecuación 1): "))
    b1 = float(input("b1 (coeficiente de y en la ecuación 1): "))
    c1 = float(input("c1 (coeficiente de z en la ecuación 1): "))
    d1 = float(input("d1 (término independiente ecuación 1): "))
    a2 = float(input("a2 (coeficiente de x en la ecuación 2): "))
    b2 = float(input("b2 (coeficiente de y en la ecuación 2): "))
    c2 = float(input("c2 (coeficiente de z en la ecuación 2): "))
    d2 = float(input("d2 (término independiente ecuación 2): "))
    a3 = float(input("a3 (coeficiente de x en la ecuación 3): "))
    b3 = float(input("b3 (coeficiente de y en la ecuación 3): "))
    c3 = float(input("c3 (coeficiente de z en la ecuación 3): "))
    d3 = float(input("d3 (término independiente ecuación 3): "))

    if return_ab:
            A = [[a1, b1, c1],
                [a2, b2, c2],
                [a3, b3, c3]]
            b = [[d1],
                [d2],
                [d3]]
            return A, b

    M_aug = [[a1, b1, c1, d1],
            [a2, b2, c2, d2],
            [a3, b3, c3, d3]]
    return M_aug

# --- Utilidad opcional para imprimir bonito la matriz aumentada ---
def imprimir_matriz(M):
    # Calcula ancho por columna para alinear
    cols = len(M[0])
    widths = [max(len(str(M[i][j])) for i in range(len(M))) for j in range(cols)]
    for fila in M:
        cuerpo = "  ".join(str(x).rjust(widths[j]) for j, x in enumerate(fila[:-1]))
        print(f"[ {cuerpo} | {str(fila[-1]).rjust(widths[-1])} ]")

def solicitar_coeficientes_nxn():
    m = 0
    n = 0
    while True:
        try:
            size_input = input("Ingrese el tamaño del sistema (m x n, ejemplo: 3x3, 2x2, 5x3): ").strip()
            if 'x' not in size_input:
                print("Formato inválido. Use el formato m x n, ejemplo: 3x3.")
                continue
            parts = size_input.split('x')
            if len(parts) != 2:
                print("Formato inválido. Use el formato m x n, ejemplo: 3x3.")
                continue
            m = int(parts[0].strip())
            n = int(parts[1].strip())
            if m < 1 or n < 1:
                print("Los tamaños deben ser enteros positivos mayores que 0.")
                continue
            break
        except ValueError:
            print("Por favor ingrese números enteros válidos en el formato m x n.")
    print(f"Ingrese los coeficientes para el sistema {m}x{n}:")
    M_aug = []
    for i in range(m):
        fila = []
        for j in range(n):
            while True:
                try:
                    val = float(input(f"Coeficiente a{i+1}{j+1} (coeficiente de la variable {j+1} en la ecuación {i+1}): "))
                    break
                except ValueError:
                    print("Por favor ingrese un número válido.")
            fila.append(val)
        while True:
            try:
                val = float(input(f"b{i+1} (término independiente de la ecuación {i+1}): "))
                break
            except ValueError:
                print("Por favor ingrese un número válido.")
        fila.append(val)
        M_aug.append(fila)
    return M_aug

# --- Demo mínima (elimina este main si integras en tu programa) ---
