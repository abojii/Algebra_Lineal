import tkinter as tk
from tkinter import messagebox, ttk
from Interfaz.vertorequalsolver import VectorEquationSolver
import re

COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

class SubVentanaPrincipal:
    """Sub-ventana principal (la que se muestra por defecto en 'Otra Opción')."""
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg=COLOR_BG)
        
        # Variables para dimensiones
        self.m_var = tk.IntVar(value=2)  # Filas de A
        self.n_var = tk.IntVar(value=2)  # Columnas de A (filas de x)
        
        
        # Frames para secciones
        self.create_dimension_frame()
        self.create_generate_buttons_frame()
        self.matrix_frame = None
        self.vector_frame = None
        self.result_frame = None
        self.result_text = None
        
        # Almacenamiento de entradas
        self.matrix_entries = []
        self.vector_entries = []
        
    def create_dimension_frame(self):
        titulo = tk.Label(self.parent, text= "Matriz-Vector (Ax)",
                          bg= COLOR_BG, fg= COLOR_TEXT,
                          font=("Segoe UI", 14, "bold")).pack(anchor= "center",padx=10,pady=5)
        
        dim_frame = tk.LabelFrame(self.parent,bg= COLOR_FRAME,bd=1,relief="solid", padx=10, pady=10)
        dim_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(dim_frame, text= "Dimenciones",fg= COLOR_TEXT,bg= COLOR_FRAME).grid(row=0, column=0, sticky="w")
        # Filas de matriz
        tk.Label(dim_frame,bg= COLOR_FRAME,fg= COLOR_SUBTEXT,text="Filas de A (m):").grid(row=1, column=0, sticky="w")
        tk.Entry(dim_frame, textvariable=self.m_var, width=5).grid(row=1, column=1)
        
        # Columnas de matriz (filas de vector)
        tk.Label(dim_frame,bg= COLOR_FRAME,fg= COLOR_SUBTEXT, text="Columnas de A / Filas de x (n):").grid(row=2, column=0, sticky="w")
        tk.Entry(dim_frame, textvariable=self.n_var, width=5).grid(row=2, column=1)
        
    def create_generate_buttons_frame(self):
        btn_frame = tk.Frame(self.parent, bg= COLOR_FRAME)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Generar Entradas para Matriz A", command=self.generate_matrix_entries,
                  bg=COLOR_BUTTON).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Generar Entradas para Vector x", command=self.generate_vector_entries,
                  bg=COLOR_BUTTON).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Calcular Ax", command=self.compute_product, bg="lightgreen").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.clear_all, bg="lightcoral").pack(side=tk.LEFT, padx=5)
        
        
    def generate_matrix_entries(self):
        m = self.m_var.get()
        n = self.n_var.get()
        if m <= 0 or n <= 0:
            messagebox.showerror("Error", "Las dimensiones deben ser positivas.")
            return
        
        # Limpiar frame anterior si existe
        if self.matrix_frame:
            self.matrix_frame.destroy()
        self.matrix_entries = []
        
        self.matrix_frame = tk.LabelFrame(self.parent,fg= COLOR_TEXT, text=f"Matriz A ({m} x {n})",bg= COLOR_FRAME,bd= 1, relief= "solid", padx=10, pady=10)
        self.matrix_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        for i in range(m):
            row_entries = []
            for j in range(n):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=1, pady=1)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)
    
    def generate_vector_entries(self):
        n = self.n_var.get()
        if n <= 0:
            messagebox.showerror("Error", "La dimensión n debe ser positiva.")
            return
        
        # Limpiar frame anterior si existe
        if self.vector_frame:
            self.vector_frame.destroy()
        self.vector_entries = []
        
        self.vector_frame = tk.LabelFrame(self.parent, text=f"Vector x ({n} x 1)",
                                          bg= COLOR_FRAME,bd=1,relief="solid", fg= COLOR_TEXT, padx=10, pady=10)
        self.vector_frame.pack(pady=10, padx=10, fill="x")
        
        for i in range(n):
            entry = tk.Entry(self.vector_frame, width=5)
            entry.grid(row=i, column=0, padx=5, pady=1)
            self.vector_entries.append(entry)
    
    def read_matrix(self):
        m = self.m_var.get()
        n = self.n_var.get()
        A = []
        for i in range(m):
            row = []
            for j in range(n):
                val_str = self.matrix_entries[i][j].get().strip()
                if not val_str:
                    messagebox.showerror("Error", f"Elemento A[{i+1}][{j+1}] vacío.")
                    return None
                try:
                    row.append(float(val_str))
                except ValueError:
                    messagebox.showerror("Error", f"Elemento A[{i+1}][{j+1}] no es numérico: {val_str}")
                    return None
            A.append(row)
        return A
    
    def read_vector(self):
        n = self.n_var.get()
        x = []
        for i in range(n):
            val_str = self.vector_entries[i].get().strip()
            if not val_str:
                messagebox.showerror("Error", f"Elemento x[{i+1}] vacío.")
                return None
            try:
                x.append(float(val_str))
            except ValueError:
                messagebox.showerror("Error", f"Elemento x[{i+1}] no es numérico: {val_str}")
                return None
        return x
    
    def compute_product(self):
        A = self.read_matrix()
        if A is None:
            return
        x = self.read_vector()
        if x is None:
            return
        
        m = len(A)
        n = len(A[0])
        if len(x) != n:
            messagebox.showerror("Error", "Las dimensiones no coinciden: columnas de A deben igualar filas de x.")
            return
        
        # Calcular Ax usando regla fila-vector (producto punto por fila)
        result = []
        for i in range(m):
            dot_product = 0.0
            for j in range(n):
                dot_product += A[i][j] * x[j]
            result.append(dot_product)
        
        # Mostrar resultado con paso a paso
        self.display_result(A, x, result)
    
    def display_result(self, A, x, result):
        if self.result_frame:
            self.result_frame.destroy()
        
        self.result_frame = tk.LabelFrame(self.parent, text="Resultado: Producto Matriz-Vector Ax (Paso a Paso)", padx=10, pady=10)
        self.result_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        m = len(A)
        n = len(A[0])
        
        result_text = tk.Text(self.result_frame, height=20, width=80, wrap=tk.WORD)  # Aumenté el tamaño para más contenido
        result_text.pack(fill="both", expand=True)
        
        # Scrollbar para el texto si es necesario
        scrollbar = tk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_text.config(yscrollcommand=scrollbar.set)
        
        result_str = "=== PRODUCTO MATRIZ-VECTOR Ax (Regla Fila-Vector) ===\n\n"
        
        # Mostrar Matriz A
        result_str += "Matriz A (m x n):\n"
        for i in range(m):
            row_str = "  [ "
            for j in range(n):
                row_str += f"{A[i][j]:.6f} "
            row_str += "]\n"
            result_str += row_str
        result_str += "\n"
        
        # Mostrar Vector x
        result_str += "Vector x (n x 1):\n"
        result_str += "  [ "
        for j in range(n):
            result_str += f"{x[j]:.6f} "
            if j < n - 1:
                result_str += "\n    "
        result_str += "]\n\n"
        
        # Paso a paso para cada fila
        result_str += "Cálculo paso a paso (producto punto por fila):\n\n"
        for i in range(m):
            result_str += f"Para el elemento {i+1} del resultado (fila {i+1} de A):\n"
            result_str += f"Fila {i+1} de A: [ "
            for j in range(n):
                result_str += f"{A[i][j]:.6f} "
            result_str += "]\n"
            
            result_str += f"Vector x:      [ "
            for j in range(n):
                result_str += f"{x[j]:.6f} "
            result_str += "]\n\n"
            
            result_str += "Productos individuales (A[i,j] * x[j]):\n"
            products = []
            for j in range(n):
                prod = A[i][j] * x[j]
                products.append(prod)
                result_str += f"  A[{i+1},{j+1}] * x[{j+1}] = {A[i][j]:.6f} * {x[j]:.6f} = {prod:.6f}\n"
            
            # Suma
            total = sum(products)
            result_str += f"\nSuma: {products[0]:.6f}"
            for j in range(1, n):
                result_str += f" + {products[j]:.6f}"
            result_str += f" = {total:.6f}\n\n"
            result_str += f"Por lo tanto, Ax[{i+1}] = {total:.6f}\n\n"
        
        # Vector resultado final
        result_str += "Vector resultado Ax:\n"
        result_str += "Ax = [\n"
        for i, val in enumerate(result):
            result_str += f"  {val:.6f}\n" if i < m - 1 else f"  {val:.6f}\n"
        result_str += "]\n"
        
        result_text.insert(tk.END, result_str)
        result_text.config(state=tk.DISABLED)
    
    def clear_all(self):
        if self.matrix_frame:
            self.matrix_frame.destroy()
        if self.vector_frame:
            self.vector_frame.destroy()
        if self.result_frame:
            self.result_frame.destroy()
        self.matrix_entries = []
        self.vector_entries = []
        # Limpiar entradas de dimensiones si es necesario, pero mantener valores por defecto
        

        

class SubVentana1:
    """Ejemplo de sub-ventana 1 (se abre desde el menú)."""
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg=COLOR_BG)
        
        label = tk.Label(parent, text="Sub-Ventana 1: Contenido Específico",
                         fg=COLOR_TEXT, bg=COLOR_BG, font=("Segoe UI", 16))
        label.pack(pady=20)
        
        tk.Button(parent, text="Volver al Menú Principal (usa el menú arriba)", 
                  bg="#ff6b6b", fg="white", relief="flat").pack(pady=10)
        
        
class SubVentana2:
    """Ejemplo de sub-ventana 2 (se abre desde el menú)."""
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg=COLOR_BG)
        
        label = tk.Label(parent, text="Sub-Ventana 2: Otro Contenido",
                         fg=COLOR_TEXT, bg=COLOR_BG, font=("Segoe UI", 16))
        label.pack(pady=20)
        
        tk.Entry(parent, width=30, bg="#3a3a4f", fg=COLOR_TEXT).pack(pady=10)
        tk.Button(parent, text="Ejemplo de Input", bg="#3b82f6", fg="white", relief="flat").pack(pady=5)
        

class Vectores:
    def __init__(self, parent, show_subframe_callback):
        
        self.parent = parent
        self.parent.configure(bg=COLOR_BG)
        self.show_subframe_callback = show_subframe_callback  # Callback para cambiar sub-frames
        
        # Frame contenedor para sub-contenido (donde se cargan las sub-ventanas)
        self.sub_content_frame = tk.Frame(self.parent, bg=COLOR_BG)
        self.sub_content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Diccionario de sub-frames (se crean lazy, solo cuando se necesitan)
        self.sub_frames = {}
        
        # Mostrar sub-ventana principal por defecto
        self.show_subframe("principal")
        
    def show_subframe(self, name):
        """Muestra/oculta sub-frames dentro de OtherScreen."""
        # Ocultar todos los sub-frames
        for sub_frame in self.sub_frames.values():
            sub_frame.pack_forget()
        
        # Crear si no existe
        if name not in self.sub_frames:
            if name == "principal":
                self.sub_frames[name] = tk.Frame(self.sub_content_frame, bg=COLOR_BG)
                SubVentanaPrincipal(self.sub_frames[name])
            elif name == "sub1":
                self.sub_frames[name] = tk.Frame(self.sub_content_frame, bg=COLOR_BG)
                VectorEquationSolver(self.sub_frames[name])
            elif name == "sub2":
                self.sub_frames[name] = tk.Frame(self.sub_content_frame, bg=COLOR_BG)
                SubVentana2(self.sub_frames[name])
            else:
                return
        
        # Mostrar el seleccionado
        self.sub_frames[name].pack(fill="both", expand=True)
        
        # Llamar callback para actualizar menú en MainApp (opcional, para sincronizar)
        if self.show_subframe_callback:
            self.show_subframe_callback(name)    
        
    