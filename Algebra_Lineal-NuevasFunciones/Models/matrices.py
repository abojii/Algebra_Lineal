# matrices.py
# Métodos para convertir matrices a forma escalonada y escalonada reducida
from fractions import Fraction

# Función auxiliar para imprimir la matriz paso a paso
def imprimir_matriz(matriz):
    for fila in matriz:
        print("   ".join(str(val) for val in fila))
    print()

def escalonada(matriz):
    print("\n=== Proceso hacia Forma Escalonada ===")
    # Convertimos a fracciones
    matriz = [list(map(Fraction, fila)) for fila in matriz]
    filas = len(matriz)
    columnas = len(matriz[0])
    fila_pivote = 0

    for col in range(columnas - 1):  # ignoramos última columna como pivote
        if fila_pivote >= filas:
            break

        # Buscar pivote distinto de 0
        pivote = None
        for i in range(fila_pivote, filas):
            if matriz[i][col] != 0:
                pivote = i
                break
        if pivote is None:
            continue

        # Intercambiar filas si es necesario
        if pivote != fila_pivote:
            matriz[fila_pivote], matriz[pivote] = matriz[pivote], matriz[fila_pivote]
            print(f"Intercambio f{fila_pivote+1} <-> f{pivote+1}")
            imprimir_matriz(matriz)

        # Normalizar la fila del pivote
        divisor = matriz[fila_pivote][col]
        matriz[fila_pivote] = [val/divisor for val in matriz[fila_pivote]]
        print(f"f{fila_pivote+1} --> f{fila_pivote+1} / {divisor}")
        imprimir_matriz(matriz)

        # Hacer ceros debajo del pivote
        for i in range(fila_pivote+1, filas):
            factor = matriz[i][col]
            if factor != 0:
                matriz[i] = [matriz[i][j] - factor*matriz[fila_pivote][j] for j in range(columnas)]
                print(f"f{i+1} --> f{i+1} - ({factor})*f{fila_pivote+1}")
                imprimir_matriz(matriz)

        fila_pivote += 1

    return matriz


def escalonada_reducida(matriz):
    print("\n=== Proceso hacia Forma Escalonada Reducida ===")
    # Convertimos a fracciones
    matriz = [list(map(Fraction, fila)) for fila in matriz]
    filas = len(matriz)
    columnas = len(matriz[0])

    # Primero llevamos a forma escalonada
    matriz = escalonada(matriz)

    # Ahora hacia arriba: ceros arriba de cada pivote
    for i in range(filas-1, -1, -1):
        # Buscar pivote en la fila
        pivote = None
        for j in range(columnas - 1):
            if matriz[i][j] == 1:
                pivote = j
                break
        if pivote is None:
            continue

        # Hacer ceros arriba del pivote
        for k in range(i):
            factor = matriz[k][pivote]
            if factor != 0:
                matriz[k] = [matriz[k][m] - factor*matriz[i][m] for m in range(columnas)]
                print(f"f{k+1} --> f{k+1} - ({factor})*f{i+1}")
                imprimir_matriz(matriz)

    return matriz
