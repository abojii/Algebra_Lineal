import tkinter as tk
from tkinter import ttk, messagebox
import re

class VectorEquationSolver:
    def __init__(self, root):
        self.root = root
        
        # Variables para almacenar datos
        self.num_vectors = tk.IntVar(value=2)
        self.vector_entries = []
        self.b_entry = None
        self.steps_text = None
        self.result_text = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel superior para entradas
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Selector de número de vectores
        ttk.Label(input_frame, text="Número de vectores (n):").grid(row=0, column=0, sticky=tk.W, pady=5)
        num_spinbox = ttk.Spinbox(input_frame, from_=1, to=10, textvariable=self.num_vectors, 
                                 command=self.update_vector_entries, width=10)
        num_spinbox.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Frame para entradas de vectores
        self.vector_frame = ttk.Frame(input_frame)
        self.vector_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Frame para vector b
        ttk.Label(input_frame, text="Vector b (término independiente):").grid(row=2, column=0, sticky=tk.W, pady=5)
        b_frame = ttk.Frame(input_frame)
        b_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.b_entry = ttk.Entry(b_frame, width=30)
        self.b_entry.pack(fill=tk.X)
        self.b_entry.insert(0, "Ej: 1 -2 3")  # Placeholder
        
        # Botón de resolver
        ttk.Button(input_frame, text="Resolver con Pasos Detallados", command=self.solve_detailed).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Botón limpiar (nueva mejora)
        ttk.Button(input_frame, text="Limpiar Entradas", command=self.clear_inputs()).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Panel para resultados y pasos
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Pestaña de resultados
        result_frame = ttk.Frame(notebook)
        notebook.add(result_frame, text="Resultados")
        
        self.result_text = tk.Text(result_frame, height=10, width=80, state=tk.DISABLED, wrap=tk.WORD)
        result_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Pestaña de pasos detallados
        steps_frame = ttk.Frame(notebook)
        notebook.add(steps_frame, text="Pasos Detallados")
        
        self.steps_text = tk.Text(steps_frame, height=15, width=80, state=tk.DISABLED, wrap=tk.WORD)
        steps_scrollbar = ttk.Scrollbar(steps_frame, orient=tk.VERTICAL, command=self.steps_text.yview)
        self.steps_text.configure(yscrollcommand=steps_scrollbar.set)
        
        self.steps_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        steps_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.update_vector_entries()
    
    def clear_inputs(self):
        """Limpia todas las entradas"""
        for entry in self.vector_entries:
            entry.delete(0, tk.END)
            entry.insert(0, "1 -2 3")
        self.b_entry.delete(0, tk.END)
        self.b_entry.insert(0, "1 -2 3")
    
    def update_vector_entries(self):
        # Preservar valores previos si es posible (mejora)
        prev_values = [entry.get() for entry in self.vector_entries]
        
        # Limpiar entradas anteriores
        for widget in self.vector_frame.winfo_children():
            widget.destroy()
        
        self.vector_entries = []
        n = self.num_vectors.get()
        if n == 0:
            return
        
        for i in range(n):
            row_frame = ttk.Frame(self.vector_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(row_frame, text=f"Vector v{i+1}:").pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(row_frame, width=30)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            # Restaurar si hay valor previo
            if i < len(prev_values):
                entry.insert(0, prev_values[i])
            else:
                entry.insert(0, "1 -2 3")  # Placeholder
            self.vector_entries.append(entry)
    
    def parse_vector(self, text, name):
        try:
            # Regex mejorado para flotantes: maneja 1, 1.2, .5, 1., -2.5, incluso 1e-3 (opcional)
            # Preprocesar: reemplazar comas por espacios
            text = re.sub(r'[,\s]+', ' ', text.strip())
            numbers = re.findall(r'-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?', text)
            if not numbers:
                raise ValueError("No se encontraron números")
            vector = [float(x) for x in numbers]
            if len(vector) == 0:
                raise ValueError("Vector vacío")
            return vector
        except ValueError as e:
            messagebox.showerror("Error", f"Error en {name}: debe ser números separados por espacios o comas. Ej: '1 -2 3' o '.5 1.2'")
            return None
        except Exception:
            messagebox.showerror("Error", f"Error al parsear {name}: valor no numérico.")
            return None
    
    def add_step(self, step, is_matrix=False):
        """Añade un paso al área de pasos detallados"""
        if self.steps_text:
            self.steps_text.config(state=tk.NORMAL)
            if is_matrix:
                self.steps_text.insert(tk.END, step + "\n\n")
            else:
                self.steps_text.insert(tk.END, "➜ " + step + "\n\n")
            self.steps_text.config(state=tk.DISABLED)
            self.steps_text.see(tk.END)
    
    def display_matrix(self, matrix, label, is_augmented=False, n_cols_A=None, width=8, prec=3):
        """Formatea y muestra una matriz (nueva función para reducir repetición)"""
        if not matrix:
            return f"{label}: Matriz vacía\n"
        n_rows = len(matrix)
        n_cols = len(matrix[0])
        if n_cols_A is None:
            n_cols_A = n_cols
        display_text = f"{label}:\n"
        for i in range(n_rows):
            display_text += "[ "
            for j in range(n_cols):
                if is_augmented and j == n_cols_A:
                    display_text += "| "
                display_text += f"{matrix[i][j]:{width}.{prec}f} "
            display_text += "]\n"
        return display_text
    
    def compute_rank(self, matrix):
        """Calcula el rango de una matriz usando GE simplificado (sin steps, sin b)"""
        if not matrix or len(matrix) == 0:
            return 0
        
        m = len(matrix)
        n = len(matrix[0])
        A = [row[:] for row in matrix]  # Copia
        
        rank = 0
        col = 0  # Columna actual
        for row in range(m):
            # Encontrar pivote en columna col, desde row
            pivot_row = row
            for j in range(row + 1, m):
                if abs(A[j][col]) > abs(A[pivot_row][col]):
                    pivot_row = j
            
            if abs(A[pivot_row][col]) < 1e-10:
                # No pivote en esta columna, salta a siguiente col
                if col >= n - 1:
                    break
                col += 1
                row -= 1  # Reintenta esta fila en nueva col
                continue
            
            # Intercambio
            A[row], A[pivot_row] = A[pivot_row], A[row]
            
            # Eliminar abajo
            for j in range(row + 1, m):
                if abs(A[row][col]) > 1e-10:
                    factor = A[j][col] / A[row][col]
                    for k in range(col, n):
                        A[j][k] -= factor * A[row][k]
            
            rank += 1
            col += 1
            if col >= n:
                break
        
        return rank
    
    def gaussian_elimination_detailed(self, A, b, show_steps=True):
        """
        Eliminación gaussiana con pivoteo parcial, tracking de pivotes y verificación de consistencia.
        Returns: (solution: list or None, rank: int, pivot_cols: list of pivot columns (or None if inconsistent))
        """
        if not A or len(A) == 0:
            return None, 0, None
        
        n_rows = len(A)
        n_cols = len(A[0])
        Ab = [[A[i][j] for j in range(n_cols)] + [b[i]] for i in range(n_rows)]  # Matriz aumentada
        
        if show_steps:
            self.add_step("Matriz aumentada [A|b]:")
            display_text = self.display_matrix(Ab, "Matriz aumentada [A|b]", is_augmented=True, n_cols_A=n_cols)
            self.add_step(display_text, is_matrix=True)
        
        # Inicializar pivotes: pivot_cols[row] = col del pivote en esa fila, o -1
        pivot_cols = [-1] * n_rows
        current_col = 0
        rank = 0
        
        # Forward elimination con pivoteo
        for row in range(n_rows):
            if current_col >= n_cols:
                break
            
            # Encontrar fila con pivote max en current_col, desde row
            max_row = row
            for j in range(row + 1, n_rows):
                if abs(Ab[j][current_col]) > abs(Ab[max_row][current_col]):
                    max_row = j
            
            # Si pivote ~0, salta columna
            if abs(Ab[max_row][current_col]) < 1e-10:
                if show_steps:
                    self.add_step(f"No pivote en columna {current_col + 1} - posible variable libre")
                current_col += 1
                row -= 1  # Reintenta fila
                continue
            
            # Intercambio si necesario
            if max_row != row:
                Ab[row], Ab[max_row] = Ab[max_row], Ab[row]
                if show_steps:
                    self.add_step(f"Intercambiando fila {row + 1} con fila {max_row + 1}")
                    display_text = self.display_matrix(Ab, f"Después del intercambio", is_augmented=True, n_cols_A=n_cols)
                    self.add_step(display_text, is_matrix=True)
            
            # Registrar pivote
            pivot_cols[row] = current_col
            rank += 1
            
            # Normalizar pivote a 1 (opcional, pero para claridad)
            pivot = Ab[row][current_col]
            if abs(pivot - 1.0) > 1e-10:
                for k in range(current_col, n_cols + 1):
                    Ab[row][k] /= pivot
                if show_steps:
                    self.add_step(f"Normalizando fila {row + 1} dividiendo por {pivot:.3f}")
                    display_text = self.display_matrix(Ab, "Después de normalización", is_augmented=True, n_cols_A=n_cols)
                    self.add_step(display_text, is_matrix=True)
            
            # Eliminar abajo en current_col
            for j in range(row + 1, n_rows):
                factor = Ab[j][current_col]
                if abs(factor) > 1e-10:
                    for k in range(current_col, n_cols + 1):
                        Ab[j][k] -= factor * Ab[row][k]
                    if show_steps:
                        self.add_step(f"Fila {j + 1} -= {factor:.3f} * Fila {row + 1}")
                        display_text = self.display_matrix(Ab, f"Después de eliminación en fila {j + 1}", is_augmented=True, n_cols_A=n_cols)
                        self.add_step(display_text, is_matrix=True)
            
            current_col += 1
        
        if show_steps:
            self.add_step("--- Forma escalonada ---")
            display_text = self.display_matrix(Ab, "Matriz en forma escalonada", is_augmented=True, n_cols_A=n_cols)
            self.add_step(display_text, is_matrix=True)
        
        # Verificar consistencia: filas no pivote (después de rank)
        for i in range(rank, n_rows):
            if abs(Ab[i][n_cols]) > 1e-10:  # b != 0
                # Chequear si fila es toda cero en coefs
                if all(abs(Ab[i][j]) < 1e-10 for j in range(n_cols)):
                    if show_steps:
                        self.add_step(f"Sistema INCONSISTENTE en fila {i + 1}: 0 = {Ab[i][n_cols]:.3f} ≠ 0")
                    return None, rank, None
        
        # Back-substitution usando pivotes
        if show_steps:
            self.add_step("--- Sustitución hacia atrás ---")
        x = [0.0] * n_cols  # Inicial 0 para variables libres
        for i in range(rank - 1, -1, -1):
            col = pivot_cols[i]
            if col == -1:
                continue
            sum_ax = Ab[i][n_cols]
            for j in range(col + 1, n_cols):
                sum_ax -= Ab[i][j] * x[j]
            x[col] = sum_ax / Ab[i][col] if abs(Ab[i][col]) > 1e-10 else sum_ax
            if show_steps:
                self.add_step(f"x_{col + 1} = {x[col]:.3f} (variable en columna {col + 1})")
        
        # Filtrar pivotes válidos
        valid_pivots = [p for p in pivot_cols if p != -1]
        
        if show_steps:
            self.add_step(f"Rango: {rank}")
            pivot_str = ", ".join([str(p + 1) for p in valid_pivots]) if valid_pivots else "Ninguno"
            self.add_step(f"Columnas pivote: {pivot_str}")
        
        return x, rank, valid_pivots
    
    def solve_detailed(self):
        # Limpiar áreas de texto
        if self.steps_text:
            self.steps_text.config(state=tk.NORMAL)
            self.steps_text.delete(1.0, tk.END)
            self.steps_text.config(state=tk.DISABLED)
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # Obtener y validar vectores
        vectors = []
        for i, entry in enumerate(self.vector_entries):
            text = entry.get().strip()
            if not text or text == "Ej: 1 -2 3":
                messagebox.showerror("Error", f"El vector v{i+1} está vacío o no válido")
                return
            vector = self.parse_vector(text, f"v{i+1}")
            if vector is None:
                return
            vectors.append(vector)
        
        # Validar vector b
        b_text = self.b_entry.get().strip()
        if not b_text or b_text == "Ej: 1 -2 3":
            messagebox.showerror("Error", "El vector b está vacío o no válido")
            return
        b = self.parse_vector(b_text, "b")
        if b is None:
            return
        
        # Verificar dimensiones
        if not vectors:
            messagebox.showerror("Error", "No hay vectores")
            return
        dimension = len(vectors[0])
        for i, v in enumerate(vectors):
            if len(v) != dimension:
                messagebox.showerror("Error", f"Todos los vectores deben tener la misma dimensión. v{i+1} tiene {len(v)}, esperado {dimension}")
                return
        if len(b) != dimension:
            messagebox.showerror("Error", f"El vector b debe tener dimensión {dimension}")
            return
        
        try:
            n_vars = len(vectors)
            # Mostrar información inicial
            self.add_step("=== SISTEMA DE ECUACIONES VECTORIALES ===")
            self.add_step(f"Dimensión: R^{dimension}")
            self.add_step(f"Número de vectores/variables: {n_vars}")
            
            # Mostrar el sistema
            self.add_step("\nSistema de ecuaciones:")
            for i in range(dimension):
                eq_terms = [f"c{j+1} * {vectors[j][i]}" for j in range(n_vars)]
                eq = " + ".join(eq_terms)
                self.add_step(f"Ecuación {i+1}: {eq} = {b[i]}")
            
            # Crear matriz A (vectores como columnas)
            A = [[vectors[j][i] for j in range(n_vars)] for i in range(dimension)]
            
            self.add_step("\n=== MATRIZ DEL SISTEMA ===")
            display_text = self.display_matrix(A, "Matriz A (vectores como columnas)")
            self.add_step(display_text, is_matrix=True)
            
            display_text = self.display_matrix([b], "Vector b", width=10)
            self.add_step(display_text, is_matrix=True)
            
            # Calcular rank_A
            rank_A = self.compute_rank(A)
            self.add_step(f"Rango de A: {rank_A}")
            
            # GE en [A|b]
            solution, rank_Ab, pivot_cols = self.gaussian_elimination_detailed(A, b, show_steps=True)
            
            # Determinar tipo
            self.add_step("\n=== ANÁLISIS DE SOLUCIONES ===")
            inconsistent = solution is None
            if inconsistent:
                self.add_step("Sistema INCONSISTENTE: no existe solución")
                self.add_step("El vector b NO puede expresarse como combinación lineal de los vectores dados")
                
                self.result_text.insert(tk.END, "RESULTADO: NO HAY SOLUCIÓN\n")
                self.result_text.insert(tk.END, "="*50 + "\n")
                self.result_text.insert(tk.END, "El sistema es INCONSISTENTE\n")
                self.result_text.insert(tk.END, f"Rango(A) = {rank_A}, Rango([A|b]) = {rank_Ab} (mayor, por inconsistencia)\n")
                self.result_text.insert(tk.END, "El vector b NO es combinación lineal de los vectores dados\n")
                
            elif rank_Ab == n_vars:
                self.add_step("Sistema CONSISTENTE con SOLUCIÓN ÚNICA")
                self.add_step("El vector b SÍ puede expresarse como combinación lineal única de los vectores dados")
                
                self.add_step("\n=== SOLUCIÓN ÚNICA ===")
                
                self.result_text.insert(tk.END, "RESULTADO: SOLUCIÓN ÚNICA\n")
                self.result_text.insert(tk.END, "="*50 + "\n")
                self.result_text.insert(tk.END, "El sistema es CONSISTENTE\n")
                self.result_text.insert(tk.END, f"Rango(A) = Rango([A|b]) = {rank_Ab} = número de variables\n")
                self.result_text.insert(tk.END, "El vector b SÍ es combinación lineal única de los vectores dados\n\n")
                self.result_text.insert(tk.END, "Solución:\n")
                
                for i, ci in enumerate(solution):
                    self.add_step(f"c{i+1} = {ci:.4f}")
                    self.result_text.insert(tk.END, f"c{i+1} = {ci:.4f}\n")
                
                # Mostrar la combinación lineal
                self.result_text.insert(tk.END, "\nCombinación lineal:\n")
                comb = " + ".join([f"({ci:.4f}) * v{i+1}" for i, ci in enumerate(solution)])
                self.result_text.insert(tk.END, f"b = {comb}\n")
                
                # Verificación con tolerancia
                self.result_text.insert(tk.END, "\nVerificación:\n")
                verification = [0.0] * dimension
                for i, ci in enumerate(solution):
                    for j in range(dimension):
                        verification[j] += ci * vectors[i][j]
                
                max_diff = max(abs(v - bb) for v, bb in zip(verification, b))
                self.result_text.insert(tk.END, f"Calculado: {[round(v, 4) for v in verification]}\n")
                self.result_text.insert(tk.END, f"Objetivo:   {[round(bb, 4) for bb in b]}\n")
                
            else:
                # Infinitas soluciones: rank_Ab < n_vars y consistente
                self.add_step("Sistema CONSISTENTE con INFINITAS SOLUCIONES")
                self.add_step("El vector b SÍ puede expresarse como combinación lineal (infinitas formas)")
                num_free = n_vars - rank_Ab
                self.add_step(f"Número de variables libres: {num_free}")
                
                # Identificar variables libres (columnas no pivote)
                free_vars = [i for i in range(n_vars) if i not in pivot_cols]
                free_str = ", ".join([str(f + 1) for f in free_vars])
                self.add_step(f"Variables libres: c{free_str}")
                
                self.result_text.insert(tk.END, "RESULTADO: INFINITAS SOLUCIONES\n")
                self.result_text.insert(tk.END, "="*50 + "\n")
                self.result_text.insert(tk.END, "El sistema es CONSISTENTE\n")
                self.result_text.insert(tk.END, f"Rango(A) = Rango([A|b]) = {rank_Ab} < número de variables = {n_vars}\n")
                self.result_text.insert(tk.END, f"Variables libres: {num_free} (c{free_str})\n")
                self.result_text.insert(tk.END, "El vector b SÍ es combinación lineal de los vectores dados\n\n")
                
                # Solución particular (ya en solution, con libres=0)
                self.result_text.insert(tk.END, "Una solución particular (variables libres = 0):\n")
                for i, ci in enumerate(solution):
                    self.add_step(f"c{i+1} = {ci:.4f}")
                    self.result_text.insert(tk.END, f"c{i+1} = {ci:.4f}\n")
                
                # Combinación lineal
                self.result_text.insert(tk.END, "\nCombinación lineal particular:\n")
                comb = " + ".join([f"({ci:.4f}) * v{i+1}" for i, ci in enumerate(solution)])
                self.result_text.insert(tk.END, f"b = {comb}\n")
                
                # Verificación
                self.result_text.insert(tk.END, "\nVerificación de la solución particular:\n")
                verification = [0.0] * dimension
                for i, ci in enumerate(solution):
                    for j in range(dimension):
                        verification[j] += ci * vectors[i][j]
                
                max_diff = max(abs(v - bb) for v, bb in zip(verification, b))
                self.result_text.insert(tk.END, f"Calculado: {[round(v, 4) for v in verification]}\n")
                self.result_text.insert(tk.END, f"Objetivo:   {[round(bb, 4) for bb in b]}\n")
                
                # Explicación general
                self.result_text.insert(tk.END, f"\nVariables libres c{free_str} pueden tomar cualquier valor real (t_i).\n")
                
                # Ejemplo de otra solución (conceptual, sin cálculo completo para simplicidad)
                if free_vars:
                    first_free = free_vars[0]
                    self.result_text.insert(tk.END, f"\nEjemplo de otra solución (c{first_free + 1} = 1, otras libres = 0):\n")
                    
            
            self.result_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver el sistema: {str(e)}")
            import traceback
            traceback.print_exc()  # Para debug, quita en producción

if __name__ == "__main__":
    root = tk.Tk()
    app = VectorEquationSolver(root)
    root.mainloop()