import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class SidebarButton(ctk.CTkButton):
    def __init__(self, master, text, icon=None, command=None, active=False, colors=None):
        # Pasa colors para inicializar
        self.colors = colors or {}  # Diccionario de colores
        super().__init__(
            master,
            text=text,
            image=icon,
            fg_color=self.colors.get("sidebar_active", "#2563EB") if active else "transparent",
            hover_color=self.colors.get("sidebar_hover", "#1F2937"),
            text_color=self.colors.get("sidebar_text", "#E5E7EB") if active else self.colors.get("sidebar_subtext", "#9CA3AF"),
            anchor="w",
            font=("Segoe UI", 14),
            corner_radius=10,
            height=40,
            command=command
        )
        self.active = active
        self.default_text_color = self.colors.get("sidebar_subtext", "#9CA3AF")

    def activate(self):
        self.configure(fg_color=self.colors.get("sidebar_active", "#2563EB"), text_color=self.colors.get("sidebar_text", "#E5E7EB"))
        self.active = True

    def deactivate(self):
        self.configure(fg_color="transparent", text_color=self.default_text_color)
        self.active = False

    def update_theme(self, colors):
        """Actualiza colores del botón."""
        self.colors = colors
        self.default_text_color = colors.get("sidebar_subtext", "#9CA3AF")
        self.configure(hover_color=colors.get("sidebar_hover", "#1F2937"))
        if self.active:
            self.activate()
        else:
            self.deactivate()

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, main_app, colors=None):
        self.colors = colors or themes["Oscuro"]  # Usa colores iniciales (ej. oscuro por defecto)
        super().__init__(master, fg_color=self.colors.get("sidebar_bg", "#1A202C"), width=250)
        self.pack_propagate(False)
        self.main_app = main_app

        # Cargar iconos (igual)
        self.config_icon = ctk.CTkImage(Image.open("icons/settings.png"), size=(18, 18))
        self.help_icon = ctk.CTkImage(Image.open("icons/help.png"), size=(16, 16))
        self.home_icon = ctk.CTkImage(Image.open("icons/casa.png"), size=(25, 25))
        self.matriz_icon = ctk.CTkImage(Image.open("icons/matriz.png"), size=(22, 22))
        self.vector_icon = ctk.CTkImage(Image.open("icons/vector.png"), size=(22, 22))
        self.error_icon = ctk.CTkImage(Image.open("icons/cancelar.png"), size=(22, 22))

        # Título
        self.title = ctk.CTkLabel(self, text="📘 Álgebra Lineal", font=("Segoe UI", 22, "bold"), text_color=self.colors.get("sidebar_text", "#E5E7EB"))
        self.title.pack(pady=(20, 10), padx=10, anchor="w")

        # Sección PRINCIPAL
        self.section1 = ctk.CTkLabel(self, text="PRINCIPAL", font=("Segoe UI", 12), text_color=self.colors.get("sidebar_subtext", "#9CA3AF"))
        self.section1.pack(pady=(10, 5), padx=10, anchor="w")

        self.btn_menu = SidebarButton(self, "Menu", self.home_icon, command=lambda: self.main_app.show_frame("menu"), colors=self.colors)
        self.btn_matrices = SidebarButton(self, "Matrices", self.matriz_icon, command=lambda: self.main_app.show_frame("calc"), colors=self.colors)
        self.btn_vectores = SidebarButton(self, "Vectores", self.vector_icon, command=lambda: self.main_app.show_frame("otra"), colors=self.colors)
        self.btn_errores = SidebarButton(self, "Errores", self.error_icon, command=lambda: self.main_app.show_frame("error"), colors=self.colors)

        self.buttons_principal = [self.btn_menu, self.btn_matrices, self.btn_vectores, self.btn_errores]
        for b in self.buttons_principal:
            b.pack(fill="x", pady=3, padx=10)

        # Separador
        self.separator = ctk.CTkFrame(self, fg_color=self.colors.get("sidebar_separator", "#1A2234"), height=2)
        self.separator.pack(fill="x", pady=15)

        # Sección HERRAMIENTAS
        self.section2 = ctk.CTkLabel(self, text="HERRAMIENTAS", font=("Segoe UI", 12), text_color=self.colors.get("sidebar_subtext", "#9CA3AF"))
        self.section2.pack(pady=(5, 5), padx=10, anchor="w")

        self.btn_config = SidebarButton(self, "Configuración", self.config_icon, command=lambda: self.main_app.show_frame("config"), colors=self.colors)
        self.btn_ayuda = SidebarButton(self, "Ayuda", self.help_icon, command=lambda: self.main_app.open_help_window(), colors=self.colors)

        self.buttons_herramientas = [self.btn_config, self.btn_ayuda]
        for b in self.buttons_herramientas:
            b.pack(fill="x", pady=3, padx=10)

        # Activar "Menu" por defecto
        self.btn_menu.activate()

    def update_theme(self, colors):
        """Actualiza todos los colores del sidebar."""
        self.colors = colors
        self.configure(fg_color=colors.get("sidebar_bg", "#1A202C"))
        self.title.configure(text_color=colors.get("sidebar_text", "#E5E7EB"))
        self.section1.configure(text_color=colors.get("sidebar_subtext", "#9CA3AF"))
        self.section2.configure(text_color=colors.get("sidebar_subtext", "#9CA3AF"))
        self.separator.configure(fg_color=colors.get("sidebar_separator", "#1A2234"))
        
        # Actualizar botones
        for b in self.buttons_principal + self.buttons_herramientas:
            b.update_theme(colors)

    def update_active_button(self, frame_name):
        for b in self.buttons_principal + self.buttons_herramientas:
            b.deactivate()
        if frame_name == "menu":
            self.btn_menu.activate()
        elif frame_name == "calc":
            self.btn_matrices.activate()
        elif frame_name == "otra":
            self.btn_vectores.activate()
        elif frame_name == "error":
            self.btn_errores.activate()
        elif frame_name == "config":
            self.btn_config.activate()