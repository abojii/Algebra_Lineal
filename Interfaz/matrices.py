import customtkinter as ctk
from tkinter import messagebox

# 🎨 Colores personalizados
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MatrixCalculator(ctk.CTkFrame):  # 👈 ahora hereda de CTkFrame
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_BG)
        self.parent = parent
        self.pack(fill="both", expand=True)

        # Variables
        self.rows_A = ctk.IntVar(value=2)
        self.cols_A = ctk.IntVar(value=2)
        self.rows_B = ctk.IntVar(value=2)
        self.cols_B = ctk.IntVar(value=2)
        self.operation = ctk.StringVar(value="Suma")
    
        title_label = ctk.CTkLabel(self,
                                   text= "Operaciones con Matrices",
                                   font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                                   text_color=COLOR_BUTTON, fg_color="transparent")
        title_label.pack(pady=(10))
        
        # --- Sección de selección de dimensiones ---
        header = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=0)
        header.pack(pady=15, padx=10, fill="x")

        # Fila 1: Selección de tamaños y operación
        ctk.CTkLabel(header, text="Tamaño de Matriz A:", text_color=COLOR_TEXT).grid(row=0, column=0, padx=20, pady=10)
        self.rowsA_menu = ctk.CTkOptionMenu(header, values=[str(i) for i in range(1,6)],
                                            variable=self.rows_A, 
                                            fg_color=COLOR_BUTTON,
                                            width=80)
        self.rowsA_menu.grid(row=0, column=1, padx=2)
        ctk.CTkLabel(header, text="x", text_color=COLOR_TEXT).grid(row=0, column=2)
        
        self.colsA_menu = ctk.CTkOptionMenu(header,
                                            values=[str(i) for i in range(1,6)],
                                            variable=self.cols_A,
                                            width=80,
                                            fg_color=COLOR_BUTTON)
        self.colsA_menu.grid(row=0, column=3, padx=2)

        ctk.CTkLabel(header, text="Tamaño de Matriz B:", text_color=COLOR_TEXT).grid(row=0, column=4, padx=(40,5))
        self.rowsB_menu = ctk.CTkOptionMenu(header, values=[str(i) for i in range(1,6)], 
                                            variable=self.rows_B,
                                            fg_color=COLOR_BUTTON,
                                            width=80)
        self.rowsB_menu.grid(row=0, column=5, padx=2)
        ctk.CTkLabel(header, text="x", text_color=COLOR_TEXT).grid(row=0, column=6)
        
        self.colsB_menu = ctk.CTkOptionMenu(header, values=[str(i) for i in range(1,6)],
                                            variable=self.cols_B,
                                            fg_color=COLOR_BUTTON,
                                            width= 80)
        self.colsB_menu.grid(row=0, column=7, padx=2)

        ctk.CTkLabel(header, text="Operación:", text_color=COLOR_TEXT).grid(row=0, column=8, padx=(40,5))
        self.operation_menu = ctk.CTkOptionMenu(header, 
                                                values=["Suma", "Resta", "Multiplicación por Escalar", "Multiplicación (A x B)"], 
                                                variable=self.operation, 
                                                fg_color=COLOR_BUTTON)
        self.operation_menu.grid(row=0, column=9, padx=5)

        # Fila 2: Botones
        button_frame = ctk.CTkFrame(header, fg_color=COLOR_FRAME)
        button_frame.grid(row=1, column=0, columnspan=5, pady=(10, 10))

        ctk.CTkButton(button_frame, text="Generar", fg_color=COLOR_BUTTON, command=self.generate_matrices).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Resolver", fg_color=COLOR_BUTTON, command=self.solve).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Limpiar", fg_color=COLOR_BUTTON, command=self.clear_all).pack(side="left", padx=10, pady=5)

        # --- Área de matrices ---
        self.matrix_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=0)
        self.matrix_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Resultado ---
        result_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        result_frame.pack(padx=8, pady=10, fill="x")
        ctk.CTkLabel(result_frame, text="Resultado:", text_color=COLOR_TEXT).pack(anchor="w", padx=10, pady=5)
        self.result_box = ctk.CTkTextbox(result_frame, height=150, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
        self.result_box.pack(fill="x", padx=10, pady=5)

        self.entries_A = []
        self.entries_B = []

    # --- Funciones ---
    def generate_matrices(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.entries_A.clear()
        self.entries_B.clear()

        rows_A, cols_A = self.rows_A.get(), self.cols_A.get()
        rows_B, cols_B = self.rows_B.get(), self.cols_B.get()

        frameA = ctk.CTkFrame(self.matrix_frame, fg_color=COLOR_BG)
        frameA.pack(side="left", expand=True, padx=30, pady=10)
        ctk.CTkLabel(frameA, text="Matriz A", text_color=COLOR_SUBTEXT).pack()
        gridA = ctk.CTkFrame(frameA, fg_color=COLOR_BG)
        gridA.pack(pady=5)
        for i in range(rows_A):
            row_entries = []
            for j in range(cols_A):
                e = ctk.CTkEntry(gridA, width=60, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
                e.grid(row=i, column=j, padx=3, pady=3)
                row_entries.append(e)
            self.entries_A.append(row_entries)

        if self.operation.get() != "Multiplicación por Escalar":
            frameB = ctk.CTkFrame(self.matrix_frame, fg_color=COLOR_BG)
            frameB.pack(side="left", expand=True, padx=30, pady=10)
            ctk.CTkLabel(frameB, text="Matriz B", text_color=COLOR_SUBTEXT).pack()
            gridB = ctk.CTkFrame(frameB, fg_color=COLOR_BG)
            gridB.pack(pady=5)
            for i in range(rows_B):
                row_entries = []
                for j in range(cols_B):
                    e = ctk.CTkEntry(gridB, width=60, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
                    e.grid(row=i, column=j, padx=3, pady=3)
                    row_entries.append(e)
                self.entries_B.append(row_entries)
        else:
            frameK = ctk.CTkFrame(self.matrix_frame, fg_color=COLOR_BG)
            frameK.pack(side="left", padx=30)
            ctk.CTkLabel(frameK, text="Escalar k:", text_color=COLOR_SUBTEXT).pack(pady=5)
            self.scalar_entry = ctk.CTkEntry(frameK, width=60, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
            self.scalar_entry.pack()

    def get_matrix(self, entries):
        return [[float(e.get()) for e in row] for row in entries]

    def solve(self):
        op = self.operation.get()
        try:
            A = self.get_matrix(self.entries_A)
            if op != "Multiplicación por Escalar":
                B = self.get_matrix(self.entries_B)
            else:
                k = float(self.scalar_entry.get())

            if op in ["Suma", "Resta"]:
                if len(A) != len(B) or len(A[0]) != len(B[0]):
                    messagebox.showerror("Error", "Las matrices deben tener las mismas dimensiones.")
                    return
            elif op == "Multiplicación (A x B)":
                if len(A[0]) != len(B):
                    messagebox.showerror("Error", "El número de columnas de A debe ser igual al número de filas de B.")
                    return

            if op == "Suma":
                result = [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
            elif op == "Resta":
                result = [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
            elif op == "Multiplicación por Escalar":
                result = [[k * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]
            elif op == "Multiplicación (A x B)":
                result = [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
            else:
                result = []

            self.show_result(result)

        except ValueError:
            messagebox.showerror("Error", "Verifica que todos los valores sean numéricos.")

    def show_result(self, matrix):
        self.result_box.delete("1.0", "end")
        for row in matrix:
            self.result_box.insert("end", "   ".join(f"{val:.2f}" for val in row) + "\n")

    def clear_all(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.result_box.delete("1.0", "end")
        self.entries_A.clear()
        self.entries_B.clear()
