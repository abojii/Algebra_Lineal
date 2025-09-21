# sistema.py
# Funciones que identifican dimensión, solicitan coeficientes y llaman al método seleccionado
# Ahora soporta cualquier tamaño de sistema
import entrada
import metodos
from fractions import Fraction

def resolver_sistema():
    coef = None
    while True:
        if coef is None:
            coef = entrada.solicitar_coeficientes_nxn()
            print("\nMatriz aumentada:")
            # USAR el formateador de metodos (2 decimales)
            metodos.print_matrix_with_format(metodos.format_matrix(coef))
            confirm = input("¿Es correcta esta matriz? (si/no): ").lower()
            if confirm == 'no':
                print("Vuelva a ingresar los coeficientes.\n")
                coef = None
                continue
            elif confirm != 'si':
                print("Responda 'si' para sí o 'no' para no.")
                continue

        # Dimensiones
        m = len(coef)
        n = len(coef[0]) - 1  # número de variables

        # Tipo de solución (feedback temprano)
        M_escalonada = metodos.escalonada_matriz(coef, mostrar_pasos=False, mostrar_pivotes=False)
        A_escalonada = [fila[:n] for fila in M_escalonada]
        Ab_escalonada = M_escalonada
        rango_A = metodos.matriz_rango(A_escalonada)
        rango_Ab = metodos.matriz_rango(Ab_escalonada)

        if rango_A == rango_Ab == n:
            tipo_solucion = "única solución"
        elif rango_A == rango_Ab < n:
            tipo_solucion = "infinitas soluciones"
        else:
            tipo_solucion = "no tiene solución"

        print(f"\nEl sistema tiene {tipo_solucion}.")

        mostrar_pivotes = input("¿Desea mostrar los pivotes durante el proceso? (si/no): ").lower() == 'si'

        print("\nSeleccione el método de resolución:")
        print("1. Sustitución (solo para 2x2 o 3x3)")
        print("2. Eliminación (solo para 2x2 o 3x3)")
        print("3. Gauss Jordan")
        print("4. Gauss")
        print("5. Escalonada Matriz (forma escalonada)")
        print("6. Escalonada Reducida Matriz (forma escalonada reducida)")
        metodo = input("Ingrese opción (1-6): ")

        resultado = None  # por defecto

        if metodo == "1":
            if m == n == 2:
                resultado = metodos.sustitucion_2x2(*coef[0], *coef[1])
            elif m == n == 3:
                resultado = metodos.sustitucion_3x3(*coef[0], *coef[1], *coef[2])
            else:
                print("Sustitución solo disponible para sistemas cuadrados 2x2 o 3x3.")
                # seguimos al diagnóstico final igualmente
        elif metodo == "2":
            if m == n == 2:
                resultado = metodos.eliminacion_2x2(*coef[0], *coef[1])
            elif m == n == 3:
                resultado = metodos.eliminacion_3x3(*coef[0], *coef[1], *coef[2])
            else:
                print("Eliminación solo disponible para sistemas cuadrados 2x2 o 3x3.")
        elif metodo == "3":
            resultado = metodos.gauss_jordan_general(coef, mostrar_pasos=True, mostrar_pivotes=mostrar_pivotes)
        elif metodo == "4":
            resultado = metodos.gauss(coef, mostrar_pasos=True, mostrar_pivotes=mostrar_pivotes)
        elif metodo == "5":
            M_escalonada = metodos.escalonada_matriz(coef, mostrar_pasos=True, mostrar_pivotes=mostrar_pivotes)
            print("\nMatriz en forma escalonada:")
            # USAR el formateador de metodos (2 decimales)
            metodos.print_matrix_with_format(metodos.format_matrix(M_escalonada))
        elif metodo == "6":
            M_reducida = metodos.escalonada_reducida_matriz(coef, mostrar_pasos=True, mostrar_pivotes=mostrar_pivotes)
            print("\nMatriz en forma escalonada reducida:")
            # USAR el formateador de metodos (2 decimales)
            metodos.print_matrix_with_format(metodos.format_matrix(M_reducida))
        else:
            print("Opción de método inválida.")

        # Mostrar solución numérica si existe
        if resultado is not None:
            print("\nSolución encontrada:")
            for i, val in enumerate(resultado):
                val_rounded = round(val, 2)
                val_frac = Fraction(val).limit_denominator()
                # Imprimir SIEMPRE con 2 decimales
                print(f"Variable {i+1}: decimal = {val_rounded:.2f}, fracción = {val_frac}")
        else:
            print("No hay solución única o no se resolvió el sistema.")

        # --- Diagnóstico final requerido: SIEMPRE se imprime (FE y FER) ---
        print("\n--- Diagnóstico final (Forma Escalonada - FE) ---")
        metodos.diagnostico_sistema(
            coef,
            forma="escalonada",
            nombres=[f"x{i+1}" for i in range(n)],
            mostrar_pasos=False
        )

        print("\n--- Diagnóstico final (Forma Escalonada Reducida - FER) ---")
        metodos.diagnostico_sistema(
            coef,
            forma="reducida",
            nombres=[f"x{i+1}" for i in range(n)],
            mostrar_pasos=False
        )

        seguir = input("\n¿Desea resolver la misma matriz con otro método? (si/no): ").lower()
        if seguir != 'si':
            break
