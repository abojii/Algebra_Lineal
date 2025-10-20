import customtkinter as ctk
from tkinter import messagebox

# Configuración de CustomTkinter
ctk.set_appearance_mode("light")  # Modos: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

class MatrixInverseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Álgebra Lineal - Tarea 6: Inversa de Matriz")
        self.geometry("900x800")  # Tamaño para mejor visibilidad
        self.resizable(True, True)

        # Variable para tamaño (ahora un entry en lugar de combo)
        self.size_entry = None  # Se inicializa en setup_ui

        # Lista para almacenar entradas de A
        self.entries_a = []

        # Frame principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        self.setup_ui()

    def setup_ui(self):
        # Título
        titulo = ctk.CTkLabel(self.main_frame, text="Calculadora de Inversa de Matriz Cuadrada (Gauss-Jordan)",
                              font=ctk.CTkFont(size=18, weight="bold"))
        titulo.pack(pady=20)

        subtitulo = ctk.CTkLabel(self.main_frame, text="Ingresa la matriz cuadrada A (n×n) para calcular su inversa y verificar propiedades",
                                 font=ctk.CTkFont(size=10))
        subtitulo.pack(pady=(0, 20))

        # Frame de configuración
        config_frame = ctk.CTkFrame(self.main_frame)
        config_frame.pack(fill="x", padx=20, pady=10)

        # Etiqueta y entry para tamaño
        ctk.CTkLabel(config_frame, text="Tamaño de la matriz (n):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.size_entry = ctk.CTkEntry(config_frame, width=60, placeholder_text="n")
        self.size_entry.grid(row=0, column=1, padx=5, pady=10)
        self.size_entry.insert(0, "2")  # Valor por defecto

        # Botones
        self.generate_btn = ctk.CTkButton(config_frame, text="Generar Campos", command=self.generar_campos, width=100)
        self.generate_btn.grid(row=0, column=2, padx=10, pady=10)

        self.calculate_btn = ctk.CTkButton(config_frame, text="Calcular Inversa", command=self.calcular_inversa, width=100, state="disabled")
        self.calculate_btn.grid(row=0, column=3, padx=5, pady=10)

        self.clear_btn = ctk.CTkButton(config_frame, text="Limpiar", command=self.limpiar, width=100)
        self.clear_btn.grid(row=0, column=4, padx=10, pady=10)

        # Frame para matriz A
        self.frame_a = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_a.pack(fill="both", padx=20, pady=10, expand=True)

        label_a = ctk.CTkLabel(self.frame_a, text="Matriz A (n × n):", font=ctk.CTkFont(weight="bold"))
        label_a.pack(pady=(10, 5))

        self.entries_a_frame = ctk.CTkScrollableFrame(self.frame_a)
        self.entries_a_frame.pack(fill="both", expand=True, pady=5)

        # Frame para resultado
        self.result_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.result_frame.pack(fill="both", padx=20, pady=10, expand=True)

        # Label de estado
        self.status_label = ctk.CTkLabel(self.result_frame, text="Estado: Listo para generar campos.", 
                                         font=ctk.CTkFont(size=10), anchor="w")
        self.status_label.pack(pady=(10, 0), fill="x")

        # Textbox para resultados (para mostrar pasos largos)
        self.result_textbox = ctk.CTkTextbox(self.result_frame, wrap="word", font=ctk.CTkFont(size=12))
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

            # Limpiar campos anteriores
            self.limpiar_campos()

            # Generar entradas para A (n x n)
            self.entries_a = []
            for i in range(n):
                row_entries = []
                for j in range(n):
                    entry = ctk.CTkEntry(self.entries_a_frame, width=60, height=30, placeholder_text=f"a{i+1}{j+1}")
                    entry.grid(row=i, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.entries_a.append(row_entries)

            # Habilitar botón de calcular
            self.calculate_btn.configure(state="normal")

            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("1.0", "Campos generados. Ingresa los valores y haz clic en 'Calcular Inversa'.")
            self.status_label.configure(text=f"Estado: Campos generados para A ({n}x{n}). Llena todos los campos.")

            print(f"Campos generados: A {n}x{n}")  # Debug en consola

        except ValueError:
            messagebox.showerror("Error", "Ingresa un número entero válido para el tamaño.")
            self.status_label.configure(text="Estado: Error en tamaño.")

    def limpiar_campos(self):
        # Limpiar entradas A
        for row in self.entries_a:
            for entry in row:
                entry.destroy()
        self.entries_a = []

        # Deshabilitar botón calcular
        self.calculate_btn.configure(state="disabled")

    def limpiar(self):
        self.limpiar_campos()
        self.result_textbox.delete("1.0", "end")
        self.status_label.configure(text="Estado: Limpiado. Listo para generar nuevos campos.")
        # Resetear entry
        self.size_entry.delete(0, "end")
        self.size_entry.insert(0, "2")
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

    def calcular_inversa(self):
        print("Botón Calcular Inversa presionado.")  # Debug

        if not self.entries_a:
            messagebox.showerror("Error", "Genera los campos primero.")
            self.status_label.configure(text="Estado: Error - Genera campos primero.")
            return

        self.status_label.configure(text="Estado: Leyendo matriz...")

        A = self.get_matrix_values(self.entries_a, "A")
        if A is None:
            return

        self.status_label.configure(text="Estado: Calculando inversa...")

        # Calcular inversa y pasos
        inverse, steps = self.gauss_jordan_inverse(A)

        # Verificar propiedades
        properties = self.check_properties(A, inverse)

        # Mostrar resultados en el textbox
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", "=== PASOS DEL MÉTODO DE GAUSS-JORDAN ===\n\n")
        for step in steps:
            self.result_textbox.insert("end", step + "\n\n")
        
        self.result_textbox.insert("end", "=== VERIFICACIÓN DE PROPIEDADES TEÓRICAS ===\n\n")
        for prop in properties:
            self.result_textbox.insert("end", prop + "\n\n")

        self.status_label.configure(text="Estado: Cálculo completado. Revisa los pasos y propiedades abajo.")
        messagebox.showinfo("Éxito", "Cálculo completado. Revisa los resultados en la ventana.")
        print("Cálculo completado.")  # Debug

    def gauss_jordan_inverse(self, A):
        """
        Calcula la inversa de la matriz A usando el método de Gauss-Jordan.
        Construye la matriz aumentada [A | I] y aplica operaciones fila.
        Retorna la inversa si existe, o None si no es invertible.
        También retorna una lista de pasos para mostrar.
        """
        n = len(A)
        # Crear identidad I
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        # Matriz aumentada [A | I]
        augmented = [A[i] + I[i] for i in range(n)]
        
        steps = []
        steps.append("Matriz aumentada inicial [A | I]:")
        steps.append(self.matrix_to_string(augmented))
        
        # Aplicar Gauss-Jordan
        for i in range(n):
            # Encontrar pivote en columna i, empezando desde fila i
            pivot_row = -1
            for k in range(i, n):
                if augmented[k][i] != 0:
                    pivot_row = k
                    break
            if pivot_row == -1:
                # No hay pivote, no invertible
                steps.append(f"No se encontró pivote en la columna {i+1}. La matriz no es invertible.")
                return None, steps
            
            # Intercambiar filas si necesario
            if pivot_row != i:
                augmented[i], augmented[pivot_row] = augmented[pivot_row], augmented[i]
                steps.append(f"Intercambio de filas {i+1} y {pivot_row+1}:")
                steps.append(self.matrix_to_string(augmented))
            
            # Hacer pivote 1
            pivot = augmented[i][i]
            for j in range(2*n):
                augmented[i][j] /= pivot
            steps.append(f"Dividir fila {i+1} por {pivot:.4f} para hacer pivote 1:")
            steps.append(self.matrix_to_string(augmented))
            
            # Eliminar en otras filas
            for k in range(n):
                if k != i:
                    factor = augmented[k][i]
                    for j in range(2*n):
                        augmented[k][j] -= factor * augmented[i][j]
                    steps.append(f"Eliminar en fila {k+1} usando fila {i+1} (factor {factor:.4f}):")
                    steps.append(self.matrix_to_string(augmented))
        
        # Extraer la inversa (parte derecha)
        inverse = [row[n:] for row in augmented]
        steps.append("Matriz inversa obtenida:")
        steps.append(self.matrix_to_string(inverse))
        return inverse, steps

    def matrix_to_string(self, matrix):
        """
        Convierte una matriz (lista de listas) a una cadena formateada para mostrar.
        """
        return '\n'.join(['\t'.join([f"{x:.4f}" for x in row]) for row in matrix]) + '\n'

    def check_properties(self, A, inverse):
        """
        Verifica las propiedades teóricas basadas en si la inversa existe.
        Retorna una lista de strings con los resultados.
        """
        n = len(A)
        properties = []
        if inverse is not None:
            properties.append("1. La matriz tiene n pivotes: Sí. Se obtuvieron n pivotes durante Gauss-Jordan, lo que indica que la matriz es invertible.")
            properties.append("2. Ax = 0 tiene solo la solución trivial: Sí. Dado que la matriz es invertible, el sistema Ax = 0 solo tiene la solución x = 0.")
            properties.append("3. Las columnas son linealmente independientes: Sí. Una matriz invertible tiene columnas linealmente independientes.")
        else:
            properties.append("1. La matriz tiene n pivotes: No. No se pudieron obtener n pivotes, por lo que la matriz no es invertible.")
            properties.append("2. Ax = 0 tiene solo la solución trivial: No. El sistema Ax = 0 tiene soluciones no triviales (espacio nulo no trivial).")
            properties.append("3. Las columnas son linealmente independientes: No. Las columnas son linealmente dependientes.")
        return properties

if __name__ == "__main__":
    app = MatrixInverseApp()
    app.mainloop()
