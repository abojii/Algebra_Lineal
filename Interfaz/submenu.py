import customtkinter as ctk
from Interfaz.constantes import COLOR_FRAME, COLOR_BUTTON

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class SubMenu:
    def __init__(self, master, title, options, callback_change, callback_clear, initial_active="principal"):
        self.master = master
        self.title = title
        self.options = options  # Lista de tuplas: [("Texto", "sub_name"), ...]
        self.callback_change = callback_change  # Función para cambiar subframe
        self.callback_clear = callback_clear    # Función para limpiar menú
        self.frame = None
        self.buttons = {}
        self.visible = True
        self.active_sub = initial_active
        self.setup()

    def setup(self):
        if self.frame and self.frame.winfo_exists():
            if not self.visible:
                self.frame.place(x=10, y=10)
                self.visible = True
            return

        num_opciones = len(self.options) + 1  # +1 para "Salir"
        height = num_opciones * 35 + 40

        self.frame = ctk.CTkFrame(self.master, width=250, height=height, fg_color=COLOR_FRAME, corner_radius=10, border_width=2, border_color="#333333")
        self.frame.place(x=10, y=10)

        # Título y botón de colapso
        title_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(title_frame, text=self.title, font=ctk.CTkFont(size=14, weight="bold"), text_color="white").pack(side="left")
        ctk.CTkButton(title_frame, text="X", width=20, height=20, fg_color="red", text_color="white", corner_radius=10, command=self.toggle, hover_color="darkred").pack(side="right", padx=(5, 0))

        # Botones de opciones
        for text, sub_name in self.options:
            btn = ctk.CTkButton(self.frame, text=text, fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=30, command=lambda n=sub_name: self.change_subframe(n))
            btn.pack(fill="x", pady=2, padx=10)
            self.buttons[sub_name] = btn

        # Botón salir
        ctk.CTkButton(self.frame, text="Salir de Sub-Menú", fg_color="red", text_color="white", corner_radius=5, height=30, command=self.toggle).pack(fill="x", pady=(5, 10), padx=10)

        self.update_active(self.active_sub)
        self.visible = True

    def show(self):
        """Muestra el submenú si está oculto."""
        if self.frame and self.frame.winfo_exists() and not self.visible:
            self.frame.place(x=10, y=10)
            self.visible = True

    def toggle(self):
        if self.frame and self.frame.winfo_exists():
            if self.visible:
                self.frame.place_forget()
                self.visible = False
            else:
                self.frame.place(x=10, y=10)
                self.visible = True

    def change_subframe(self, sub_name):
        self.callback_change(sub_name)
        self.active_sub = sub_name
        self.update_active(sub_name)

    def update_active(self, active_name):
        for btn in self.buttons.values():
            btn.configure(fg_color=COLOR_BUTTON)
        if active_name in self.buttons:
            self.buttons[active_name].configure(fg_color="#60a5fa")

    def clear(self):
        if self.frame and self.frame.winfo_exists():
            self.frame.destroy()
        self.frame = None
        self.buttons = {}
        if self.callback_clear:  # Verificación para evitar TypeError si es None
            self.callback_clear()
