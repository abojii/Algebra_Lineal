moimport customtkinter as ctk
from tkinter import messagebox
from Models.solverMatrizInversa import gauss_jordan_inverse, check_theoretical_properties
from Models.solverrelacioninversa import InverseRelationSolver
from Models.solverdeterminante import DeterminantSolver
from fractions import Fraction
# Configuración de CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Definición de colores
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

class MatrixInverseApp(ctk.CTkFrame):  # Cambia CTk por CTkFrame
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_BG)  # Llama al constructor de CTkFrame
        self.parent = parent
        self.pack(fill="both", expand=True)

        self.size_entry = None
        self.entries_a = []
        self.inverse_solver = InverseRelationSolver(DeterminantSolver())

        self.setup_ui()

    def setup_ui(self):
        titulo = ctk.CTkLabel(
            self,
            text="Calculadora de Inversa de Matriz Cuadrada (Gauss-Jordan)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXT  # Color del texto
        )
        titulo.pack(pady=20)

        subtitulo = ctk.CTkLabel(
            self,
            text="Ingresa la matriz cuadrada A (n×n) para calcular su inversa y verificar propiedades",
            font=ctk.CTkFont(size=10),
            text_color=COLOR_SUBTEXT  # Color del subtítulo
        )
        subtitulo.pack(pady=(0, 20))

        config_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME)  # Color del frame de configuración
        config_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(config_frame, text="Tamaño de la matriz (n):", text_color=COLOR_TEXT).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.size_entry = ctk.CTkEntry(config_frame, width=60, placeholder_text="n", fg_color=COLOR_ENTRY)  # Color de entrada
        self.size_entry.grid(row=0, column=1, padx=5, pady=10)
        self.size_entry.insert(0, "2")

        self.generate_btn = ctk.CTkButton(config_frame, text="Generar Campos", command=self.generar_campos, width=100, fg_color=COLOR_BUTTON)  # Color del botón
        self.generate_btn.grid(row=0, column=2, padx=10, pady=10)

        self.calculate_btn = ctk.CTkButton(config_frame, text="Calcular Inversa", command=self.calcular_inversa, width=100, state="disabled", fg_color=COLOR_BUTTON)  # Color del botón
        self.calculate_btn.grid(row=0, column=3, padx=5, pady=10)

        self.clear_btn = ctk.CTkButton(config_frame, text="Limpiar", command=self.limpiar, width=100, fg_color=COLOR_BUTTON)  # Color del botón
        self.clear_btn.grid(row=0, column=4, padx=10, pady=10)

        self.frame_a = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_a.pack(fill="both", padx=20, pady=10, expand=True)

        label_a = ctk.CTkLabel(self.frame_a, text="Matriz A (n × n):", font=ctk.CTkFont(weight="bold"), text_color=COLOR_TEXT)
        label_a.pack(pady=(10, 5))

        self.entries_a_frame = ctk.CTkScrollableFrame(self.frame_a, fg_color=COLOR_FRAME)  # Color del frame de entradas
        self.entries_a_frame.pack(fill="both", expand=True, pady=5)

        self.result_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.result_frame.pack(fill="both", padx=20, pady=10, expand=True)

        self.status_label = ctk.CTkLabel(self.result_frame, text="Estado: Listo para generar campos.", 
                                         font=ctk.CTkFont(size=10), anchor="w", text_color=COLOR_SUBTEXT)
        self.status_label.pack(pady=(10, 0), fill="x")

        self.result_textbox = ctk.CTkTextbox(self.result_frame, wrap="word", font=ctk.CTkFont(size=12), fg_color=COLOR_ENTRY)  # Color del textbox
        self.result_textbox.pack(pady=10, fill="both", expand=True)

    def generar_campos(self):
        try:
            n_str = self.size_entry.get().strip()
            if not n_str:
                messagebox.showerror("Error", "Ingresa un tamaño válido.")
                return
            n = int(n_str)

            if n < 2:
                messagebox.showerror("Error", "Tamaño debe ser al menos 2.")
                return

            self.limpiar_campos()
            self.entries_a = []
            for i in range(n):
                row_entries = []
                for j in range(n):
                    entry = ctk.CTkEntry(self.entries_a_frame, width=60, height=30, placeholder_text=f"a{i+1}{j+1}")
                    entry.grid(row=i, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.entries_a.append(row_entries)

            self.calculate_btn.configure(state="normal")

            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("1.0", "Campos generados. Ingresa los valores y haz clic en 'Calcular Inversa'.")
            self.status_label.configure(text=f"Estado: Campos generados para A ({n}x{n}). Llena todos los campos.")
            print(f"Campos generados: A {n}x{n}")

        except ValueError:
            messagebox.showerror("Error", "Ingresa un número entero válido para el tamaño.")
            self.status_label.configure(text="Estado: Error en tamaño.")

    def limpiar_campos(self):
        for row in self.entries_a:
            for entry in row:
                entry.destroy()
        self.entries_a = []
        self.calculate_btn.configure(state="disabled")

    def limpiar(self):
        self.limpiar_campos()
        self.result_textbox.delete("1.0", "end")
        self.status_label.configure(text="Estado: Limpiado. Listo para generar nuevos campos.")
        self.size_entry.delete(0, "end")
        self.size_entry.insert(0, "2")
        print("Todo limpiado.")

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
                    messagebox.showerror("Error", f"Campo vacío en {matrix_name}[{i+1}][{j+1}].")
                    self.status_label.configure(text=f"Estado: Error - Campo vacío en {matrix_name}.")
                    return None
                try:
                    #  Convertimos directamente a fracción (Fraction acepta “3/4”, “2”, “0.5”, etc.)
                    valor = Fraction(val_str)
                    row_vals.append(valor)
                except Exception:
                    messagebox.showerror(
                        "Error",
                        f"Valor inválido en {matrix_name}[{i+1}][{j+1}]: '{entry.get()}'. "
                        "Usa números o fracciones (ej: 1/2, -3/4, 2)."
                    )
                    self.status_label.configure(text=f"Estado: Error - Valor inválido en {matrix_name}.")
                    return None
            matrix.append(row_vals)

        print(f"{matrix_name} leída correctamente: {matrix}")
        return matrix

    def calcular_inversa(self):
        print("Botón Calcular Inversa presionado.")

        if not self.entries_a:
            messagebox.showerror("Error", "Genera los campos primero.")
            self.status_label.configure(text="Estado: Error - Genera campos primero.")
            return

        self.status_label.configure(text="Estado: Leyendo matriz...")

        A = self.get_matrix_values(self.entries_a, "A")
        if A is None:
            return

        self.status_label.configure(text="Estado: Calculando inversa...")

        inverse, steps = gauss_jordan_inverse(A)
        properties = check_theoretical_properties(A, inverse)

        # Interpretar invertibilidad usando el solver
        is_invertible, det = self.inverse_solver.check_invertibility(A)
        interpret = self.inverse_solver.interpret_invertibility(det)

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", "=== PASOS DEL MÉTODO DE GAUSS-JORDAN ===\n\n")
        for step in steps:
            self.result_textbox.insert("end", step + "\n\n")

        self.result_textbox.insert("end", "=== VERIFICACIÓN DE PROPIEDADES TEÓRICAS ===\n\n")
        for prop in properties:
            self.result_textbox.insert("end", prop + "\n\n")

        self.result_textbox.insert("end", f"=== RELACIÓN CON EL DETERMINANTE ===\n\n{interpret}\n\n")

        self.status_label.configure(text="Estado: Cálculo completado. Revisa los resultados abajo.")
        messagebox.showinfo("Éxito", "Cálculo completado. Revisa los resultados en la ventana.")
        print("Cálculo completado.")