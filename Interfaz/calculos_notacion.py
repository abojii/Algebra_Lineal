import customtkinter as ctk
from tkinter import messagebox

# ======= COLORES (iguales que tus otras interfaces) =======
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

class PositionalNotation(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_BG)
        self.parent = parent

        # ======= TÍTULO =======
        title_label = ctk.CTkLabel(
            self,
            text="Notación Posicional",
            text_color=COLOR_TEXT,
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(15, 10))

        subtitle_label = ctk.CTkLabel(
            self,
            text="Descomponer números en base 10 y base 2",
            text_color=COLOR_SUBTEXT,
            font=("Arial", 14)
        )
        subtitle_label.pack(pady=(0, 20))

        # ======= SECCIÓN BASE 10 =======
        base10_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        base10_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(base10_frame, text="Número en Base 10:", text_color=COLOR_TEXT, font=("Arial", 14)).pack(pady=(10, 5))
        self.base10_entry = ctk.CTkEntry(base10_frame, width=200, height=32, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT, justify="center")
        self.base10_entry.pack(pady=(0, 10))

        self.base10_button = ctk.CTkButton(base10_frame, text="Descomponer en Base 10", command=self.decompose_base10, width=200, height=32, fg_color=COLOR_BUTTON)
        self.base10_button.pack(pady=(0, 10))

        self.base10_result = ctk.CTkLabel(base10_frame, text="", text_color=COLOR_SUBTEXT, font=("Arial", 12), wraplength=400)
        self.base10_result.pack(pady=(0, 10))

        # ======= SECCIÓN BASE 2 =======
        base2_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        base2_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(base2_frame, text="Número en Base 2 (binario):", text_color=COLOR_TEXT, font=("Arial", 14)).pack(pady=(10, 5))
        self.base2_entry = ctk.CTkEntry(base2_frame, width=200, height=32, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT, justify="center")
        self.base2_entry.pack(pady=(0, 10))

        self.base2_button = ctk.CTkButton(base2_frame, text="Descomponer en Base 2", command=self.decompose_base2, width=200, height=32, fg_color=COLOR_BUTTON)
        self.base2_button.pack(pady=(0, 10))

        self.base2_result = ctk.CTkLabel(base2_frame, text="", text_color=COLOR_SUBTEXT, font=("Arial", 12), wraplength=400)
        self.base2_result.pack(pady=(0, 10))

        # ======= BOTÓN LIMPIAR =======
        self.clear_button = ctk.CTkButton(self, text="Limpiar Todo", command=self.clear_all, width=150, height=32, fg_color="#ef4444")
        self.clear_button.pack(pady=20)

    # ======= DESCOMPONER BASE 10 =======
    def decompose_base10(self):
        try:
            num = int(self.base10_entry.get())
            if num < 0:
                raise ValueError("Número debe ser positivo.")
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número entero positivo válido.")
            return

        digits = [int(d) for d in str(num)]
        n = len(digits)
        terms = []
        for i, digit in enumerate(digits):
            power = n - 1 - i
            terms.append(f"{digit}×10^{power}")

        decomposition = " + ".join(terms)
        result_text = f"{num} = {decomposition}"
        self.base10_result.configure(text=result_text)

    # ======= DESCOMPONER BASE 2 =======
    def decompose_base2(self):
        try:
            binary = self.base2_entry.get().strip()
            if not all(c in '01' for c in binary) or not binary:
                raise ValueError("Debe ser un número binario válido (solo 0s y 1s).")
            num = int(binary, 2)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        digits = [int(d) for d in binary]
        n = len(digits)
        terms = []
        for i, digit in enumerate(digits):
            power = n - 1 - i
            terms.append(f"{digit}⋅2^{power}")

        decomposition = " + ".join(terms)
        result_text = f"{binary} = {decomposition}"
        self.base2_result.configure(text=result_text)

    # ======= LIMPIAR =======
    def clear_all(self):
        self.base10_entry.delete(0, 'end')
        self.base2_entry.delete(0, 'end')
        self.base10_result.configure(text="")
        self.base2_result.configure(text="")

# ======= MAIN PARA PROBAR =======
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modo oscuro para coincidir con los colores
    ctk.set_default_color_theme("blue")  # Tema azul

    app = ctk.CTk()  # Crear la aplicación principal
    app.title("Notación Posicional - Prueba")
    app.geometry("500x600")  # Tamaño de la ventana

    # Instanciar la frame y empaquetarla
    frame = PositionalNotation(app)
    frame.pack(fill="both", expand=True)

    app.mainloop()  # Ejecutar el loop principal
