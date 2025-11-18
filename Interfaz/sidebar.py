import customtkinter as ctk
from PIL import Image

# Paleta de colores
COLOR_HOVER = "#1F2937"
COLOR_ACTIVE = "#2563EB"
COLOR_TEXT = "#E5E7EB"
COLOR_SUBTEXT = "#9CA3AF"
SEPARATOR_COLOR = "#1A2234"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
class SidebarButton(ctk.CTkButton):
    def __init__(self, master, text, icon=None, command=None, active=False):
        super().__init__(
            master,
            text=text,
            image=icon,
            fg_color=COLOR_ACTIVE if active else "transparent",
            hover_color=COLOR_HOVER,
            text_color=COLOR_TEXT if active else COLOR_SUBTEXT,
            anchor="w",
            font=("Segoe UI", 14),
            corner_radius=10,
            height=40,
            command=command
        )
        self.active = active
        self.default_text_color = COLOR_SUBTEXT

    def activate(self):
        self.configure(fg_color=COLOR_ACTIVE, text_color=COLOR_TEXT)
        self.active = True

    def deactivate(self):
        self.configure(fg_color="transparent", text_color=self.default_text_color)
        self.active = False

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, main_app):
        super().__init__(master, fg_color="#1A202C", width=250)
        self.pack_propagate(False)
        self.main_app = main_app

        # Cargar iconos
        self.config_icon = ctk.CTkImage(Image.open("icons/settings.png"), size=(18, 18))
        self.help_icon = ctk.CTkImage(Image.open("icons/help.png"), size=(16, 16))
        self.home_icon = ctk.CTkImage(Image.open("icons/casa.png"), size=(25, 25))
        self.matriz_icon = ctk.CTkImage(Image.open("icons/matriz.png"), size=(22, 22))
        self.vector_icon = ctk.CTkImage(Image.open("icons/vector.png"), size=(22, 22))
        self.error_icon = ctk.CTkImage(Image.open("icons/cancelar.png"), size=(22, 22))

        # Título
        title = ctk.CTkLabel(self, text="📘 Álgebra Lineal", font=("Segoe UI", 22, "bold"), text_color=COLOR_TEXT)
        title.pack(pady=(20, 10), padx=10, anchor="w")

        # Sección PRINCIPAL
        section1 = ctk.CTkLabel(self, text="PRINCIPAL", font=("Segoe UI", 12), text_color=COLOR_SUBTEXT)
        section1.pack(pady=(10, 5), padx=10, anchor="w")

        self.btn_menu = SidebarButton(self, "Menu", self.home_icon, command=lambda: self.main_app.show_frame("menu"))
        self.btn_matrices = SidebarButton(self, "Matrices", self.matriz_icon, command=lambda: self.main_app.show_frame("calc"))
        self.btn_vectores = SidebarButton(self, "Vectores", self.vector_icon, command=lambda: self.main_app.show_frame("otra"))
        self.btn_errores = SidebarButton(self, "Errores", self.error_icon, command=lambda: self.main_app.show_frame("error"))

        self.buttons_principal = [self.btn_menu, self.btn_matrices, self.btn_vectores, self.btn_errores]
        for b in self.buttons_principal:
            b.pack(fill="x", pady=3, padx=10)

        # Separador
        ctk.CTkFrame(self, fg_color=SEPARATOR_COLOR, height=2).pack(fill="x", pady=15)

        # Sección HERRAMIENTAS
        section2 = ctk.CTkLabel(self, text="HERRAMIENTAS", font=("Segoe UI", 12), text_color=COLOR_SUBTEXT)
        section2.pack(pady=(5, 5), padx=10, anchor="w")

        self.btn_config = SidebarButton(self, "Configuración", self.config_icon, command=lambda: self.main_app.open_config_window())
        self.btn_ayuda = SidebarButton(self, "Ayuda", self.help_icon, command=lambda: self.main_app.open_help_window())

        self.buttons_herramientas = [self.btn_config, self.btn_ayuda]
        for b in self.buttons_herramientas:
            b.pack(fill="x", pady=3, padx=10)

        # Activar "Menu" por defecto
        self.btn_menu.activate()

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