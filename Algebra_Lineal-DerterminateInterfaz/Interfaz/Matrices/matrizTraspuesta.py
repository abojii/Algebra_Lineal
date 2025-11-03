import customtkinter as ctk
from tkinter import messagebox

# ======= COLORES (iguales que tus otras interfaces) =======
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

class MatrixTranspose(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_BG)
        self.parent = parent

        # ======= TÍTULO =======
        title_label = ctk.CTkLabel(
            self,
            text="Matriz Traspuesta",
            text_color=COLOR_TEXT,
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(15, 10))

        subtitle_label = ctk.CTkLabel(
            self,
            text="Ingresa una matriz para calcular su traspuesta",
            text_color=COLOR_SUBTEXT,
            font=("Arial", 14)
        )
        subtitle_label.pack(pady=(0, 20))

        # ======= SECCIÓN DE TAMAÑO =======
        size_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        size_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(size_frame, text="Filas:", text_color=COLOR_TEXT).pack(side="left", padx=5)
        self.rows_menu = ctk.CTkOptionMenu(size_frame, values=[str(i) for i in range(1, 7)], width=80, height=28, font=("Arial", 12))
        self.rows_menu.pack(side="left", padx=5)

        ctk.CTkLabel(size_frame, text="Columnas:", text_color=COLOR_TEXT).pack(side="left", padx=5)
        self.cols_menu = ctk.CTkOptionMenu(size_frame, values=[str(i) for i in range(1, 7)], width=80, height=28, font=("Arial", 12))
        self.cols_menu.pack(side="left", padx=5)

        self.generate_button = ctk.CTkButton(size_frame, text="Generar", command=self.generate_matrix, width=90, height=32, fg_color=COLOR_BUTTON)
        self.generate_button.pack(side="left", padx=15)

        # ======= MATRIZ ORIGINAL =======
        self.matrix_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        self.matrix_frame.pack(padx=20, pady=15)

        # ======= BOTONES DE ACCIÓN =======
        action_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        action_frame.pack(pady=5)

        self.solve_button = ctk.CTkButton(action_frame, text="Calcular Traspuesta", command=self.calculate_transpose, width=150, height=32, fg_color="#22c55e")
        self.solve_button.pack(side="left", padx=10)

        self.clear_button = ctk.CTkButton(action_frame, text="Limpiar", command=self.clear_all, width=90, height=32, fg_color="#ef4444")
        self.clear_button.pack(side="left", padx=10)

        # ======= RESULTADOS =======
        self.result_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        self.result_frame.pack(padx=20, pady=15, fill="x")

        self.matrix_entries = []
        self.result_labels = []

    # ======= GENERAR MATRIZ =======
    def generate_matrix(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        rows = int(self.rows_menu.get())
        cols = int(self.cols_menu.get())
        self.matrix_entries = []

        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ctk.CTkEntry(self.matrix_frame, width=60, height=30, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT, justify="center")
                entry.grid(row=i, column=j, padx=3, pady=3)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

    # ======= CALCULAR TRASPUESTA =======
    def calculate_transpose(self):
        if not self.matrix_entries:
            messagebox.showerror("Error", "Primero genera e ingresa la matriz.")
            return

        try:
            matrix = [[float(entry.get()) for entry in row] for row in self.matrix_entries]
        except ValueError:
            messagebox.showerror("Error", "Todos los elementos deben ser numéricos.")
            return

        transpose = list(map(list, zip(*matrix)))

        # Mostrar resultado
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.result_frame, text="Matriz Traspuesta:", text_color=COLOR_TEXT, font=("Arial", 16, "bold")).pack(pady=(10, 5))

        result_matrix_frame = ctk.CTkFrame(self.result_frame, fg_color=COLOR_FRAME)
        result_matrix_frame.pack(pady=10)

        for i, row in enumerate(transpose):
            for j, val in enumerate(row):
                lbl = ctk.CTkLabel(result_matrix_frame, text=str(val), text_color=COLOR_TEXT, width=60, height=30, font=("Arial", 13), fg_color=COLOR_ENTRY)
                lbl.grid(row=i, column=j, padx=3, pady=3)

        # Verificar propiedades
        self.check_properties(matrix, transpose)

    # ======= PROPIEDADES =======
    def check_properties(self, matrix, transpose):
        rows, cols = len(matrix), len(matrix[0])

        is_square = rows == cols
        is_symmetric = is_square and all(matrix[i][j] == matrix[j][i] for i in range(rows) for j in range(cols))

        info = f"Dimensiones originales: {rows}x{cols}\n"
        info += f"Dimensiones traspuesta: {cols}x{rows}\n\n"
        info += f"¿Matriz cuadrada?: {'Sí' if is_square else 'No'}\n"
        info += f"¿Matriz simétrica (A = Aᵀ)?: {'Sí' if is_symmetric else 'No'}"

        ctk.CTkLabel(self.result_frame, text=info, text_color=COLOR_SUBTEXT, font=("Arial", 13)).pack(pady=10)

    # ======= LIMPIAR =======
    def clear_all(self):
        for frame in [self.matrix_frame, self.result_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
        self.matrix_entries = []
