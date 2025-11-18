# main.py
# Módulo principal que ejecuta el programa
import sistema
def main():
    print("Calculadora de Álgebra Lineal - Sistemas de Ecuaciones")
    while True:
        print("\n1. Resolver sistema")
        print("2. Salir")
        opcion = input("Ingrese opción (1/2): ")
        if opcion == "1":
            sistema.resolver_sistema()
        elif opcion == "2":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida, intente de nuevo.")
if __name__ == "__main__":
    main()