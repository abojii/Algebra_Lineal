import customtkinter as ctk
from tkinter import messagebox


from Models.solverNotacionnum import decompose_base10, decompose_base2

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

        title_label = ctk.CTkLabel(self, text="Notación Posicional", text_color=COLOR_TEXT, font=("Arial", 24, "bold"))
        title_label.pack(pady=(15, 10))

        subtitle_label = ctk.CTkLabel(self, text="Descomponer números en base 10 y base 2", text_color=COLOR_SUBTEXT, font=("Arial", 14))
        subtitle_label.pack(pady=(0, 20))

        base10_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        base10_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(base10_frame, text="Número en Base 10:", text_color=COLOR_TEXT, font=("Arial", 14)).pack(pady=(10, 5))
        self.base10_entry = ctk.CTkEntry(base10_frame, width=200, height=32, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT, justify="center")
        self.base10_entry.pack(pady=(0, 10))

        self.base10_button = ctk.CTkButton(base10_frame, text="Descomponer en Base 10", command=self.decompose_base10, width=200, height=32, fg_color=COLOR_BUTTON)
        self.base10_button.pack(pady=(0, 10))

        self.base10_result = ctk.CTkTextbox(base10_frame, width=400, height=100, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT, wrap="word")
        self.base10_result.pack(pady=(0, 10))
        self.base10_result.configure(state="disabled")

        base2_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        base2_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(base2_frame, text="Número en Base 2 (binario):", text_color=COLOR_TEXT, font=("Arial", 14)).pack(pady=(10, 5))
        self.base2_entry = ctk.CTkEntry(base2_frame, width=200, height=32, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT, justify="center")
        self.base2_entry.pack(pady=(0, 10))

        self.base2_button = ctk.CTkButton(base2_frame, text="Descomponer en Base 2", command=self.decompose_base2, width=200, height=32, fg_color=COLOR_BUTTON)
        self.base2_button.pack(pady=(0, 10))

        self.base2_result = ctk.CTkTextbox(base2_frame, width=400, height=100, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT, wrap="word")
        self.base2_result.pack(pady=(0, 10))
        self.base2_result.configure(state="disabled")

        self.clear_button = ctk.CTkButton(self, text="Limpiar Todo", command=self.clear_all, width=150, height=32, fg_color="#ef4444")
        self.clear_button.pack(pady=20)

    def decompose_base10(self):
        try:
            result_text = decompose_base10(self.base10_entry.get())
            self.base10_result.configure(state="normal")
            self.base10_result.delete("1.0", "end")
            self.base10_result.insert("1.0", result_text)
            self.base10_result.configure(state="disabled")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def decompose_base2(self):
        try:
            result_text = decompose_base2(self.base2_entry.get())
            self.base2_result.configure(state="normal")
            self.base2_result.delete("1.0", "end")
            self.base2_result.insert("1.0", result_text)
            self.base2_result.configure(state="disabled")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_all(self):
        self.base10_entry.delete(0, 'end')
        self.base2_entry.delete(0, 'end')

        self.base10_result.configure(state="normal")
        self.base10_result.delete("1.0", "end")
        self.base10_result.configure(state="disabled")

        self.base2_result.configure(state="normal")
        self.base2_result.delete("1.0", "end")
        self.base2_result.configure(state="disabled")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Notación Posicional - Prueba")
    app.geometry("500x700")

    frame = PositionalNotation(app)
    frame.pack(fill="both", expand=True)

    app.mainloop()
