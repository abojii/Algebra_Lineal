import customtkinter as ctk
from tkinter import messagebox
import re  # Mantenido si se usa en otros módulos
from Interfaz.Vectores import propiedadesAlgb_Rn
from Interfaz.Vectores import homogeneo
from constantes import COLOR_BG, COLOR_FRAME, COLOR_TEXT, COLOR_SUBTEXT, COLOR_BUTTON, COLOR_ENTRY  # Import relativo desde config.py
from Interfaz.Vectores import sistema_ecuaciones  # Asumiendo que está en Interfaz/
from Interfaz.Vectores.vertorequalsolver import VectorEquationSolver  # Adáptalo si usa Tkinter
from Interfaz.Vectores.propiedadesAlgb_Rn import VectorAlgebraPropertiesGUI  # Adáptalo si usa Tkinter

class SubVentanaPrincipal:
    """Sub-ventana principal (la que se muestra por defecto en 'Vectores')."""
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color=COLOR_BG)  # Corregido: fg_color en lugar de bg
        
        # Variables para dimensiones
        self.m_var = ctk.IntVar(value=2)  # Filas de A
        self.n_var = ctk.IntVar(value=2)  # Columnas de A (filas de x)
        
        # Frames para secciones
        self.create_dimension_frame()
        self.create_generate_buttons_frame()
        self.matrix_frame = None
        self.vector_frame = None
        self.result_frame = None
        self.result_text = None  # Inicializado como None; se crea en display_result
        
        # Almacenamiento de entradas
        self.matrix_entries = []
        self.vector_entries = []
        
    def create_dimension_frame(self):
        titulo = ctk.CTkLabel(self.parent, text="Matriz-Vector (Ax)",
                              text_color=COLOR_TEXT, fg_color="transparent",
                              font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"))
        titulo.pack(anchor="center", padx=10, pady=5)
        
        dim_frame = ctk.CTkFrame(self.parent, fg_color=COLOR_FRAME, corner_radius=0)
        dim_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(dim_frame, text="Dimensiones", text_color=COLOR_TEXT, fg_color="transparent").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        # Filas de matriz
        ctk.CTkLabel(dim_frame, text="Filas de A (m):", text_color=COLOR_SUBTEXT, fg_color="transparent").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        m_entry = ctk.CTkEntry(dim_frame, textvariable=self.m_var, width=60, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
        m_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Columnas de matriz (filas de vector)
        ctk.CTkLabel(dim_frame, text="Columnas de A / Filas de x (n):", text_color=COLOR_SUBTEXT, fg_color="transparent").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        n_entry = ctk.CTkEntry(dim_frame, textvariable=self.n_var, width=60, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
        n_entry.grid(row=2, column=1, padx=5, pady=5)
        
    def create_generate_buttons_frame(self):
        btn_frame = ctk.CTkFrame(self.parent, fg_color=COLOR_FRAME, corner_radius=0)
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Generar Entradas para Matriz A", command=self.generate_matrix_entries,
                      fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=30).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Generar Entradas para Vector x", command=self.generate_vector_entries,
                      fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=30).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Calcular Ax", command=self.compute_product,
                      fg_color="#4ade80", text_color="black", corner_radius=5, height=30).pack(side="left", padx=5)  # Verde claro para "éxito"
        ctk.CTkButton(btn_frame, text="Limpiar", command=self.clear_all,
                      fg_color="#f87171", text_color="white", corner_radius=5, height=30).pack(side="left", padx=5)  # Rojo claro
        
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
        
        self.matrix_frame = ctk.CTkFrame(self.parent, fg_color=COLOR_FRAME, corner_radius=0)
        ctk.CTkLabel(self.matrix_frame, text=f"Matriz A ({m} x {n})", text_color=COLOR_TEXT, fg_color="transparent",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=5)
        self.matrix_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        grid = ctk.CTkFrame(self.matrix_frame, fg_color=COLOR_FRAME, corner_radius=0)
        grid.pack(pady=5, padx=10)
        
        for i in range(m):
            row_entries = []
            for j in range(n):
                entry = ctk.CTkEntry(grid, width=60, height=30, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT, corner_radius=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
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
        
        self.vector_frame = ctk.CTkFrame(self.parent, fg_color=COLOR_FRAME, corner_radius=0)
        ctk.CTkLabel(self.vector_frame, text=f"Vector x ({n} x 1)", text_color=COLOR_TEXT, fg_color="transparent",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=5)
        self.vector_frame.pack(pady=10, padx=10, fill="x")
        
        grid = ctk.CTkFrame(self.vector_frame, fg_color=COLOR_FRAME, corner_radius=0)
        grid.pack(pady=5, padx=10)
        
        for i in range(n):
            entry = ctk.CTkEntry(grid, width=60, height=30, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT, corner_radius=5)
            entry.grid(row=i, column=0, padx=5, pady=2)
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
                    messagebox.showerror("Error", f"Elemento A[{i+1}][{j+1}] vacío. Llena todas las entradas.")
                    return None
                try:
                    row.append(float(val_str))
                except ValueError:
                    messagebox.showerror("Error", f"Elemento A[{i+1}][{j+1}] no es numérico: '{val_str}'. Usa números (ej. 1.5).")
                    return None
            A.append(row)
        print(f"DEBUG: Matriz A leída correctamente: {A}")  # Depuración opcional
        return A
    
    def read_vector(self):
        n = self.n_var.get()
        x = []
        for i in range(n):
            val_str = self.vector_entries[i].get().strip()
            if not val_str:
                messagebox.showerror("Error", f"Elemento x[{i+1}] vacío. Llena todas las entradas.")
                return None
            try:
                x.append(float(val_str))
            except ValueError:
                messagebox.showerror("Error", f"Elemento x[{i+1}] no es numérico: '{val_str}'. Usa números (ej. 1.5).")
                return None
        print(f"DEBUG: Vector x leído correctamente: {x}")  # Depuración opcional
        return x
    
    def compute_product(self):
        print("DEBUG: Iniciando compute_product")  # Depuración
        A = self.read_matrix()
        if A is None:
            print("DEBUG: Falló lectura de matriz")
            return
        x = self.read_vector()
        if x is None:
            print("DEBUG: Falló lectura de vector")
            return
        
        m = len(A)
        n = len(A[0])
        if len(x) != n:
            messagebox.showerror("Error", f"Las dimensiones no coinciden: columnas de A ({n}) deben igualar filas de x ({len(x)}).")
            return
        
        # Calcular Ax usando regla fila-vector (producto punto por fila)
        result = []
        for i in range(m):
            dot_product = 0.0
            for j in range(n):
                dot_product += A[i][j] * x[j]
            result.append(dot_product)
        
        print(f"DEBUG: Resultado calculado: {result}")  # Depuración
        # Mostrar resultado con paso a paso
        self.display_result(A, x, result)
    
    def display_result(self, A, x, result):
        print("DEBUG: Iniciando display_result")  # Depuración
        if self.result_frame:
            self.result_frame.destroy()

        self.result_frame = ctk.CTkFrame(self.parent, fg_color=COLOR_FRAME, corner_radius=0)
        ctk.CTkLabel(self.result_frame, text="Resultado: Producto Matriz-Vector Ax (Paso a Paso)", 
                     text_color=COLOR_TEXT, fg_color="transparent", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        self.result_frame.pack(pady=10, padx=10, fill="both", expand=True)

        m = len(A)
        n = len(A[0])

        # Crear textbox si no existe
        if self.result_text is None:
            self.result_text = ctk.CTkTextbox(self.result_frame, height=300, fg_color=COLOR_BG, text_color=COLOR_TEXT,
                                              corner_radius=10, scrollbar_button_color=COLOR_BUTTON, scrollbar_button_hover_color=COLOR_BUTTON)
            self.result_text.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            # Limpiar si ya existe
            self.result_text.configure(state="normal")  # Habilitar para editar
            self.result_text.delete("1.0", "end")

        result_str = (
            "=== PRODUCTO MATRIZ-VECTOR Ax (Regla Fila-Vector) ===\n\n"
            "Matriz A (m x n):\n"
        )
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

            result_str += "Vector x:      [ "
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
            result_str += f"  {val:.6f}\n"
        result_str += "]\n"

        # Verificación con b = result (Ax siempre consistente)
        result_str += self.is_linear_combination(A, result) + "\n"
        result_str += "Coeficientes de la combinación: los elementos de x = ["
        for j in range(n):
            result_str += f"{x[j]:.6f}"
            if j < n - 1:
                result_str += ", "
        result_str += "].\n"

        # Insertar y deshabilitar para solo lectura
        self.result_text.insert("end", result_str)
        self.result_text.configure(state="disabled")  # Solo lectura, como en Tkinter
        print("DEBUG: Resultado insertado en textbox")  # Depuración
    
        
    def is_linear_combination(self, A, b):
        m = len(A)
        n = len(A[0])
        if len(b) != m:
            return f"No, dimensiones incompatibles: b debe tener {m} elementos."

        # Matriz aumentada [A | b]
        aug = [A[i][:] + [b[i]] for i in range(m)]

        # Tolerancia numérica para flotantes
        tol = 1e-10

        # Eliminación gaussiana hacia adelante con pivoteo parcial
        row = 0
        col = 0
        while row < m and col < n:
            # Pivoteo: fila con mayor abs en col
            max_row = row
            for k in range(row + 1, m):
                if abs(aug[k][col]) > abs(aug[max_row][col]):
                    max_row = k
            # Intercambio
            aug[row], aug[max_row] = aug[max_row], aug[row]

            # Si pivote ~0, salta col
            if abs(aug[row][col]) < tol:
                col += 1
                continue

            # Eliminar debajo
            for k in range(row + 1, m):
                factor = aug[k][col] / aug[row][col]
                for j in range(col, n + 1):
                    aug[k][j] -= factor * aug[row][j]

            row += 1
            col += 1

        # Verificar consistencia en filas restantes
        for i in range(row, m):
            all_zero = all(abs(aug[i][j]) < tol for j in range(n))
            if all_zero and abs(aug[i][n]) > tol:
                return ":b no es una combinación lineal de las columnas de A (sistema Ax = b inconsistente)."

        return ":b es una combinación lineal de las columnas de A (sistema Ax = b consistente; existe solución x)."

    def clear_all(self):
        if self.matrix_frame:
            self.matrix_frame.destroy()
        if self.vector_frame:
            self.vector_frame.destroy()
        if self.result_frame:
            self.result_frame.destroy()
        self.matrix_entries = []
        self.vector_entries = []
        if self.result_text:
            self.result_text.delete("1.0", "end")


class SubVentana1:
    """Sub-ventana 1: Ecuación Vectorial (placeholder adaptado; integra VectorEquationSolver si está adaptado)."""
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color=COLOR_BG)  # Corregido: fg_color en lugar de bg
        
        titulo = ctk.CTkLabel(self.parent, text="Sub-Ventana 1: Ecuación Vectorial",
                              text_color=COLOR_TEXT, fg_color="transparent",
                              font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"))
        titulo.pack(pady=20)
        
        # Placeholder para contenido (integra aquí VectorEquationSolver si está adaptado a CTk)
        # from .vertorequalsolver import VectorEquationSolver
        # VectorEquationSolver(self.parent)  # Descomenta cuando esté adaptado
        
        descripcion = ctk.CTkLabel(self.parent, text="Contenido para Ecuación Vectorial (en desarrollo).\nUsa el menú lateral para navegar.",
                                   text_color=COLOR_SUBTEXT, fg_color="transparent",
                                   font=ctk.CTkFont(size=12))
        descripcion.pack(pady=10)
        
        volver_btn = ctk.CTkButton(self.parent, text="Volver al Menú Principal",
                                   fg_color="#ff6b6b", text_color="white", corner_radius=5, height=30)
        volver_btn.pack(pady=10)


class SubVentana2:
    """Sub-ventana 2: Propiedades Algebraicas de ℝⁿ (placeholder adaptado; integra VectorAlgebraPropertiesGUI si está adaptado)."""
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color=COLOR_BG)  # Corregido: fg_color en lugar de bg
        
        titulo = ctk.CTkLabel(self.parent, text="Sub-Ventana 2: Propiedades Algebraicas de ℝⁿ",
                              text_color=COLOR_TEXT, fg_color="transparent",
                              font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"))
        titulo.pack(pady=20)
        
        # Placeholder para contenido (integra aquí VectorAlgebraPropertiesGUI si está adaptado a CTk)
        # from .propiedadesAlgb_Rn import VectorAlgebraPropertiesGUI
        # VectorAlgebraPropertiesGUI(self.parent)  # Descomenta cuando esté adaptado
        
        descripcion = ctk.CTkLabel(self.parent, text="Contenido para Propiedades de ℝⁿ (en desarrollo).\nUsa el menú lateral para navegar.",
                                   text_color=COLOR_SUBTEXT, fg_color="transparent",
                                   font=ctk.CTkFont(size=12))
        descripcion.pack(pady=10)
        
        # Ejemplo de input (adaptado)
        entry_ejemplo = ctk.CTkEntry(self.parent, width=300, height=30, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT,
                                      placeholder_text="Ejemplo de entrada...")
        entry_ejemplo.pack(pady=10)
        
        btn_ejemplo = ctk.CTkButton(self.parent, text="Ejemplo de Acción",
                                    fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=30)
        btn_ejemplo.pack(pady=5)


class SubVentana3:
    """Sub-ventana 3: Ecuaciones Homogéneas (placeholder adaptado; integra homogeneo si está adaptado)."""
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color=COLOR_BG)  # Corregido: fg_color en lugar de bg
        
        titulo = ctk.CTkLabel(self.parent, text="Sub-Ventana 3: Ecuaciones Homogéneas",
                              text_color=COLOR_TEXT, fg_color="transparent",
                              font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"))
        titulo.pack(pady=20)
        
        # Placeholder para contenido (integra aquí homogeneo.LinearSystemSolver si está adaptado a CTk)
        # from . import homogeneo
        # homogeneo.LinearSystemSolver(self.parent)  # Descomenta cuando esté adaptado
        
        descripcion = ctk.CTkLabel(self.parent, text="Contenido para Ecuaciones Homogéneas (en desarrollo).\nUsa el menú lateral para navegar.",
                                   text_color=COLOR_SUBTEXT, fg_color="transparent",
                                   font=ctk.CTkFont(size=12))
        descripcion.pack(pady=10)
        
        volver_btn = ctk.CTkButton(self.parent, text="Volver al Menú Principal",
                                   fg_color="#ff6b6b", text_color="white", corner_radius=5, height=30)
        volver_btn.pack(pady=10)


class Vectores:
    def __init__(self, parent, show_subframe_callback):
        self.parent = parent
        self.parent.configure(fg_color=COLOR_BG)  # Corregido: fg_color en lugar de bg
        self.show_subframe_callback = show_subframe_callback  # Callback para cambiar sub-frames
        
        # Frame contenedor para sub-contenido (donde se cargan las sub-ventanas)
        self.sub_content_frame = ctk.CTkFrame(self.parent, fg_color=COLOR_BG, corner_radius=0)
        self.sub_content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Diccionario de sub-frames (se crean lazy, solo cuando se necesitan)
        self.sub_frames = {}
        
        # Mostrar sub-ventana principal por defecto
        self.show_subframe("principal")
        
    def show_subframe(self, name):
        """Muestra/oculta sub-frames dentro de Vectores."""
        # Ocultar todos los sub-frames
        for sub_frame in self.sub_frames.values():
            sub_frame.pack_forget()
        
        # Crear si no existe
        if name not in self.sub_frames:
            if name == "principal":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                SubVentanaPrincipal(self.sub_frames[name])
            elif name == "sub1":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                # VectorEquationSolver(self.sub_frames[name])  # Descomenta cuando esté adaptado
                VectorEquationSolver(self.sub_frames[name])  # Usa placeholder por ahora
            elif name == "sub2":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                # VectorAlgebraPropertiesGUI(self.sub_frames[name])  # Descomenta cuando esté adaptado
                propiedadesAlgb_Rn.VectorAlgebraPropertiesGUI(self.sub_frames[name])  # Usa placeholder por ahora
            elif name == "sub3":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                # homogeneo.LinearSystemSolver(self.sub_frames[name])  # Descomenta cuando esté adaptado
                homogeneo.LinearSystemSolver(self.sub_frames[name])  # Usa placeholder por ahora
            else:
                return
        
        # Mostrar el seleccionado
        self.sub_frames[name].pack(fill="both", expand=True)
        
        # Llamar callback para actualizar menú en MainApp (opcional, para sincronizar)
        if self.show_subframe_callback:
            self.show_subframe_callback(name)

               