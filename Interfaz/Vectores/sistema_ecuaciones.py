import tkinter as tk
from tkinter import ttk, messagebox
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

class SistemaEcuacionesApp:
    """def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg=COLOR_BG)
        self.metodo_var = tk.StringVar()

        # Título
        titulo = tk.Label(parent, text="Calculadora de Álgebra Lineal",
                          font=("Segoe UI", 18, "bold"),
                          fg=COLOR_BUTTON, bg=COLOR_BG)
        titulo.pack(pady=10)

        subtitulo = tk.Label(parent,
                             text="Resuelve sistemas de ecuaciones lineales",
                             font=("Segoe UI", 10),
                             fg=COLOR_SUBTEXT, bg=COLOR_BG)
        subtitulo.pack()

        # Frame de configuración
        frame_config = tk.Frame(parent, bg=COLOR_FRAME, bd=1, relief="solid")
        frame_config.pack(fill="x", padx=20, pady=15)

        tk.Label(frame_config, text="Tamaño de la Matriz:",
                 fg=COLOR_SUBTEXT, bg=COLOR_FRAME).grid(row=0, column=0, padx=10, pady=10)

        self.matriz_combo = ttk.Combobox(frame_config, values=["2x2", "3x3", "4x4"], width=10)
        self.matriz_combo.set("2x2")
        self.matriz_combo.grid(row=0, column=1, padx=5, pady=10)

        ttk.Button(frame_config, text="Generar", command=self.generar_campos).grid(row=0, column=2, padx=5)
        ttk.Button(frame_config, text="Resolver", command=self.resolver).grid(row=0, column=3, padx=5)
        ttk.Button(frame_config, text="Limpiar", command=self.limpiar).grid(row=0, column=4, padx=5)
        
        # Metodos para resolver
        frame_metodos = tk.LabelFrame(parent, bg=COLOR_FRAME, bd=1, relief="solid")
        frame_metodos.pack(padx=20, pady=1, fill="x")
        
        LabelTituloMetodo = tk.Label(frame_metodos, text="Metodo de resolucion", fg=COLOR_SUBTEXT, bg=COLOR_FRAME)
        LabelTituloMetodo.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        self.metodo_var = tk.StringVar(value="gauss")  # Corregido: usar self.metodo_var

        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Eliminación Gaussiana",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="gauss", padx=10).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Eliminación Gauss-Jordan",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="gaussjordan", padx=10).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Escalonada Matriz (Forma escalonada)",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="Escalonada Matriz", padx=10).grid(row=3, column=0, sticky='w', padx=5, pady=2)
        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Escalonada Reducida Matriz",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="Escalonada Reducida", padx=10).grid(row=1, column=1, sticky='w', padx=5, pady=2)  # Corregido: row=4 para evitar superposición

        # Frame sistema de ecuaciones
        self.frame_sistema = tk.Frame(parent, bg=COLOR_FRAME, bd=1, relief="solid")
        self.frame_sistema.pack(fill="both", padx=20, pady=15, expand=True)

        self.entries = []  # Guardar casillas

        # Label de resultados
        self.result_label = tk.Label(parent, text="", font=("Segoe UI", 12),
                                     fg=COLOR_TEXT, bg=COLOR_BG)
        self.result_label.pack(pady=10)"""

    # sistema_ecuaciones.py
# Implementación en Python puro para resolver sistemas lineales con pasos detallados.
# Retorna (pasos, solucion, clasificacion)

def formatear_matriz(A, b, titulo="Matriz aumentada"):
    """Formatea la matriz aumentada [A | b] como string multilínea."""
    n = len(A)
    m = len(A[0])
    mat_str = f"{titulo}:\n"
    for i in range(n):
        # Coeficientes de A
        fila_a = [f"{A[i][j]:.2f}" for j in range(m)]
        # Separador y b
        fila_str = " | ".join(fila_a) + f" | {b[i]:.2f}"
        mat_str += fila_str + "\n"
    mat_str += "-" * (sum(len(s) for s in fila_a) + len(fila_a)*3 + 10) + "\n"  # Línea separadora aproximada
    return mat_str

def es_cero(valor, tol=1e-10):
    """Verifica si un valor es 'cero' numéricamente."""
    return abs(valor) < tol

def gauss(A, b):
    """Eliminación Gaussiana: Forma escalonada con pivoteo parcial y retro-sustitución."""
    n = len(A)
    m = len(A[0])  # Asume m == n (cuadrada)
    pasos = []
    mat = [row[:] for row in A]  # Copia
    vec = b[:]  # Copia de b
    
    pasos.append("INICIO - Eliminación Gaussiana (Forma Escalonada)")
    pasos.append(formatear_matriz(mat, vec, "Matriz aumentada inicial"))
    
    pivotes = {}  # Diccionario para rastrear posiciones de pivotes: (col, fila_pivote)
    rango = 0
    
    for col in range(n):
        # Pivoteo parcial: Buscar fila con mayor |elemento| en columna col, desde fila actual
        max_row = col
        max_val = abs(mat[col][col])
        for row in range(col + 1, n):
            val = abs(mat[row][col])
            if val > max_val:
                max_val = val
                max_row = row
        
        if es_cero(max_val):
            pasos.append(f"PASO {col+1}: No hay pivote no cero en columna {col+1}. Columna {col+1} es dependiente (posible variable libre).")
            continue  # Salta esta columna (no incrementa rango)
        
        # Intercambio de filas si necesario
        if max_row != col:
            mat[col], mat[max_row] = mat[max_row], mat[col]
            vec[col], vec[max_row] = vec[max_row], vec[col]
            pasos.append(f"PASO {col+1}: Intercambio de filas {col+1} y {max_row+1} para pivote máximo.")
            pasos.append(formatear_matriz(mat, vec, f"Después de intercambio en columna {col+1}"))
        
        # Registrar pivote
        pivotes[col] = col
        rango += 1
        pivote_val = mat[col][col]
        pasos.append(f"PIVOTE en posición ({col+1}, {col+1}): {pivote_val:.2f}")
        
        # Eliminación adelante (hacia abajo)
        for row in range(col + 1, n):
            if es_cero(mat[row][col]):
                continue
            factor = mat[row][col] / pivote_val
            pasos.append(f"PASO {col+1}.{row+1}: Factor de eliminación para fila {row+1}: {factor:.2f} = a{row+1}{col+1} / pivote")
            for j in range(col, m):  # Desde col para eficiencia
                mat[row][j] -= factor * mat[col][j]
            vec[row] -= factor * vec[col]
            mat[row][col] = 0.0  # Asegurar cero exacto
        pasos.append(formatear_matriz(mat, vec, f"Después de eliminación abajo en columna {col+1}"))
    
    # Verificar consistencia y clasificar
    clasificacion, solucion = analizar_y_resolver(mat, vec, n, m, pivotes, pasos, metodo="gauss")
    pasos.append(f"RANGO de la matriz: {rango}")
    return pasos, solucion, clasificacion

def gauss_jordan(A, b):
    """Eliminación Gauss-Jordan: Forma escalonada reducida (adelante + atrás)."""
    n = len(A)
    m = len(A[0])
    pasos = []
    mat = [row[:] for row in A]
    vec = b[:]
    
    pasos.append("INICIO - Eliminación Gauss-Jordan (Forma Reducida)")
    pasos.append(formatear_matriz(mat, vec, "Matriz aumentada inicial"))
    
    pivotes = {}
    rango = 0
    
    # Fase 1: Eliminación adelante (igual que gauss)
    for col in range(n):
        max_row = col
        max_val = abs(mat[col][col])
        for row in range(col + 1, n):
            val = abs(mat[row][col])
            if val > max_val:
                max_val = val
                max_row = row
        
        if es_cero(max_val):
            continue
        
        if max_row != col:
            mat[col], mat[max_row] = mat[max_row], mat[col]
            vec[col], vec[max_row] = vec[max_row], vec[col]
            pasos.append(f"PASO {col+1}: Intercambio de filas {col+1} y {max_row+1}.")
            pasos.append(formatear_matriz(mat, vec, f"Después de intercambio"))
        
        pivotes[col] = col
        rango += 1
        pivote_val = mat[col][col]
        pasos.append(f"PIVOTE en ({col+1}, {col+1}): {pivote_val:.2f}")
        
        # Normalizar fila pivote (dividir por pivote para hacer 1)
        if abs(pivote_val - 1.0) > 1e-10:
            factor_norm = 1.0 / pivote_val
            pasos.append(f"PASO {col+1}a: Normalización fila {col+1} por {factor_norm:.2f}")
            for j in range(col, m):
                mat[col][j] *= factor_norm
            vec[col] *= factor_norm
            pasos.append(formatear_matriz(mat, vec, f"Después de normalización"))
        
        # Eliminación abajo
        for row in range(col + 1, n):
            if es_cero(mat[row][col]):
                continue
            factor = mat[row][col]
            pasos.append(f"PASO {col+1}b.{row+1}: Eliminación abajo fila {row+1} por {factor:.2f}")
            for j in range(col, m):
                mat[row][j] -= factor * mat[col][j]
            vec[row] -= factor * vec[col]
            mat[row][col] = 0.0
        pasos.append(formatear_matriz(mat, vec, f"Después de eliminación abajo"))
    
    # Fase 2: Eliminación atrás (hacia arriba)
    for col in range(n - 1, -1, -1):
        if col not in pivotes:
            continue
        pivote_row = pivotes[col]
        for row in range(pivote_row - 1, -1, -1):
            if es_cero(mat[row][col]):
                continue
            factor = mat[row][col]
            pasos.append(f"PASO atrás {col+1}.{row+1}: Eliminación arriba fila {row+1} por {factor:.2f}")
            for j in range(col, m):
                mat[row][j] -= factor * mat[pivote_row][j]
            vec[row] -= factor * vec[pivote_row]
            mat[row][col] = 0.0
        pasos.append(formatear_matriz(mat, vec, f"Después de eliminación arriba en columna {col+1}"))
    
    clasificacion, solucion = analizar_y_resolver(mat, vec, n, m, pivotes, pasos, metodo="gauss_jordan")
    pasos.append(f"RANGO de la matriz: {rango}")
    return pasos, solucion, clasificacion

def forma_escalonada(A, b):
    """Forma escalonada simple (similar a gauss, sin retro-sustitución detallada)."""
    # Reusa lógica de gauss, pero sin la fase de resolución en pasos
    return gauss(A, b)  # Por simplicidad, misma que gauss (puedes diferenciar si quieres solo escalonamiento)

def forma_escalonada_reducida(A, b):
    """Forma escalonada reducida (similar a gauss_jordan)."""
    return gauss_jordan(A, b)  # Por simplicidad, misma que gauss_jordan

def analizar_y_resolver(mat, vec, n, m, pivotes, pasos, metodo="gauss"):
    """Analiza la matriz escalonada/reducida para clasificar y resolver."""
    # Verificar inconsistencia
    inconsistent = False
    for i in range(n):
        all_zero = all(es_cero(mat[i][j]) for j in range(m))
        if all_zero and not es_cero(vec[i]):
            inconsistent = True
            pasos.append(f"INCONSISTENTE: Fila {i+1} es [0 ... 0 | {vec[i]:.2f}] ≠ 0")
            return "Incompatible (Sin solución)", None
    
    if inconsistent:
        return "Incompatible", None
    
    rango = len(pivotes)
    if rango == n:
        # Compatible determinado: Retro-sustitución
        pasos.append("SISTEMA COMPATIBLE DETERMINADO - Retro-sustitución hacia atrás:")
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            piv_col = [k for k, v in pivotes.items() if v == i][0] if metodo == "gauss" else i  # Ajuste para gauss
            sum_ax = vec[i]
            for j in range(i + 1, n):
                sum_ax -= mat[i][j] * x[j]
            x[i] = sum_ax / mat[i][i] if not es_cero(mat[i][i]) else 0.0
            pasos.append(f"x{i+1} = ({sum_ax:.2f} / {mat[i][i]:.2f}) = {x[i]:.2f}")
        solucion = [f"x{k+1} = {x[k]:.2f}" for k in range(n)]
        return "Compatible determinado (Solución única)", solucion
    
    else:
        # Compatible indeterminado: Variables libres
        pasos.append(f"SISTEMA COMPATIBLE INDETERMINADO - Rango {rango} < {n} variables. Hay {n - rango} variables libres.")
        libres_cols = [col for col in range(n) if col not in pivotes]
        params = ['t', 's', 'u', 'v'][:len(libres_cols)]  # Parámetros simples
        var_libres = {libres_cols[k]: params[k] for k in range(len(libres_cols))}
        pasos.append(f"Variables libres: {', '.join([f'x{j+1} = {p}' for j, p in var_libres.items()])}")
        
        # Expresar solución general (simple: asignar libres y back-sub para dependientes)
        x = {}
        for col, param in var_libres.items():
            x[col] = param
        # Back-sub para variables pivote
        for i in range(n - 1, -1, -1):
            if i in pivotes.values():  # Es pivote row
                piv_col = next(k for k, v in pivotes.items() if v == i)
                sum_ax = vec[i]
                for j in range(piv_col + 1, n):
                    if j in x:
                        sum_ax -= mat[i][j] * x[j]
                if not es_cero(mat[i][piv_col]):
                    x[piv_col] = f"({sum_ax:.2f}" + "".join([f" - {mat[i][j]:.2f}*{x[j]}" if isinstance(x[j], str) and mat[i][j] != 0 else "" for j in range(piv_col + 1, n)]) + f") / {mat[i][piv_col]:.2f}"
                else:
                    x[piv_col] = "0"  # No debería pasar
        solucion = [f"x{k+1} = {x.get(k, '0')}" for k in range(n)]
        return f"Compatible indeterminado ({n - rango} parámetros libres)", solucion
