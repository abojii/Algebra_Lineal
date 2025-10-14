import customtkinter as ctk
from tkinter import messagebox
import re

# Configuración de CustomTkinter
ctk.set_appearance_mode("light")  # Modos: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

class MatrixMultiplier(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Multiplicación de Matrices")
        self.geometry("900x800")  # Tamaño para mejor visibilidad
        self.resizable(True, True)

        # Variables para tamaños
        self.rows_a_var = ctk.StringVar(value="2")
        self.cols_a_var = ctk.StringVar(value="2")  # También será rows_b
        self.cols_b_var = ctk.StringVar(value="2")

        # Listas para almacenar entradas
        self.entries_a = []
        self.entries_b = []

        # Frame principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        self.setup_ui()

    def setup_ui(self):
        # Título
        titulo = ctk.CTkLabel(self.main_frame, text="Calculadora de Multiplicación de Matrices A × B",
                              font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=20)

        subtitulo = ctk.CTkLabel(self.main_frame, text="Ingresa las matrices A (m×n) y B (n×p) para calcular el producto C = A × B",
                                 font=ctk.CTkFont(size=10))
        subtitulo.pack(pady=(0, 20))

        # Frame de configuración
        config_frame = ctk.CTkFrame(self.main_frame)
        config_frame.pack(fill="x", padx=20, pady=10)

        # Etiquetas y combos para tamaños
        ctk.CTkLabel(config_frame, text="Filas de A (m):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        rows_a_combo = ctk.CTkComboBox(config_frame, values=["2", "3", "4"], variable=self.rows_a_var, width=60)
        rows_a_combo.grid(row=0, column=1, padx=5, pady=10)

        ctk.CTkLabel(config_frame, text="Columnas de A / Filas de B (n):").grid(row=0, column=2, padx=10, pady=10, sticky="w")
        cols_a_combo = ctk.CTkComboBox(config_frame, values=["2", "3", "4"], variable=self.cols_a_var, width=60)
        cols_a_combo.grid(row=0, column=3, padx=5, pady=10)

        ctk.CTkLabel(config_frame, text="Columnas de B (p):").grid(row=0, column=4, padx=10, pady=10, sticky="w")
        cols_b_combo = ctk.CTkComboBox(config_frame, values=["2", "3", "4"], variable=self.cols_b_var, width=60)
        cols_b_combo.grid(row=0, column=5, padx=5, pady=10)

        # Botones (con referencias directas)
        self.generate_btn = ctk.CTkButton(config_frame, text="Generar Campos", command=self.generar_campos, width=100)
        self.generate_btn.grid(row=0, column=6, padx=10, pady=10)

        self.multiply_btn = ctk.CTkButton(config_frame, text="Multiplicar", command=self.multiplicar, width=100, state="disabled")
        self.multiply_btn.grid(row=0, column=7, padx=5, pady=10)

        self.clear_btn = ctk.CTkButton(config_frame, text="Limpiar", command=self.limpiar, width=100)
        self.clear_btn.grid(row=0, column=8, padx=10, pady=10)

        # Frame para matriz A
        self.frame_a = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_a.pack(fill="both", padx=20, pady=10, expand=True)

        label_a = ctk.CTkLabel(self.frame_a, text="Matriz A (m × n):", font=ctk.CTkFont(weight="bold"))
        label_a.pack(pady=(10, 5))

        self.entries_a_frame = ctk.CTkScrollableFrame(self.frame_a)
        self.entries_a_frame.pack(fill="both", expand=True, pady=5)

        # Frame para matriz B
        self.frame_b = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_b.pack(fill="both", padx=20, pady=10, expand=True)

        label_b = ctk.CTkLabel(self.frame_b, text="Matriz B (n × p):", font=ctk.CTkFont(weight="bold"))
        label_b.pack(pady=(10, 5))

        self.entries_b_frame = ctk.CTkScrollableFrame(self.frame_b)
        self.entries_b_frame.pack(fill="both", expand=True, pady=5)

        # Frame para resultado
        self.result_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.result_frame.pack(fill="both", padx=20, pady=10, expand=True)

        # Label de estado (arriba, para depuración)
        self.status_label = ctk.CTkLabel(self.result_frame, text="Estado: Listo para generar campos.", 
                                         font=ctk.CTkFont(size=10), anchor="w")
        self.status_label.pack(pady=(10, 0), fill="x")

        # Label para resultados (en la parte inferior del frame)
        self.result_label = ctk.CTkLabel(self.result_frame, text="", 
                                         font=ctk.CTkFont(size=12), 
                                         justify="left", wraplength=800,  # Envuelve el texto para legibilidad
                                         anchor="w")
        self.result_label.pack(pady=10, anchor="s", fill="x")  # Anclado al sur (inferior) del frame

    def generar_campos(self):
        try:
            m = int(self.rows_a_var.get())
            n = int(self.cols_a_var.get())
            p = int(self.cols_b_var.get())

            if m < 2 or m > 4 or n < 2 or n > 4 or p < 2 or p > 4:
                messagebox.showerror("Error", "Tamaños deben ser entre 2 y 4.")
                return

            # Limpiar campos anteriores
            self.limpiar_campos()

            # Generar entradas para A (m x n)
            self.entries_a = []
            for i in range(m):
                row_entries = []
                for j in range(n):
                    entry = ctk.CTkEntry(self.entries_a_frame, width=60, height=30, placeholder_text=f"a{i+1}{j+1}")
                    entry.grid(row=i, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.entries_a.append(row_entries)

            # Generar entradas para B (n x p)
            self.entries_b = []
            for i in range(n):
                row_entries = []
                for j in range(p):
                    entry = ctk.CTkEntry(self.entries_b_frame, width=60, height=30, placeholder_text=f"b{i+1}{j+1}")
                    entry.grid(row=i, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.entries_b.append(row_entries)

            # Habilitar botón de multiplicar
            self.multiply_btn.configure(state="normal")

            self.result_label.configure(text="Campos generados. Ingresa los valores y haz clic en 'Multiplicar'.")
            self.status_label.configure(text=f"Estado: Campos generados para A ({m}x{n}) y B ({n}x{p}). Llena todos los campos.")

            print(f"Campos generados: A {m}x{n}, B {n}x{p}")  # Debug en consola

        except ValueError:
            messagebox.showerror("Error", "Selecciona tamaños válidos.")
            self.status_label.configure(text="Estado: Error en tamaños.")

    def limpiar_campos(self):
        # Limpiar entradas A
        for row in self.entries_a:
            for entry in row:
                entry.destroy()
        self.entries_a = []

        # Limpiar entradas B
        for row in self.entries_b:
            for entry in row:
                entry.destroy()
        self.entries_b = []

        # Deshabilitar botón multiplicar
        self.multiply_btn.configure(state="disabled")

    def limpiar(self):
        self.limpiar_campos()
        self.result_label.configure(text="")
        self.status_label.configure(text="Estado: Limpiado. Listo para generar nuevos campos.")
        # Resetear combos
        self.rows_a_var.set("2")
        self.cols_a_var.set("2")
        self.cols_b_var.set("2")
        print("Todo limpiado.")  # Debug

    def get_matrix_values(self, entries, matrix_name):
        if not entries:
            messagebox.showerror("Error", f"No hay campos generados para {matrix_name}.")
            return None

        matrix = []
        for i, row in enumerate(entries):
            row_vals = []
            for j, entry in enumerate(row):
                val_str = entry.get().strip()
                if not val_str:
                    messagebox.showerror("Error", f"Campo vacío en {matrix_name}[{i+1}][{j+1}]. Llena todos los valores.")
                    self.status_label.configure(text=f"Estado: Error - Campo vacío en {matrix_name}.")
                    return None
                try:
                    # Soporte para fracciones simples como 1/2
                    if '/' in val_str:
                        parts = val_str.split('/')
                        if len(parts) != 2:
                            raise ValueError("Fracción inválida")
                        num, den = map(float, parts)
                        if den == 0:
                            raise ValueError("Denominador cero")
                        row_vals.append(num / den)
                    else:
                        row_vals.append(float(val_str))
                except ValueError as e:
                    messagebox.showerror("Error", f"Valor inválido en {matrix_name}[{i+1}][{j+1}]: '{entry.get()}'. Usa números o fracciones (ej: 1/2).")
                    self.status_label.configure(text=f"Estado: Error - Valor inválido en {matrix_name}.")
                    return None
            matrix.append(row_vals)
        print(f"{matrix_name} leída correctamente: {matrix}")  # Debug
        return matrix

    def multiplicar(self):
        print("Botón Multiplicar presionado.")  # Debug

        if not self.entries_a or not self.entries_b:
            messagebox.showerror("Error", "Genera los campos primero.")
            self.status_label.configure(text="Estado: Error - Genera campos primero.")
            return

        self.status_label.configure(text="Estado: Leyendo matrices...")

        A = self.get_matrix_values(self.entries_a, "A")
        if A is None:
            return

        B = self.get_matrix_values(self.entries_b, "B")
        if B is None:
            return

        # Verificar dimensiones
        if len(A[0]) != len(B):
            messagebox.showerror("Error", f"Dimensiones incompatibles: A tiene {len(A[0])} columnas, B tiene {len(B)} filas.")
            self.status_label.configure(text="Estado: Error - Dimensiones incompatibles.")
            return

        self.status_label.configure(text="Estado: Calculando multiplicación...")

        C = self.multiplicar_matrices(A, B)

        # Mostrar resultado en el label (formateado con saltos de línea)
        result_text = "=== RESULTADO: Matriz C (m × p) ===\n\n"
        m_result = len(C)
        p_result = len(C[0]) if m_result > 0 else 0
        result_text += f"Dimensiones de C: {m_result} × {p_result}\n\n"
        for i, row in enumerate(C):
            formatted_row = " | ".join([f"{val:.4f}" for val in row])  # 4 decimales para precisión
            result_text += f"Fila {i+1}: {formatted_row}\n"
        result_text += "\n=== Cálculo completado ==="
        
        self.result_label.configure(text=result_text)
        self.status_label.configure(text="Estado: Cálculo exitoso. Revisa el resultado abajo.")
        messagebox.showinfo("Éxito", "Multiplicación completada. Revisa el resultado en la ventana.")
        print(f"Resultado C: {C}")  # Debug en consola

    def multiplicar_matrices(self, A, B):
        m = len(A)
        n = len(A[0])
        p = len(B[0])

        C = [[0.0 for _ in range(p)] for _ in range(m)]

        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]

        return C

if __name__ == "__main__":
    app = MatrixMultiplier()
    app.mainloop()
