# main.py
# Módulo principal que ejecuta el programa

import sistema
import vectores   #  nuevo módulo que vamos a crear (vectores.py)

def main():
    print("Calculadora de Álgebra Lineal")
    while True:
        print("\n1. Resolver sistema de ecuaciones")
        print("2. Operaciones con vectores en R^n")
        print("3. Salir")
        opcion = input("Ingrese opción (1/2/3): ")

        if opcion == "1":
            sistema.resolver_sistema()
        elif opcion == "2":
            vectores.menu_vectores()   #  llama al submenú de vectores
        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    main()