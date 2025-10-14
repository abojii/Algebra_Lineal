import customtkinter as ctk
from Interfaz.constantes import COLOR_BG, COLOR_FRAME, COLOR_BUTTON

class SubMenuManager:
    """Manager genérico para submenús overlay. Se usa desde secciones en el paquete Interfaz."""
    def __init__(self, content_frame, section_name, options, change_callback, clear_callback=None, toggle_callback=None):
        """
        Inicializa el manager.
        - content_frame: Frame donde colocar el overlay (e.g., main_app.content_frame).
        - section_name: Nombre para el título (e.g., "Vectores" o "Matrizes").
        - options: Lista de tuplas [(texto, sub_name), ...].
        - change_callback: Función a llamar al seleccionar opción (e.g., section.change_subframe).
        - clear_callback: Función para limpiar después de destruir (opcional).
        - toggle_callback: Función para toggle visibilidad (opcional).
        """
        self.content_frame = content_frame
        self.section_name = section_name
        self.options = options
        self.change_callback = change_callback
        self.clear_callback = clear_callback
        self.toggle_callback = toggle_callback
        self.sub_menu_frame = None
        self.sub_menu_buttons = {}
        self.visible = True
        self._create_submenu()

    def _create_submenu(self):
        """Crea el frame del submenú como overlay (place geometry)."""
        if self.sub_menu_frame and self.sub_menu_frame.winfo_exists():
            if not self.visible:
                self.sub_menu_frame.place(x=10, y=10)
            return

        num_opciones = len(self.options) + 1  # +1 para botón "Salir"
        height = min(num_opciones * 35 + 50, 400)  # Dinámico con límite para scroll

        self.sub_menu_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            width=250,
            height=height,
            fg_color=COLOR_FRAME,
            corner_radius=10,
            border_width=2,
            border_color="#333333"  # Sombra sutil
        )
        self.sub_menu_frame.place(x=10, y=10)

        # Título con botón colapsar
        title_frame = ctk.CTkFrame(self.sub_menu_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            title_frame,
            text=f"Submenú {self.section_name}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(side="left")

        collapse_btn = ctk.CTkButton(
            title_frame,
            text="X",
            width=20, height=20,
            fg_color="red", hover_color="darkred",
            text_color="white",
            corner_radius=10,
            command=self.toggle_submenu
        )
        collapse_btn.pack(side="right", padx=(5, 0))

        # Botones de opciones
        self.sub_menu_buttons = {}
        for text, sub_name in self.options:
            btn = ctk.CTkButton(
                self.sub_menu_frame,
                text=text,
                fg_color=COLOR_BUTTON, hover_color="#4f9eff",
                text_color="white",
                corner_radius=5,
                height=30,
                command=lambda n=sub_name: self._on_option_selected(n)
            )
            btn.pack(fill="x", pady=2, padx=10)
            self.sub_menu_buttons[sub_name] = btn

        # Botón salir (destruye el submenú)
        salir_btn = ctk.CTkButton(
            self.sub_menu_frame,
            text="Salir de Sub-Menú",
            fg_color="red", hover_color="darkred",
            text_color="white",
            corner_radius=5,
            height=30,
            command=self.clear_submenu
        )
        salir_btn.pack(fill="x", pady=(5, 10), padx=10)

        self.visible = True

    def _on_option_selected(self, sub_name):
        """Maneja selección: resalta y llama callback."""
        self.update_active(sub_name)
        if self.change_callback:
            self.change_callback(sub_name)

    def update_active(self, active_name):
        """Resalta el botón activo en el submenú."""
        for btn in self.sub_menu_buttons.values():
            btn.configure(fg_color=COLOR_BUTTON)
        if active_name in self.sub_menu_buttons:
            self.sub_menu_buttons[active_name].configure(fg_color="#60a5fa")  # Azul claro para activo

    def toggle_submenu(self):
        """Alterna visibilidad (colapsa/expande sin destruir)."""
        if self.visible:
            self.sub_menu_frame.place_forget()
            self.visible = False
        else:
            self.sub_menu_frame.place(x=10, y=10)
            self.visible = True
        if self.toggle_callback:
            self.toggle_callback(self.visible)

    def clear_submenu(self):
        """Destruye completamente el submenú y resetea estado."""
        if self.sub_menu_frame and self.sub_menu_frame.winfo_exists():
            self.sub_menu_frame.destroy()
        self.sub_menu_frame = None
        self.sub_menu_buttons = {}
        self.visible = True
        if self.clear_callback:
            self.clear_callback()
