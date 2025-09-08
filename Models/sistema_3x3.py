# sistema_3x3.py
# Programa para resolver sistemas de ecuaciones lineales 3x3
# utilizando métodos de sustitución y eliminación
# Sin librerías externas, solo Python estándar
from fractions import Fraction

def solicitar_coeficientes_3x3():
    """
    Solicita al usuario los coeficientes del sistema 3x3.
    Devuelve la matriz aumentada como lista de listas.
    """
    print("Ingrese los coeficientes para el sistema 3x3:")
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
            c1 = float(input("c1 (coeficiente de z en la ecuación 1): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    while True:
        try:
            d1 = float(input("d1 (término independiente ecuación 1): "))
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
            c2 = float(input("c2 (coeficiente de z en la ecuación 2): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    while True:
        try:
            d2 = float(input("d2 (término independiente ecuación 2): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    while True:
        try:
            a3 = float(input("a3 (coeficiente de x en la ecuación 3): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    while True:
        try:
            b3 = float(input("b3 (coeficiente de y en la ecuación 3): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    while True:
        try:
            c3 = float(input("c3 (coeficiente de z en la ecuación 3): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    while True:
        try:
            d3 = float(input("d3 (término independiente ecuación 3): "))
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    M_aug = [[a1, b1, c1, d1], [a2, b2, c2, d2], [a3, b3, c3, d3]]
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

def sustitucion_3x3(a1, b1, c1, d1, a2, b2, c2, d2, a3, b3, c3, d3):
    """
    Resuelve el sistema 3x3 por método de sustitución.
    Devuelve (x, y, z) si hay solución única, None si no.
    """
    if a1 == 0:
        print("No se puede despejar x de la primera ecuación (a1=0).")
        return None
    coef_y2 = -a2 * b1 + b2 * a1
    coef_z2 = -a2 * c1 + c2 * a1
    term_ind2 = d2 * a1 - a2 * d1
    coef_y3 = -a3 * b1 + b3 * a1
    coef_z3 = -a3 * c1 + c3 * a1
    term_ind3 = d3 * a1 - a3 * d1
    coef_z = coef_z2 * coef_y3 - coef_z3 * coef_y2
    term_ind = term_ind2 * coef_y3 - term_ind3 * coef_y2
    if coef_z == 0:
        print("No hay solución única.")
        return None
    z = term_ind / coef_z
    y = (term_ind2 - coef_z2 * z) / coef_y2
    x = (d1 - b1 * y - c1 * z) / a1
    return x, y, z

def eliminacion_3x3(a1, b1, c1, d1, a2, b2, c2, d2, a3, b3, c3, d3):
    """
    Resuelve el sistema 3x3 por método de eliminación.
    Devuelve (x, y, z) si hay solución única, None si no.
    """
    b2_new = b1 * a2 - b2 * a1
    c2_new = c1 * a2 - c2 * a1
    d2_new = d1 * a2 - d2 * a1
    b3_new = b1 * a3 - b3 * a1
    c3_new = c1 * a3 - c3 * a1
    d3_new = d1 * a3 - d3 * a1
    coef_z = c2_new * b3_new - c3_new * b2_new
    term_ind = d2_new * b3_new - d3_new * b2_new
    if coef_z == 0:
        print("No hay solución única.")
        return None
    z = term_ind / coef_z
    y = (d2_new - c2_new * z) / b2_new
    x = (d1 - b1 * y - c1 * z) / a1
    return x, y, z

def gauss_jordan(a1, b1, c1, d1, a2, b2, c2, d2, a3, b3, c3, d3):
    Fila1 = [a1, b1, c1]
    Fila2 = [a2, b2, c2]
    Fila3 = [a3, b3, c3]
    a1 = [Fila1, Fila2, Fila3]
    
    b1 = [d1, d2, d3]
    
    def OperacionesGauss(A, b):
        n = 3

        for i in range(n):
            A[i].append(b[i])
    
        for i in range(n):
            # Buscar pivote
            pivot = A[i][i]
            if pivot == 0:
                raise ValueError("Pivote cero, el sistema puede no tener solución única")
        
        # Dividir toda la fila por el pivote para hacer el pivote 1
        for k in range(i, n+1):
            A[i][k] /= pivot
        
        # Hacer ceros en toda la columna i excepto en la fila i
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n+1):
                    A[j][k] -= factor * A[i][k]
    
        # Ahora la matriz aumentada tiene la forma [I | x]
        x = A[0][n]
        y = A[1][n]
        z = A[2][n]
        return x, y, z

    return OperacionesGauss(a1, b1)

def gauss(a1, b1, c1, d1, a2, b2, c2, d2, a3, b3, c3, d3):
    Fila1 = [a1, b1, c1]
    Fila2 = [a2, b2, c2]
    Fila3 = [a3, b3, c3]
    a1 = [Fila1, Fila2, Fila3]
    
    b1 = [d1, d2, d3]
    
    def OperacionesGauss1(A, b):
        n = 3

        for i in range(n):
            A[i].append(b[i])
    
        for i in range(n):
            # Buscar pivote
            pivot = A[i][i]
            if pivot == 0:
                raise ValueError("Pivote cero, el sistema puede no tener solución única")

            for j in range(i + 1, n):
                factor = A[j][i] / pivot
                for k in range(i, n+1):
                    A[j][k] -= factor * A[i][k]
        # Dividir toda la fila por el pivote para hacer el pivote 1
        x = [0 for _ in range(n)]
        for i in range(n-1, -1, -1):
            suma = 0
            for j in range(i+1, n):
                suma += A[i][j] * x[j]
            x[i] = (A[i][n] - suma) / A[i][i]
        
        return tuple(x)

    return OperacionesGauss1(a1, b1)

def main():
    """
    Función principal del programa.
    """
    print("Resolución de Sistema 3x3")
    M = solicitar_coeficientes_3x3()
    if not confirmar_matriz(M):
        print("Vuelva a ejecutar el programa para ingresar nuevamente.")
        return
    print("\nSeleccione método:")
    print("1. Sustitución")
    print("2. Eliminación")
    metodo = input("Ingrese opción (1/2): ")
    if metodo == "1":
        resultado = sustitucion_3x3(*M[0], *M[1], *M[2])
    elif metodo == "2":
        resultado = eliminacion_3x3(*M[0], *M[1], *M[2])
    else:
        print("Opción inválida.")
        return
    if resultado:
        x, y, z = resultado
        x_frac = Fraction(x).limit_denominator()
        y_frac = Fraction(y).limit_denominator()
        z_frac = Fraction(z).limit_denominator()
        print(f"\nSolución decimal: x = {x}, y = {y}, z = {z}")
        print(f"Solución fracción: x = {x_frac}, y = {y_frac}, z = {z_frac}")
    else:
        print("No hay solución única.")

if __name__ == "__main__":
    main()
