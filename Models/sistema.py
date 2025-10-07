# sistema.py
# Funciones que identifican dimensión, solicitan coeficientes y llaman al método seleccionado
from Models import entrada
from Models import metodos
from fractions import Fraction

def es_homogeneo(matriz_aumentada):
    # Verifica si la última columna es todo ceros para cualquier tamaño de matriz aumentada
    if not matriz_aumentada or not matriz_aumentada[0]:
        return False  # matriz vacía o inválida
    for fila in matriz_aumentada:
        if len(fila) < 2:
            return False  # no es matriz aumentada válida
        if fila[-1] != 0:
            return False
    return True

def resolver_sistema():
    print("Seleccione el tipo de sistema a resolver:")
    print("1. Sistema 2x2")
    print("2. Sistema 3x3")
    opcion = input("Ingrese opción (1/2): ")
    if opcion == "1":
        while True:
            coef = entrada.solicitar_coeficientes_2x2()
            print("\nMatriz aumentada:")
            entrada.imprimir_matriz(coef)
            if es_homogeneo(coef):
                print("El sistema es homogéneo.")
            else:
                print("El sistema no es homogéneo.")
            confirm = input("¿Es correcta esta matriz? (si/no): ").lower()
            if confirm == 'si':
                break
            elif confirm == 'no':
                print("Vuelva a ingresar los coeficientes.\n")
            else:
                print("Responda 'si' para sí o 'no' para no.")
        print("\nSeleccione el método de resolución:")
        print("1. Sustitución")
        print("2. Eliminación")
        metodo = input("Ingrese opción (1,2): ")
        if metodo == "1":
            resultado = metodos.sustitucion_2x2(*coef[0], *coef[1])
            if resultado:
                x, y = resultado
                x_frac = Fraction(x).limit_denominator()
                y_frac = Fraction(y).limit_denominator()
                print(f"Solución decimal: x = {x}, y = {y}")
                print(f"Solución fracción: x = {x_frac}, y = {y_frac}")
            else:
                print("No hay solución única.")
        elif metodo == "2":
            resultado = metodos.eliminacion_2x2(*coef[0], *coef[1])
            if resultado:
                x, y = resultado
                x_frac = Fraction(x).limit_denominator()
                y_frac = Fraction(y).limit_denominator()
                print(f"Solución decimal: x = {x}, y = {y}")
                print(f"Solución fracción: x = {x_frac}, y = {y_frac}")
            else:
                print("No hay solución única.")     
        else:
            print("Opción de método inválida.")

    elif opcion == "2":
        while True:
            coef = entrada.solicitar_coeficientes_3x3()
            print("\nMatriz aumentada:")
            entrada.imprimir_matriz(coef)
            if es_homogeneo(coef):
                print("El sistema es homogéneo.")
            else:
                print("El sistema no es homogéneo.")
            confirm = input("¿Es correcta esta matriz? (si/no): ").lower()
            if confirm == 'si':
                break
            elif confirm == 'no':
                print("Vuelva a ingresar los coeficientes.\n")
            else:
                print("Responda 'si' para sí o 'no' para no.")
        print("\nSeleccione el método de resolución:")
        print("1. Sustitución")
        print("2. Eliminación")
        print("3. Gauss Jordan")
        print("4. Gauss")
        metodo = input("Ingrese opción (1,2,3,4): ")
        if metodo == "1":
            resultado = metodos.sustitucion_3x3(*coef[0], *coef[1], *coef[2])
            if resultado:
                x, y, z = resultado
                x_frac = Fraction(x).limit_denominator()
                y_frac = Fraction(y).limit_denominator()
                z_frac = Fraction(z).limit_denominator()
                print(f"\nSolución decimal: x = {x}, y = {y}, z = {z}")
                print(f"Solución fracción: x = {x_frac}, y = {y_frac}, z = {z_frac}")
            else:
                print("No hay solución única.")
        elif metodo == "2":
            resultado = metodos.eliminacion_3x3(*coef[0], *coef[1], *coef[2])
            if resultado:
                x, y, z = resultado
                x_frac = Fraction(x).limit_denominator()
                y_frac = Fraction(y).limit_denominator()
                z_frac = Fraction(z).limit_denominator()
                print(f"Solución decimal: x = {x}, y = {y}, z = {z}")
                print(f"Solución fracción: x = {x_frac}, y = {y_frac}, z = {z_frac}")
            else:
                print("No hay solución única.")
                
        elif metodo == "3":
            resultado = metodos.gauss_jordan(*coef[0], *coef[1], *coef[2])
            if resultado:
                x, y, z= resultado
                x_frac = Fraction(x).limit_denominator()
                y_frac = Fraction(y).limit_denominator()
                z_frac = Fraction(z).limit_denominator()
                print(f"Solución decimal: x = {x}, y = {y}, z = {z}")
                print(f"Solución fracción: x = {x_frac}, y = {y_frac}, z = {z_frac}")
            else:
                print("No hay solución única.")
                
        elif metodo == "4":
            resultado = metodos.gauss(*coef[0], *coef[1], *coef[2])
            if resultado:
                x, y, z= resultado
                x_frac = Fraction(x).limit_denominator()
                y_frac = Fraction(y).limit_denominator()
                z_frac = Fraction(z).limit_denominator()
                print(f"Solución decimal: x = {x}, y = {y}, z = {z}")
                print(f"Solución fracción: x = {x_frac}, y = {y_frac}, z = {z_frac}")
            else:
                print("No hay solución única.")  
                
        else:
            print("Opción de método inválida.")
            
    else:
        print("Opción inválida.")
