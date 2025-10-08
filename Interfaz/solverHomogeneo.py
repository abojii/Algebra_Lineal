from copy import deepcopy

def create_matrix(rows, cols, default=0.0):
    """Crea una matriz vacía (lista de listas)."""
    return [[default for _ in range(cols)] for _ in range(rows)]

def matrix_to_string(mat, precision=4):
    """Convierte matriz a string legible."""
    if not mat:
        return "[]"
    rows = []
    for row in mat:
        rows.append("[" + " ".join(f"{x:.{precision}f}" if isinstance(x, float) else str(x) for x in row) + "]")
    return "\n".join(rows)

def is_zero(val, tol=1e-10):
    """Verifica si un valor es 'cero' con tolerancia."""
    return abs(val) < tol

def swap_rows(mat, r1, r2):
    """Intercambia dos filas en la matriz."""
    mat[r1], mat[r2] = mat[r2], mat[r1]

def scale_row(mat, row, scalar):
    """Multiplica una fila por un escalar."""
    for j in range(len(mat[0])):
        mat[row][j] *= scalar

def add_scaled_row(mat, target_row, source_row, scalar):
    """Agrega scalar * source_row a target_row."""
    for j in range(len(mat[0])):
        mat[target_row][j] += scalar * mat[source_row][j]

def solve_linear_system(A, b, homogeneous=False):
    # sourcery skip: low-code-quality
    """
    Resuelve A x = b (o A x = 0 si homogeneous) con Gauss-Jordan manual.
    
    Args:
        A: list of lists (m x n) - Matriz de coeficientes.
        b: list (m,) - Vector de términos independientes.
        homogeneous: bool - Si True, fuerza b = [0]*m.
    
    Returns:
        dict con 'steps' (list[str]), 'solution_general' (str), 'solution_trivial' (str),
               'rank' (int), 'free_vars' (list[int]), 'particular_solution' (str),
               'linear_independent' (bool), 'error' (str o None).
    """
    if homogeneous:
        b = [0.0] * len(b)
    
    m = len(A)  # Filas
    if m == 0:
        return {'error': 'Matriz vacía.'}
    n = len(A[0])  # Columnas
    
    # Matriz aumentada [A | b]
    aug = [A[i][:] + [b[i]] for i in range(m)]
    
    steps = []
    steps.append("Paso 0: Matriz aumentada inicial [A | b]:\n" + matrix_to_string(aug))
    
    # Gauss-Jordan: Hacia adelante
    rank = 0
    pivot_cols = {}  # col -> row
    for col in range(n):
        # Buscar pivote (primera fila >= rank con |aug[row][col]| > tol)
        pivot_row = None
        for row in range(rank, m):
            if not is_zero(aug[row][col]):
                pivot_row = row
                break
        
        if pivot_row is None:
            steps.append(f"Paso {len(steps)}: No pivote en columna {col}. Posible variable libre.")
            continue
        
        # Intercambiar si necesario
        if pivot_row != rank:
            swap_rows(aug, rank, pivot_row)
            steps.append(f"Paso {len(steps)}: Intercambio filas {rank} y {pivot_row} para pivote en col {col}.")
            steps.append("Matriz después de intercambio:\n" + matrix_to_string(aug))
        
        pivot = aug[rank][col]
        steps.append(f"Paso {len(steps)}: Pivote fila {rank}, col {col}: {pivot:.4f}. Normalizando fila {rank}.")
        
        # Normalizar fila pivote (dividir por pivote)
        scale_row(aug, rank, 1.0 / pivot)
        steps.append("Matriz después de normalización:\n" + matrix_to_string(aug))
        
        # Eliminar en otras filas (hacia adelante y atrás, pero primero adelante)
        for row in range(m):
            if row != rank and not is_zero(aug[row][col]):
                factor = aug[row][col]
                add_scaled_row(aug, row, rank, -factor)
                steps.append(f"Paso {len(steps)}: Eliminación fila {row}: restar {factor:.4f} * fila {rank}.")
        
        steps.append(f"Matriz después de eliminación en col {col}:\n" + matrix_to_string(aug))
        
        pivot_cols[col] = rank
        rank += 1
        if rank == m:
            break  # No más filas
    
    # Rango = número de pivotes
    rank = len(pivot_cols)
    steps.append(f"Paso final: Rango de A = {rank} (pivotes encontrados).")
    
    # Verificar consistencia (no homogéneo)
    consistent = True
    for row in range(rank, m):
        if not is_zero(aug[row][n]):
            consistent = False
            steps.append(f"Inconsistente: Fila {row} es [0...0 | {aug[row][n]:.4f}] != 0.")
    
    if not consistent:
        return {
            'steps': steps,
            'solution_general': 'Sistema inconsistente: No hay solución exacta.',
            'solution_trivial': 'N/A',
            'rank': rank,
            'free_vars': [],
            'particular_solution': 'N/A (inconsistente)',
            'linear_independent': (rank == n),
            'error': 'Sistema inconsistente.'
        }
    
    # Variables libres: columnas sin pivote
    free_vars = [j for j in range(n) if j not in pivot_cols]
    steps.append(f"Variables libres: {free_vars} (dimensión kernel: {len(free_vars)}).")
    
    # Independencia lineal
    linear_independent = (rank == n)
    steps.append(f"Columnas de A linealmente independientes: {linear_independent} (rank == {n}).")
    
    # Solución trivial
    if homogeneous:
        solution_trivial = "x = [0, 0, ..., 0] (triviale, única si rank == n; sino infinitas triviales + no triviales)."
    else:
        solution_trivial = "N/A (no aplica para no homogéneo)."
    
    # Back-substitution para solución (Gauss-Jordan ya está en forma escalonada reducida)
    # Asumimos forma reducida; para particular, asignar 0 a libres
    x_part = [0.0] * n
    for col, row in pivot_cols.items():
        x_part[col] = aug[row][n]
    
    particular_str = f"Solución particular (libres=0): x_p = [{', '.join(f'{v:.4f}' for v in x_part)}]"
    
    num_free = len(free_vars)
    if num_free == 0:
        general_str = f"Solución única: x = [{', '.join(f'{v:.4f}' for v in x_part)}]"
    else:
        # Base del kernel
        kernel_basis = []
        for free_idx, free_col in enumerate(free_vars):
            v = [0.0] * n
            v[free_col] = 1.0
            for col, row in pivot_cols.items():
                v[col] = -aug[row][free_col]
            kernel_basis.append(v)
        
        basis_str = "\n".join([f"v{i+1} = [{', '.join(f'{val:.4f}' for val in basis)}]" for i, basis in enumerate(kernel_basis)])
        general_str = f"Solución general: x = x_p + Σ c_i * v_i (i=1 a {num_free})\nBase del kernel:\n{basis_str}"
    
    # Para sobredeterminado inconsistente, ya manejado arriba
    if m > n and rank < m:
        steps.append("Nota: Sistema sobredeterminado. Si inconsistente, no solución exacta; usa aproximación.")
    
    return {
        'steps': steps,
        'solution_general': general_str,
        'solution_trivial': solution_trivial,
        'rank': rank,
        'free_vars': free_vars,
        'particular_solution': particular_str,
        'linear_independent': linear_independent,
        'error': None
    }
