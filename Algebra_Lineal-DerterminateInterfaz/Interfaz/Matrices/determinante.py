import customtkinter as ctk
from tkinter import messagebox
import numpy as np

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
            return np.array([[float(e.get()) for e in row] for row in self.entries_A])
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
        steps_text = f"--- Método seleccionado: {metodo} ---\n\n"

        if metodo == "Cramer":
            if n > 3:
                messagebox.showwarning("No aplicable", "El método de Cramer solo se usa para matrices pequeñas (2x2 o 3x3).")
                return
            steps_text += self.metodo_cramer(A)

        elif metodo == "Sarrus":
            if n != 3:
                messagebox.showwarning("No aplicable", "La regla de Sarrus solo aplica a matrices 3x3.")
                return
            steps_text += self.regla_sarrus(A)

        elif metodo == "Cofactores":
            steps_text += self.expansion_cofactores(A)

        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", steps_text)

    # --- Método de Cramer (2x2 o 3x3) ---
    def metodo_cramer(self, A):
        n = len(A)
        text = "=== Método de Cramer ===\n"
        if n == 2:
            det = A[0, 0]*A[1, 1] - A[0, 1]*A[1, 0]
            text += f"Det(A) = ({A[0,0]}×{A[1,1]}) - ({A[0,1]}×{A[1,0]}) = {det}\n\n"
        elif n == 3:
            text += self.regla_sarrus(A)
            det = (A[0, 0]*A[1, 1]*A[2, 2] + A[0, 1]*A[1, 2]*A[2, 0] + A[0, 2]*A[1, 0]*A[2, 1]) \
                  - (A[0, 2]*A[1, 1]*A[2, 0] + A[0, 0]*A[1, 2]*A[2, 1] + A[0, 1]*A[1, 0]*A[2, 2])
            text += f"Determinante final (Cramer): {det}\n\n"
        return text

    # --- Regla de Sarrus ---
    def regla_sarrus(self, A):
        if A.shape != (3, 3):
            return "Regla de Sarrus solo aplicable a 3x3.\n"

        text = "=== Regla de Sarrus (3x3) ===\n"
        text += "Se suman los productos de las diagonales principales y se restan las inversas.\n\n"
        d1 = A[0, 0]*A[1, 1]*A[2, 2]
        d2 = A[0, 1]*A[1, 2]*A[2, 0]
        d3 = A[0, 2]*A[1, 0]*A[2, 1]
        i1 = A[0, 2]*A[1, 1]*A[2, 0]
        i2 = A[0, 0]*A[1, 2]*A[2, 1]
        i3 = A[0, 1]*A[1, 0]*A[2, 2]
        det = (d1 + d2 + d3) - (i1 + i2 + i3)

        text += f"Diagonal 1: {A[0,0]}×{A[1,1]}×{A[2,2]} = {d1}\n"
        text += f"Diagonal 2: {A[0,1]}×{A[1,2]}×{A[2,0]} = {d2}\n"
        text += f"Diagonal 3: {A[0,2]}×{A[1,0]}×{A[2,1]} = {d3}\n"
        text += f"Inversas: {i1}, {i2}, {i3}\n"
        text += f"Det(A) = ({d1}+{d2}+{d3}) - ({i1}+{i2}+{i3}) = {det}\n\n"
        return text

    # --- Expansión por Cofactores ---
    def expansion_cofactores(self, A):
        text = "=== Expansión por Cofactores ===\n"
        det, steps = self.det_cofactor(A, 0)
        text += steps
        text += f"\nDeterminante final (Cofactores): {det}\n"
        return text

    def det_cofactor(self, A, nivel):
        n = len(A)
        if n == 1:
            return A[0, 0], f"{'  ' * nivel}Det({A[0,0]}) = {A[0,0]}\n"
        det = 0
        steps = ""
        for j in range(n):
            signo = (-1)**j
            minor = np.delete(np.delete(A, 0, axis=0), j, axis=1)
            subdet, substeps = self.det_cofactor(minor, nivel + 1)
            term = signo * A[0, j] * subdet
            det += term
            steps += f"{'  '*nivel}Cofactor({0},{j}) = (-1)^({0}+{j}) * {A[0,j]} * det(Minor) = {signo} * {A[0,j]} * {subdet} = {term}\n"
            steps += substeps
        return det, steps

    # --- Limpiar todo ---
    def clear_all(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.result_box.delete("1.0", "end")
        self.entries_A.clear()
        self.generate_matrix()