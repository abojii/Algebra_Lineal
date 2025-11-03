import customtkinter as ctk
import sys
import os
from tkinter import messagebox
from Models.solverPropiedadesTranspuesta import verify_transpose_double, verify_transpose_scalar_sum, verify_transpose_sum, verify_transpose_product, verify_transpose_scalar

# Colores personalizados
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MatrixTransposeProperties(ctk.CTkFrame):  # ahora hereda de CTkFrame
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_BG)
        self.parent = parent
        self.pack(fill="both", expand=True)

        # Variables
        self.rows = ctk.IntVar(value=2)
        self.cols = ctk.IntVar(value=2)
        self.k = ctk.DoubleVar(value=2.0)
        self.property = ctk.StringVar(value="(A^T)^T = A")
    
        title_label = ctk.CTkLabel(self,
                                   text="Verificación de Propiedades de la Transpuesta de Matrices",
                                   font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                                   text_color=COLOR_BUTTON, fg_color="transparent")
        title_label.pack(pady=(10))
        
        # --- Sección de selección de dimensiones ---
        header = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=0)
        header.pack(pady=15, padx=10, fill="x")

        # Fila 1: Selección de tamaños y propiedad
        ctk.CTkLabel(header, text="Tamaño de Matrices:", text_color=COLOR_TEXT).grid(row=0, column=0, padx=20, pady=10)
        self.rows_menu = ctk.CTkOptionMenu(header, values=[str(i) for i in range(1,6)],
                                            variable=self.rows, 
                                            fg_color=COLOR_BUTTON,
                                            width=80)
        self.rows_menu.grid(row=0, column=1, padx=2)
        ctk.CTkLabel(header, text="x", text_color=COLOR_TEXT).grid(row=0, column=2)
        
        self.cols_menu = ctk.CTkOptionMenu(header,
                                            values=[str(i) for i in range(1,6)],
                                            variable=self.cols,
                                            width=80,
                                            fg_color=COLOR_BUTTON)
        self.cols_menu.grid(row=0, column=3, padx=2)

        ctk.CTkLabel(header, text="Propiedad:", text_color=COLOR_TEXT).grid(row=0, column=4, padx=(40,5))
        self.property_menu = ctk.CTkOptionMenu(header, 
                                                values=["(A^T)^T = A", "(A + B)^T = A^T + B^T", "(AB)^T = B^T A^T", "(kA)^T = k A^T", "(r(A + B))^T = r(A^T + B^T)"], 
                                                variable=self.property, 
                                                fg_color=COLOR_BUTTON,
                                                width=200)
        self.property_menu.grid(row=0, column=5, padx=5)

        # Fila 2: Escalar (se muestra según la propiedad)
        self.scalar_frame = ctk.CTkFrame(header, fg_color=COLOR_FRAME)
        self.scalar_frame.grid(row=1, column=0, columnspan=6, pady=(10, 10))

        ctk.CTkLabel(self.scalar_frame, text="Escalar k:", text_color=COLOR_TEXT).pack(side="left", padx=10)
        self.k_entry = ctk.CTkEntry(self.scalar_frame, textvariable=self.k, width=80, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
        self.k_entry.pack(side="left", padx=2)

        # Fila 3: Botones
        button_frame = ctk.CTkFrame(header, fg_color=COLOR_FRAME)
        button_frame.grid(row=2, column=0, columnspan=6, pady=(10, 10))

        ctk.CTkButton(button_frame, text="Generar Matrices", fg_color=COLOR_BUTTON, command=self.generate_matrices).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Verificar Propiedad", fg_color=COLOR_BUTTON, command=self.verify_properties).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Limpiar", fg_color=COLOR_BUTTON, command=self.clear_all).pack(side="left", padx=10, pady=5)

        # --- Área de matrices ---
        self.matrix_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=0)
        self.matrix_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Resultado ---
        result_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        result_frame.pack(padx=8, pady=10, fill="x")
        ctk.CTkLabel(result_frame, text="Resultado:", text_color=COLOR_TEXT).pack(anchor="w", padx=10, pady=5)
        self.result_box = ctk.CTkTextbox(result_frame, height=300, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
        self.result_box.pack(fill="x", padx=10, pady=5)

        self.entries_A = []
        self.entries_B = []

    # --- Funciones ---
    def generate_matrices(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.entries_A.clear()
        self.entries_B.clear()

        rows, cols = self.rows.get(), self.cols.get()
        prop = self.property.get()

        # Siempre generar A
        frameA = ctk.CTkFrame(self.matrix_frame, fg_color=COLOR_BG)
        frameA.pack(side="left", expand=True, padx=10, pady=10)
        ctk.CTkLabel(frameA, text="Matriz A", text_color=COLOR_SUBTEXT).pack()
        gridA = ctk.CTkFrame(frameA, fg_color=COLOR_BG)
        gridA.pack(pady=5)
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                e = ctk.CTkEntry(gridA, width=60, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
                e.grid(row=i, column=j, padx=3, pady=3)
                row_entries.append(e)
            self.entries_A.append(row_entries)

        if prop in ["(A + B)^T = A^T + B^T", "(AB)^T = B^T A^T"]:
            # Generar B
            frameB = ctk.CTkFrame(self.matrix_frame, fg_color=COLOR_BG)
            frameB.pack(side="left", expand=True, padx=10, pady=10)
            ctk.CTkLabel(frameB, text="Matriz B", text_color=COLOR_SUBTEXT).pack()
            gridB = ctk.CTkFrame(frameB, fg_color=COLOR_BG)
            gridB.pack(pady=5)
            for i in range(rows):
                row_entries = []
                for j in range(cols):
                    e = ctk.CTkEntry(gridB, width=60, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
                    e.grid(row=i, column=j, padx=3, pady=3)
                    row_entries.append(e)
                self.entries_B.append(row_entries)
        elif prop == "(r(A + B))^T = r(A^T + B^T)":
            # Generar B
            frameB = ctk.CTkFrame(self.matrix_frame, fg_color=COLOR_BG)
            frameB.pack(side="left", expand=True, padx=10, pady=10)
            ctk.CTkLabel(frameB, text="Matriz B", text_color=COLOR_SUBTEXT).pack()
            gridB = ctk.CTkFrame(frameB, fg_color=COLOR_BG)
            gridB.pack(pady=5)
            for i in range(rows):
                row_entries = []
                for j in range(cols):
                    e = ctk.CTkEntry(gridB, width=60, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
                    e.grid(row=i, column=j, padx=3, pady=3)
                    row_entries.append(e)
                self.entries_B.append(row_entries)

                # Mostrar/ocultar escalar según propiedad
                if prop in ["(kA)^T = k A^T", "(r(A + B))^T = r(A^T + B^T)"]:
                    self.scalar_frame.grid(row=1, column=0, columnspan=6, pady=(10, 10))
                else:
                    self.scalar_frame.grid_forget()

    def get_matrix(self, entries):
        return [[float(e.get()) for e in row] for row in entries]

    def verify_properties(self):
        prop = self.property.get()
        try:
            A = self.get_matrix(self.entries_A)
            rows, cols = len(A), len(A[0])

            if prop == "(A^T)^T = A":
                cumple, steps = verify_transpose_double(A)

            elif prop == "(A + B)^T = A^T + B^T":
                B = self.get_matrix(self.entries_B)
                if len(B) != rows or len(B[0]) != cols:
                    messagebox.showerror("Error", "A y B deben tener las mismas dimensiones.")
                    return
                cumple, steps = verify_transpose_sum(A, B)

            elif prop == "(AB)^T = B^T A^T":
                B = self.get_matrix(self.entries_B)
                if cols != len(B):
                    messagebox.showerror("Error", "El número de columnas de A debe ser igual al número de filas de B.")
                    return
                cumple, steps = verify_transpose_product(A, B)

            elif prop == "(kA)^T = k A^T":
                k = self.k.get()
                cumple, steps = verify_transpose_scalar(A, k)
                
            elif prop == "(r(A + B))^T = r(A^T + B^T)":
                B = self.get_matrix(self.entries_B)
                r = self.k.get()  # Usa k como r
                if len(B) != rows or len(B[0]) != cols:
                    messagebox.showerror("Error", "A y B deben tener las mismas dimensiones.")
                    return
                cumple, steps = verify_transpose_scalar_sum(A, B, r)

            self.result_box.delete("1.0", "end")
            self.result_box.insert("end", steps)

        except ValueError:
            messagebox.showerror("Error", "Verifica que todos los valores sean numéricos.")

    def clear_all(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.result_box.delete("1.0", "end")
        self.entries_A.clear()
        self.entries_B.clear()
