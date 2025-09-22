import tkinter as tk
from tkinter import ttk, messagebox
import math

class VectorEquationSolver:
    def __init__(self, root):
        self.root = root
        
        # Variables para almacenar datos
        self.num_vectors = tk.IntVar(value=2)
        self.vector_entries = []
        self.b_entry = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuración de grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Selector de número de vectores
        ttk.Label(main_frame, text="Número de vectores (n):").grid(row=0, column=0, sticky=tk.W, pady=5)
        num_spinbox = ttk.Spinbox(main_frame, from_=1, to=10, textvariable=self.num_vectors, 
                                 command=self.update_vector_entries, width=10)
        num_spinbox.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Frame para entradas de vectores
        self.vector_frame = ttk.Frame(main_frame)
        self.vector_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Frame para vector b
        ttk.Label(main_frame, text="Vector b (término independiente):").grid(row=2, column=0, sticky=tk.W, pady=5)
        b_frame = ttk.Frame(main_frame)
        b_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.b_entry = ttk.Entry(b_frame, width=30)
        self.b_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Botón de resolver
        ttk.Button(main_frame, text="Resolver", command=self.solve).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Área de resultados
        self.result_text = tk.Text(main_frame, height=8, width=50, state=tk.DISABLED)
        self.result_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Scrollbar para el área de resultados
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=4, column=2, sticky=(tk.N, tk.S), pady=5)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.update_vector_entries()
    
    def update_vector_entries(self):
        # Limpiar entradas anteriores
        for widget in self.vector_frame.winfo_children():
            widget.destroy()
        
        self.vector_entries = []
        n = self.num_vectors.get()
        
        for i in range(n):
            ttk.Label(self.vector_frame, text=f"Vector v{i+1}:").grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(self.vector_frame, width=30)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
            self.vector_entries.append(entry)
    
    def parse_vector(self, text, name):
        try:
            vector = [float(x.strip()) for x in text.split()]
            if len(vector) == 0:
                raise ValueError("Vector vacío")
            return vector
        except ValueError as e:
            messagebox.showerror("Error", f"Error en {name}: debe ser números separados por espacios")
            return None
    
    # Operaciones vectoriales y matriciales manuales
    def vector_add(self, v1, v2):
        return [v1[i] + v2[i] for i in range(len(v1))]
    
    def vector_scale(self, v, scalar):
        return [scalar * x for x in v]
    
    def dot_product(self, v1, v2):
        return sum(v1[i] * v2[i] for i in range(len(v1)))
    
    def matrix_multiply(self, A, B):
        # Multiplicación de matrices A*B
        rows_A = len(A)
        cols_A = len(A[0])
        rows_B = len(B)
        cols_B = len(B[0])
        
        if cols_A != rows_B:
            raise ValueError("Dimensiones incompatibles para multiplicación")
        
        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
        
        return result
    
    def transpose(self, matrix):
        # Transponer una matriz
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    
    def gaussian_elimination(self, A, b):
        # Implementación manual de eliminación gaussiana
        n = len(A)
        
        # Crear matriz aumentada
        Ab = [A[i] + [b[i]] for i in range(n)]
        
        # Eliminación hacia adelante
        for i in range(n):
            # Pivoteo parcial
            max_row = i
            for j in range(i+1, n):
                if abs(Ab[j][i]) > abs(Ab[max_row][i]):
                    max_row = j
            Ab[i], Ab[max_row] = Ab[max_row], Ab[i]
            
            # Hacer cero los elementos debajo del pivote
            for j in range(i+1, n):
                factor = Ab[j][i] / Ab[i][i] if Ab[i][i] != 0 else 0
                for k in range(i, n+1):
                    Ab[j][k] -= factor * Ab[i][k]
        
        # Sustitución hacia atrás
        x = [0] * n
        for i in range(n-1, -1, -1):
            if Ab[i][i] == 0:
                if Ab[i][n] != 0:
                    return None  # Sistema inconsistente
                else:
                    return []  # Infinitas soluciones
            
            x[i] = Ab[i][n] / Ab[i][i]
            for j in range(i-1, -1, -1):
                Ab[j][n] -= Ab[j][i] * x[i]
        
        return x
    
    def matrix_rank(self, matrix):
        # Calcular el rango de una matriz usando eliminación gaussiana
        if not matrix:
            return 0
        
        m = len(matrix)
        n = len(matrix[0])
        
        # Crear copia para no modificar la original
        A = [row[:] for row in matrix]
        
        rank = 0
        for i in range(min(m, n)):
            # Encontrar pivote
            pivot_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[pivot_row][i]):
                    pivot_row = j
            
            if abs(A[pivot_row][i]) < 1e-10:  # Cero con tolerancia
                continue
            
            # Intercambiar filas
            A[i], A[pivot_row] = A[pivot_row], A[i]
            rank += 1
            
            # Eliminar elementos debajo del pivote
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
        
        return rank
    
    def solve(self):
        # Obtener y validar vectores
        vectors = []
        for i, entry in enumerate(self.vector_entries):
            text = entry.get()
            if not text.strip():
                messagebox.showerror("Error", f"El vector v{i+1} está vacío")
                return
            vector = self.parse_vector(text, f"v{i+1}")
            if vector is None:
                return
            vectors.append(vector)
        
        # Validar vector b
        b_text = self.b_entry.get()
        if not b_text.strip():
            messagebox.showerror("Error", "El vector b está vacío")
            return
        b = self.parse_vector(b_text, "b")
        if b is None:
            return
        
        # Verificar que todos los vectores tengan la misma dimensión
        dimension = len(vectors[0])
        for i, v in enumerate(vectors):
            if len(v) != dimension:
                messagebox.showerror("Error", f"Todos los vectores deben tener la misma dimensión. v{i+1} tiene dimensión {len(v)}")
                return
        if len(b) != dimension:
            messagebox.showerror("Error", f"El vector b debe tener dimensión {dimension}")
            return
        
        try:
            # Crear matriz A (vectores como columnas)
            A = [[vectors[j][i] for j in range(len(vectors))] for i in range(dimension)]
            
            # Calcular rangos
            rank_A = self.matrix_rank([row[:] for row in A])
            
            # Matriz aumentada [A|b]
            A_augmented = [A[i] + [b[i]] for i in range(dimension)]
            rank_Ab = self.matrix_rank(A_augmented)
            
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            
            self.result_text.insert(tk.END, "Sistema de ecuaciones:\n")
            for i in range(dimension):
                eq = " + ".join([f"c{j+1}*{vectors[j][i]}" for j in range(len(vectors))])
                self.result_text.insert(tk.END, f"{eq} = {b[i]}\n")
            self.result_text.insert(tk.END, "\n" + "="*50 + "\n\n")
            
            if rank_A < rank_Ab:
                self.result_text.insert(tk.END, "Resultado: NO hay solución\n")
                self.result_text.insert(tk.END, "El sistema es inconsistente\n")
            elif rank_A == len(vectors):
                self.result_text.insert(tk.END, "Resultado: Solución ÚNICA\n")
                # Resolver sistema
                if dimension == len(vectors):  # Sistema cuadrado
                    solution = self.gaussian_elimination(A, b)
                    if solution is None:
                        self.result_text.insert(tk.END, "Error al resolver el sistema\n")
                    elif solution == []:
                        self.result_text.insert(tk.END, "Infinitas soluciones\n")
                    else:
                        for i, ci in enumerate(solution):
                            self.result_text.insert(tk.END, f"c{i+1} = {ci:.4f}\n")
                else:
                    self.result_text.insert(tk.END, "Sistema no cuadrado, usando método de mínimos cuadrados aproximado\n")
                    # Aproximación simple para sistemas no cuadrados
                    A_transpose = self.transpose(A)
                    ATA = self.matrix_multiply(A_transpose, A)
                    ATb = [sum(A_transpose[i][j] * b[j] for j in range(dimension)) for i in range(len(vectors))]
                    
                    try:
                        solution = self.gaussian_elimination(ATA, ATb)
                        if solution is not None and solution != []:
                            for i, ci in enumerate(solution):
                                self.result_text.insert(tk.END, f"c{i+1} = {ci:.4f}\n")
                        else:
                            self.result_text.insert(tk.END, "No se pudo encontrar solución única\n")
                    except:
                        self.result_text.insert(tk.END, "Error en el cálculo de mínimos cuadrados\n")
            else:
                self.result_text.insert(tk.END, "Resultado: INFINITAS soluciones\n")
                self.result_text.insert(tk.END, "El sistema tiene variables libres\n")
                
                # Intentar encontrar una solución particular
                try:
                    A_transpose = self.transpose(A)
                    ATA = self.matrix_multiply(A_transpose, A)
                    ATb = [sum(A_transpose[i][j] * b[j] for j in range(dimension)) for i in range(len(vectors))]
                    
                    solution = self.gaussian_elimination(ATA, ATb)
                    if solution is not None and solution != []:
                        self.result_text.insert(tk.END, "\nUna solución particular:\n")
                        for i, ci in enumerate(solution):
                            self.result_text.insert(tk.END, f"c{i+1} = {ci:.4f}\n")
                except:
                    self.result_text.insert(tk.END, "No se pudo calcular una solución particular\n")
            
            self.result_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver el sistema: {str(e)}")
