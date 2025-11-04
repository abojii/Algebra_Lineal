import customtkinter as ctk
from tkinter import messagebox
from Models.solverDeterminante import DeterminantSolver

# ===== Colores personalizados =====
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"
COLOR_BUTTON1 = "#f87171"
COLOR_BUTTON2 = "#4ade80"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DeterminantCalculator(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_BG)
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.solver = DeterminantSolver()

        # --- Título ---
        title_label = ctk.CTkLabel(self,
                                   text="Cálculo del Determinante",
                                   font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                                   text_color=COLOR_BUTTON)
        title_label.pack(pady=(10))

        # --- Controles superiores ---
        header = ctk.CTkFrame(self, fg_color=COLOR_FRAME)
        header.pack(padx=10, pady=10, fill="x")

        # Tamaño de matriz
        ctk.CTkLabel(header, text="Tamaño de la matriz (n x n):", text_color=COLOR_TEXT).grid(row=0, column=0, padx=10, pady=10)
        self.size_var = ctk.IntVar(value=3)
        self.size_menu = ctk.CTkOptionMenu(header, values=[str(i) for i in range(2, 6)],
                                           variable=self.size_var, fg_color=COLOR_BUTTON,
                                           command=lambda _: self.generate_matrix())
        self.size_menu.grid(row=0, column=1, padx=5)

        # Selección de método
        ctk.CTkLabel(header, text="Método:", text_color=COLOR_TEXT).grid(row=0, column=2, padx=10)
        self.method_var = ctk.StringVar(value="Cofactores")
        self.method_menu = ctk.CTkOptionMenu(header,
                                             values=["Cramer", "Sarrus", "Cofactores"],
                                             variable=self.method_var,
                                             fg_color=COLOR_BUTTON)
        self.method_menu.grid(row=0, column=3, padx=5)

        # Botones
        ctk.CTkButton(header, text="Generar", fg_color=COLOR_BUTTON,
                      command=self.generate_matrix).grid(row=0, column=4, padx=10)
        ctk.CTkButton(header, text="Calcular", fg_color=COLOR_BUTTON2, text_color="black",
                      command=self.solve).grid(row=0, column=5, padx=10)
        ctk.CTkButton(header, text="Limpiar", fg_color=COLOR_BUTTON1,text_color="black",
                      command=self.clear_all).grid(row=0, column=6, padx=10)

        # --- Área de la matriz ---
        self.matrix_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME)
        self.matrix_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Área de resultados ---
        result_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME)
        result_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(result_frame, text="Pasos y resultado:", text_color=COLOR_TEXT).pack(anchor="w", padx=10, pady=5)
        self.result_box = ctk.CTkTextbox(result_frame, height=250, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
        self.result_box.pack(fill="x", padx=10, pady=5)

        self.entries_A = []
        self.generate_matrix()

    # --- Generar campos para la matriz ---
    def generate_matrix(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.entries_A.clear()

        n = self.size_var.get()
        ctk.CTkLabel(self.matrix_frame, text="Matriz A", text_color=COLOR_SUBTEXT).pack(pady=5)
        gridA = ctk.CTkFrame(self.matrix_frame, fg_color=COLOR_BG)
        gridA.pack(pady=5)

        for i in range(n):
            row_entries = []
            for j in range(n):
                e = ctk.CTkEntry(gridA, width=60, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
                e.grid(row=i, column=j, padx=3, pady=3)
                row_entries.append(e)
            self.entries_A.append(row_entries)

    # --- Obtener matriz desde los inputs ---
    def get_matrix(self):
        try:
            return [[float(e.get()) for e in row] for row in self.entries_A]
        except ValueError:
            messagebox.showerror("Error", "Todos los valores deben ser numéricos.")
            return None

    # --- Resolver determinante según método ---
    def solve(self):
        A = self.get_matrix()
        if A is None:
            return

        metodo = self.method_var.get()
        n = len(A)
        self.solver.steps = []  # Limpiar pasos previos
        steps_text = f"--- Método seleccionado: {metodo} ---\n\n"

        if metodo == "Cramer":
            if n > 3:
                messagebox.showwarning("No aplicable", "El método de Cramer solo se usa para matrices pequeñas (2x2 o 3x3).")
                return
            det = self.solver.det_cramer(A)
            steps_text += "\n".join(self.solver.steps) + f"\n\nDeterminante: {det}"

        elif metodo == "Sarrus":
            if n != 3:
                messagebox.showwarning("No aplicable", "La regla de Sarrus solo aplica a matrices 3x3.")
                return
            det = self.solver.det_sarrus(A)
            steps_text += "\n".join(self.solver.steps) + f"\n\nDeterminante: {det}"

        elif metodo == "Cofactores":
            det = self.solver.det_cofactor(A)
            steps_text += "\n".join(self.solver.steps) + f"\n\nDeterminante: {det}"

        # Interpretar invertibilidad
        steps_text += "\n\n" + self.solver.interpret_invertibility(det)

        # Verificar propiedades
        steps_text += "\n\n--- Verificación de Propiedades ---\n"
        if self.solver.check_property1(A):
            steps_text += "Propiedad 1: Sí, una fila o columna es cero.\n"
        else:
            steps_text += "Propiedad 1: No, ninguna fila o columna es cero.\n"

        if self.solver.check_property2(A):
            steps_text += "Propiedad 2: Sí, dos filas o columnas son iguales o proporcionales.\n"
        else:
            steps_text += "Propiedad 2: No, ninguna fila o columna es igual o proporcional.\n"

        if self.solver.check_property3(A):
            steps_text += "Propiedad 3: Sí, intercambiar filas cambia el signo del determinante.\n"
        else:
            steps_text += "Propiedad 3: No, intercambiar filas no cambia el signo.\n"

        if self.solver.check_property4(A):
            steps_text += "Propiedad 4: Sí, multiplicar fila por k multiplica el determinante por k.\n"
        else:
            steps_text += "Propiedad 4: No, multiplicar fila por k no multiplica el determinante por k.\n"

        if self.solver.check_property5(A):
            steps_text += "Propiedad 5: Sí, det(AB) = det(A) * det(B).\n"
        else:
            steps_text += "Propiedad 5: No, det(AB) != det(A) * det(B).\n"

        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", steps_text)

    # --- Limpiar todo ---
    def clear_all(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.result_box.delete("1.0", "end")
        self.entries_A.clear()
        self.generate_matrix()
