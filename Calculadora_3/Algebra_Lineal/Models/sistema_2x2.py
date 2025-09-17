# sistema_2x2.py
# Programa para resolver sistemas de ecuaciones lineales 2x2
# utilizando métodos de sustitución y eliminación
# Sin librerías externas, solo Python estándar
from fractions import Fraction

def solicitar_coeficientes_2x2():
    """
    Solicita al usuario los coeficientes del sistema 2x2.
    Devuelve la matriz aumentada como lista de listas.
    """
    print("Ingrese los coeficientes para el sistema 2x2:")
    while True:
        try:
            a1 = float(input("a1 (coeficiente de x en la ecuación 1): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    while True:
        try:
            b1 = float(input("b1 (coeficiente de y en la ecuación 1): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    while True:
        try:
            c1 = float(input("c1 (término independiente ecuación 1): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    while True:
        try:
            a2 = float(input("a2 (coeficiente de x en la ecuación 2): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    while True:
        try:
            b2 = float(input("b2 (coeficiente de y en la ecuación 2): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    while True:
        try:
            c2 = float(input("c2 (término independiente ecuación 2): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    M_aug = [[a1, b1, c1], [a2, b2, c2]]
    return M_aug

def imprimir_matriz(M):
    """
    Imprime la matriz de forma visual en la terminal.
    Calcula anchos para alinear las columnas.
    """
    cols = len(M[0])
    widths = [max(len(str(M[i][j])) for i in range(len(M))) for j in range(cols)]
    for fila in M:
        cuerpo = "  ".join(str(x).rjust(widths[j]) for j, x in enumerate(fila[:-1]))
        print(f"[ {cuerpo} | {str(fila[-1]).rjust(widths[-1])} ]")

def confirmar_matriz(M):
    """
    Muestra la matriz y pide confirmación al usuario.
    """
    print("\nMatriz aumentada:")
    imprimir_matriz(M)
    while True:
        confirm = input("¿Es correcta esta matriz? (si/no): ").lower()
        if confirm == 'si':
            return True
        elif confirm == 'no':
            return False
        else:
            print("Responda 'si' para sí o 'no' para no.")

def sustitucion_2x2(a1, b1, c1, a2, b2, c2):
    """
    Resuelve el sistema 2x2 por método de sustitución.
    Muestra pasos en forma de matriz.
    Devuelve (x, y) si hay solución única, None si no.
    """
    M = [[a1, b1, c1], [a2, b2, c2]]
    print("Matriz inicial:")
    imprimir_matriz(M)
    print("\nMétodo de sustitución:")
    if a1 == 0:
        print("No se puede despejar x de la primera ecuación (a1=0).")
        return None
    print(f"Paso 1: Despejar x de la primera ecuación: x = ({c1} - {b1}*y) / {a1}")
    coef_y = -a2 * b1 + b2 * a1
    term_ind = c2 * a1 - a2 * c1
    print(f"Paso 2: Sustituir en la segunda ecuación: {coef_y}*y = {term_ind}")
    if coef_y == 0:
        print("El sistema no tiene solución única.")
        return None
    y = term_ind / coef_y
    print(f"Paso 3: Calcular y = {term_ind} / {coef_y} = {y}")
    x = (c1 - b1 * y) / a1
    print(f"Paso 4: Calcular x = ({c1} - {b1}*{y}) / {a1} = {x}")
    return x, y

def eliminacion_2x2(a1, b1, c1, a2, b2, c2):
    """
    Resuelve el sistema 2x2 por método de eliminación.
    Muestra pasos en forma de matriz.
    Devuelve (x, y) si hay solución única, None si no.
    """
    M = [[a1, b1, c1], [a2, b2, c2]]
    print("Matriz inicial:")
    imprimir_matriz(M)
    print("\nMétodo de eliminación:")
    factor = a2 / a1
    print(f"Paso 1: Multiplicar fila 1 por {factor} y restar de fila 2 para eliminar x:")
    M[1][0] -= factor * M[0][0]
    M[1][1] -= factor * M[0][1]
    M[1][2] -= factor * M[0][2]
    imprimir_matriz(M)
    coef_y = M[1][1]
    term_ind = M[1][2]
    if coef_y == 0:
        print("El sistema no tiene solución única.")
        return None
    y = term_ind / coef_y
    print(f"Paso 2: Calcular y = {term_ind} / {coef_y} = {y}")
    x = (c1 - b1 * y) / a1
    print(f"Paso 3: Calcular x = ({c1} - {b1}*{y}) / {a1} = {x}")
    return x, y

def main():
    """
    Función principal del programa.
    """
    print("Resolución de Sistema 2x2")
    M = solicitar_coeficientes_2x2()
    if not confirmar_matriz(M):
        print("Vuelva a ejecutar el programa para ingresar nuevamente.")
        return
    print("\nSeleccione método:")
    print("1. Sustitución")
    print("2. Eliminación")
    metodo = input("Ingrese opción (1/2): ")
    if metodo == "1":
        resultado = sustitucion_2x2(*M[0], *M[1])
    elif metodo == "2":
        resultado = eliminacion_2x2(*M[0], *M[1])
    else:
        print("Opción inválida.")
        return
    if resultado:
        x, y = resultado
        x_frac = Fraction(x).limit_denominator()
        y_frac = Fraction(y).limit_denominator()
        print(f"\nSolución decimal: x = {x}, y = {y}")
        print(f"Solución fracción: x = {x_frac}, y = {y_frac}")
    else:
        print("No hay solución única.")

if __name__ == "__main__":
    main()
