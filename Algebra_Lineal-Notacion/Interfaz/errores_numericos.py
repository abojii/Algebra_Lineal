import customtkinter as ctk
from tkinter import messagebox
 
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#24af2b"
COLOR_ENTRY = "#3a3a4f"
  
COLOR_ACCENT1 = "#2a4d8f"  
COLOR_ACCENT2 = "#1f3a70"  
COLOR_ACCENT3 = "#3b5fa0"  
COLOR_ACCENT4 = "#16325a" 
COLOR_ACCENT5 = "#4a6bb5"  

class NumericalErrors(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_BG)
        self.parent = parent

  
        title_label = ctk.CTkLabel(
            self,
            text="Conceptos de Error en Métodos Numéricos",
            text_color=COLOR_TEXT,
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(15, 10))

        subtitle_label = ctk.CTkLabel(
            self,
            text="Explicaciones y ejemplos de tipos de error",
            text_color=COLOR_SUBTEXT,
            font=("Arial", 14)
        )
        subtitle_label.pack(pady=(0, 20))

        # ======= FRAME PARA ERRORES =======
        errors_frame = ctk.CTkScrollableFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        errors_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Error Inherente
        inherent_frame = ctk.CTkFrame(errors_frame, fg_color=COLOR_ACCENT1, corner_radius=5)
        inherent_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(inherent_frame, text="• Error Inherente:", text_color=COLOR_TEXT, font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(inherent_frame, text="Es el error presente en los datos de entrada debido a mediciones inexactas o aproximaciones iniciales. No se puede eliminar completamente.", text_color=COLOR_SUBTEXT, font=("Arial", 12), wraplength=400).pack(anchor="w", padx=10, pady=5)
        self.inherent_example = ctk.CTkLabel(inherent_frame, text="", text_color=COLOR_TEXT, font=("Arial", 12))
        self.inherent_example.pack(anchor="w", padx=10, pady=5)

        # Error de Redondeo
        rounding_frame = ctk.CTkFrame(errors_frame, fg_color=COLOR_ACCENT2, corner_radius=5)
        rounding_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(rounding_frame, text="• Error de Redondeo:", text_color=COLOR_TEXT, font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(rounding_frame, text="Ocurre cuando se aproximan números a un número finito de dígitos, como en cálculos con punto flotante.", text_color=COLOR_SUBTEXT, font=("Arial", 12), wraplength=400).pack(anchor="w", padx=10, pady=5)
        self.rounding_example = ctk.CTkLabel(rounding_frame, text="", text_color=COLOR_TEXT, font=("Arial", 12))
        self.rounding_example.pack(anchor="w", padx=10, pady=5)

        # Error de Truncamiento
        truncation_frame = ctk.CTkFrame(errors_frame, fg_color=COLOR_ACCENT3, corner_radius=5)
        truncation_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(truncation_frame, text="• Error de Truncamiento:", text_color=COLOR_TEXT, font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(truncation_frame, text="Se produce al detener una serie infinita o un proceso iterativo antes de converger completamente.", text_color=COLOR_SUBTEXT, font=("Arial", 12), wraplength=400).pack(anchor="w", padx=10, pady=5)
        self.truncation_example = ctk.CTkLabel(truncation_frame, text="", text_color=COLOR_TEXT, font=("Arial", 12))
        self.truncation_example.pack(anchor="w", padx=10, pady=5)

        # Overflow y Underflow
        overflow_frame = ctk.CTkFrame(errors_frame, fg_color=COLOR_ACCENT4, corner_radius=5)
        overflow_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(overflow_frame, text="• Overflow y Underflow:", text_color=COLOR_TEXT, font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(overflow_frame, text="Overflow: Resultado demasiado grande para representarse. Underflow: Resultado demasiado pequeño, cercano a cero.", text_color=COLOR_SUBTEXT, font=("Arial", 12), wraplength=400).pack(anchor="w", padx=10, pady=5)
        self.overflow_example = ctk.CTkLabel(overflow_frame, text="", text_color=COLOR_TEXT, font=("Arial", 12))
        self.overflow_example.pack(anchor="w", padx=10, pady=5)

        # Error del Modelo Matemático
        model_frame = ctk.CTkFrame(errors_frame, fg_color=COLOR_ACCENT5, corner_radius=5)
        model_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(model_frame, text="• Error del Modelo Matemático:", text_color=COLOR_TEXT, font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(model_frame, text="Diferencia entre el modelo matemático y la realidad física, debido a simplificaciones o suposiciones.", text_color=COLOR_SUBTEXT, font=("Arial", 12), wraplength=400).pack(anchor="w", padx=10, pady=5)
        self.model_example = ctk.CTkLabel(model_frame, text="", text_color=COLOR_TEXT, font=("Arial", 12))
        self.model_example.pack(anchor="w", padx=10, pady=5)

        # ======= BOTONES =======
        button_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        button_frame.pack(pady=20)

        self.show_examples_button = ctk.CTkButton(button_frame, text="Mostrar Ejemplos", command=self.show_examples, width=150, height=32, fg_color=COLOR_BUTTON)
        self.show_examples_button.pack(side="left", padx=10)

        self.clear_button = ctk.CTkButton(button_frame, text="Limpiar", command=self.clear_all, width=90, height=32, fg_color="#ef4444")
        self.clear_button.pack(side="left", padx=10)

    def show_examples(self):
        # Error Inherente: Ejemplo con medición inexacta
        self.inherent_example.configure(text="Ejemplo: Medir la longitud de una barra con regla inexacta. Valor real: 10.000 cm, medido: 10.005 cm. Error inherente: 0.005 cm.")
        print("Error Inherente: Medir la longitud de una barra con regla inexacta. Valor real: 10.000 cm, medido: 10.005 cm. Error inherente: 0.005 cm.")

        # Error de Redondeo: Ejemplo con división
        result = round(1/3, 2)  # 0.33 en lugar de 0.333...
        self.rounding_example.configure(text=f"Ejemplo: 1/3 ≈ {result} (redondeado a 2 decimales). Valor exacto: 0.333..., error: {abs(1/3 - result):.5f}.")
        print(f"Error de Redondeo: 1/3 ≈ {result} (redondeado a 2 decimales). Valor exacto: 0.333..., error: {abs(1/3 - result):.5f}.")

        # Error de Truncamiento: Serie de Taylor truncada
        import math
        x = 0.5
        approx = x - (x**3)/6  # Truncada después de dos términos para sin(x)
        exact = math.sin(x)
        self.truncation_example.configure(text=f"Ejemplo: sin(0.5) ≈ {approx:.5f} (serie truncada). Valor exacto: {exact:.5f}, error: {abs(exact - approx):.5f}.")
        print(f"Error de Truncamiento: sin(0.5) ≈ {approx:.5f} (serie truncada). Valor exacto: {exact:.5f}, error: {abs(exact - approx):.5f}.")

        # Overflow y Underflow: Ejemplos con floats
        try:
            overflow = 1e308 * 2  # Overflow
            self.overflow_example.configure(text="Ejemplo Overflow: 1e308 * 2 causa overflow (demasiado grande). Underflow: 1e-324 / 2 ≈ 0 (demasiado pequeño).")
        except OverflowError:
            self.overflow_example.configure(text="Ejemplo Overflow: Operación causa OverflowError. Underflow: 1e-324 / 2 ≈ 0.")
        print("Overflow y Underflow: Operación 1e308 * 2 causa overflow. 1e-324 / 2 ≈ 0 (underflow).")

        # Error del Modelo Matemático: Modelo simplificado
        self.model_example.configure(text="Ejemplo: Usar un modelo lineal para datos cuadráticos. Predicción inexacta debido a simplificación.")
        print("Error del Modelo Matemático: Usar un modelo lineal para datos cuadráticos. Predicción inexacta debido a simplificación.")

    def clear_all(self):
        self.inherent_example.configure(text="")
        self.rounding_example.configure(text="")
        self.truncation_example.configure(text="")
        self.overflow_example.configure(text="")
        self.model_example.configure(text="")

# ======= MAIN PARA PROBAR 
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modo oscuro para coincidir con los colores
    ctk.set_default_color_theme("blue")  # Tema azul

    app = ctk.CTk()  # Crear la aplicación principal
    app.title("Conceptos de Error en Métodos Numéricos - Prueba")
    app.geometry("600x700")  # Tamaño de la ventana

    # Instanciar la frame y empaquetarla
    frame = NumericalErrors(app)
    frame.pack(fill="both", expand=True)

    app.mainloop()  # Ejecutar el loop principal