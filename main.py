import customtkinter as ctk
from Interfaz.sistemaApp import SistemaEcuacionesApp
from Interfaz.sistemaApp import Matrices
from Interfaz.menu import MenuDashboard
from Interfaz.constantes import COLOR_BG, COLOR_FRAME, COLOR_BUTTON
from Interfaz.vectores import Vectores

# Paleta de colores (mezcla tus constantes con el ejemplo para profesionalismo)
COLOR_HOVER = "#1F2937"  # Hover para botones
COLOR_ACTIVE = "#2563EB"  # Azul para activo
COLOR_TEXT = "#E5E7EB"    # Texto principal
COLOR_SUBTEXT = "#9CA3AF" # Texto secundario
SEPARATOR_COLOR = "#1A2234"  # Para separadores

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class SidebarButton(ctk.CTkButton):
    def __init__(self, master, text, icon=None, command=None, active=False):
        super().__init__(
            master,
            text=text,  # Solo el texto (sin icono aquí)
            image=icon,  # Icono separado (si es CTkImage)
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
        from PIL import Image
        self.config_icon = ctk.CTkImage(Image.open("icons/settings.png"), size=(18, 18))
        self.help_icon = ctk.CTkImage(Image.open("icons/help.png"), size=(16, 16))
        self.home_icon = ctk.CTkImage(Image.open("icons/casa.png"), size=(25,25))
        self.matriz_icon = ctk.CTkImage(Image.open("icons/matriz.png"), size=(22,22))
        self.vector_icon = ctk.CTkImage(Image.open("icons/vector.png"), size=(22,22))
        self.error_icon = ctk.CTkImage(Image.open("icons/cancelar.png"), size=(22,22))

        # Título del sidebar
        title = ctk.CTkLabel(self, text="📘 Álgebra Lineal", font=("Segoe UI", 22, "bold"), text_color=COLOR_TEXT)
        title.pack(pady=(20, 10), padx=10, anchor="w")

        # Sección: PRINCIPAL
        section1 = ctk.CTkLabel(self, text="PRINCIPAL", font=("Segoe UI", 12), text_color=COLOR_SUBTEXT)
        section1.pack(pady=(10, 5), padx=10, anchor="w")

        # Botones principales con emoji en texto
        self.btn_menu = SidebarButton(self, "Menu",self.home_icon, command=lambda: self.main_app.show_frame("menu"))
        self.btn_matrices = SidebarButton(self, "Matrices",self.matriz_icon, command=lambda: self.main_app.show_frame("calc"))
        self.btn_vectores = SidebarButton(self, "Vectores",self.vector_icon, command=lambda: self.main_app.show_frame("otra"))
        self.btn_errores = SidebarButton(self, "Errores",self.error_icon, command=lambda: self.main_app.show_frame("error"))

        self.buttons_principal = [self.btn_menu, self.btn_matrices, self.btn_vectores, self.btn_errores]
        for b in self.buttons_principal:
            b.pack(fill="x", pady=3, padx=10)

        # Separador
        ctk.CTkFrame(self, fg_color=SEPARATOR_COLOR, height=2).pack(fill="x", pady=15)

        # Sección: HERRAMIENTAS
        section2 = ctk.CTkLabel(self, text="HERRAMIENTAS", font=("Segoe UI", 12), text_color=COLOR_SUBTEXT)
        section2.pack(pady=(5, 5), padx=10, anchor="w")

        # Botones con iconos PNG (image separado)
        self.btn_config = SidebarButton(self, "Configuración", self.config_icon, command=lambda: self.main_app.open_config_window())
        self.btn_ayuda = SidebarButton(self, "Ayuda", self.help_icon, command=lambda: self.main_app.open_help_window())

        self.buttons_herramientas = [self.btn_config, self.btn_ayuda]
        for b in self.buttons_herramientas:
            b.pack(fill="x", pady=3, padx=10)

        # Activar "Menu" por defecto
        self.btn_menu.activate()

    def update_active_button(self, frame_name):
        # Desactivar todos
        for b in self.buttons_principal + self.buttons_herramientas:
            b.deactivate()
        # Activar el correspondiente
        if frame_name == "menu":
            self.btn_menu.activate()
        elif frame_name == "calc":
            self.btn_matrices.activate()
        elif frame_name == "otra":
            self.btn_vectores.activate()
        elif frame_name == "error":
            self.btn_errores.activate()

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicacion Calculadora algebra lineal")
        self.geometry("900x600")
        self.configure(fg_color=COLOR_BG)
        # Frame para el contenido principal

        # Frame toggle
        self.toggle_frame = ctk.CTkFrame(self, width=30, fg_color=COLOR_FRAME, corner_radius=0)
        self.toggle_frame.pack(side="left", fill="y")

        self.toggle_button = ctk.CTkButton(self.toggle_frame, text="<<", command=self.toggle_menu,
                                           fg_color=COLOR_BUTTON, text_color="white", width=30, height=30, corner_radius=5)
        self.toggle_button.pack(pady=10, padx=5)

        # Sidebar (reemplaza menu_frame y buttons_frame)
        self.sidebar = Sidebar(self, self)  # Pasa self para referencia
        self.sidebar.pack(side="left", fill="y")

        # Frame para el contenido principal
        self.content_frame = ctk.CTkFrame(self, fg_color=COLOR_BG, corner_radius=0, border_width=1, border_color="#374151")  # Agrega borde gris oscuro
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Crear frames para cada "pantalla"
        self.frames = {}

        # Frame para el menu principal
        frame_menu = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0,border_width=1,
                border_color="#374151")
        self.frames["menu"] = frame_menu
        self.menu_dashboard = MenuDashboard(frame_menu, lambda name: self.show_frame(name))  # Pasa callback en lugar de self

        # Frame para la calculadora de álgebra lineal (Matrices)
        frame_calc = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0,border_width=1,
                                border_color="#374151")
        self.frames["calc"] = frame_calc
        
        # Definir el callback como una función interna para capturar 'self' correctamente
        def update_sub_menu2_callback(name):
            self.update_sub_menu2(name)
        
        self.sistema_app = Matrices(frame_calc, update_sub_menu2_callback)

        # Frame para vectores
        frame_otra = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0,border_width=1,
                                border_color="#374151")
        self.frames["otra"] = frame_otra
        
        # Definir el callback como una función interna para capturar 'self' correctamente
        def update_sub_menu_callback(name):
            self.update_sub_menu(name)
        
        self.other_app = Vectores(frame_otra, update_sub_menu_callback)

        # Mostrar inicialmente el menú
        self.show_frame("menu")

        self.menu_visible = True
        self.current_subframe = "principal"
        self.sub_menu_buttons = {}
        self.sub_menu_buttons2 = {}
        self.sub_menu_active = False
        self.sub_menu_visible = True
        self.sub_menu_active2 = False
        self.sub_menu_visible2 = True

    def toggle_menu(self):
        if self.menu_visible:
            self.sidebar.pack_forget()
            self.menu_visible = False
            self.toggle_button.configure(text=">>")
        else:
            self.sidebar.pack(side="left", fill="y", before=self.content_frame)
            self.menu_visible = True
            self.toggle_button.configure(text="<<")

    def show_frame(self, name):
        # Actualizar sidebar activo
        self.sidebar.update_active_button(name)
        
        for f in self.frames.values():
            f.pack_forget()
            f.grid_forget()

        if frame := self.frames.get(name):
            frame.pack(fill="both", expand=True)

            if name == "otra":
                self.setup_sub_menu()
                self.sub_menu_active = True
                if hasattr(self, 'sub_menu_frame') and not self.sub_menu_visible:
                    self.toggle_sub_menu()
            elif name == "calc":
                self.clear_menu()
                self.setup_sub_menu2()
                self.sub_menu_active2 = True
                if hasattr(self, 'sub_menu_frame2') and not self.sub_menu_visible2:
                    self.toggle_sub_menu2()
            else:
                self.clear_menu()
                self.clear_menu2()
                self.sub_menu_active = False
                self.sub_menu_active2 = False

    def setup_sub_menu(self):  # Para Vectores
        if hasattr(self, 'sub_menu_frame') and self.sub_menu_frame.winfo_exists():
            if not self.sub_menu_visible:
                self.sub_menu_frame.place(x=10, y=10)
                self.sub_menu_visible = True
            return

        num_opciones = 5
        height = num_opciones * 35 + 40

        self.sub_menu_frame = ctk.CTkFrame(self.content_frame, width=250, height=height, fg_color=COLOR_FRAME, corner_radius=10, border_width=2, border_color="#333333")
        self.sub_menu_frame.place(x=10, y=10)

        title_frame = ctk.CTkFrame(self.sub_menu_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(10, 5))

        sub_title = ctk.CTkLabel(title_frame, text="Submenú Vectores", font=ctk.CTkFont(size=14, weight="bold"), text_color="white")
        sub_title.pack(side="left")

        collapse_btn = ctk.CTkButton(title_frame, text="X", width=20, height=20, fg_color="red", text_color="white", corner_radius=10, command=self.toggle_sub_menu, hover_color="darkred")
        collapse_btn.pack(side="right", padx=(5, 0))

        self.sub_menu_buttons = {}
        opciones = [("Matriz-Vector (Ax)", "principal"), ("Ecuación Vectorial", "sub1"), ("Propiedades algebraicas de ℝⁿ", "sub2"), ("Ecuaciones Homogéneas", "sub3")]

        for text, sub_name in opciones:
            btn = ctk.CTkButton(self.sub_menu_frame, text=text, fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=30, command=lambda n=sub_name: self.change_subframe(n))
            btn.pack(fill="x", pady=2, padx=10)
            self.sub_menu_buttons[sub_name] = btn

        salir_btn = ctk.CTkButton(self.sub_menu_frame, text="Salir de Sub-Menú", fg_color="red", text_color="white", corner_radius=5, height=30, command=self.clear_menu)
        salir_btn.pack(fill="x", pady=(5, 10), padx=10)

        self.update_sub_menu(self.current_subframe)
        self.sub_menu_visible = True

    def setup_sub_menu2(self):  # Para Matrices
        if hasattr(self, 'sub_menu_frame2') and self.sub_menu_frame2.winfo_exists():
            if not self.sub_menu_visible2:
                self.sub_menu_frame2.place(x=10, y=10)
                self.sub_menu_visible2 = True
            return

        num_opciones = 6
        height = num_opciones * 35 + 40

        self.sub_menu_frame2 = ctk.CTkFrame(self.content_frame, width=250, height=height, fg_color=COLOR_FRAME, corner_radius=10, border_width=2, border_color="#333333")
        self.sub_menu_frame2.place(x=10, y=10)

        title_frame = ctk.CTkFrame(self.sub_menu_frame2, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(10, 5))

        sub_title = ctk.CTkLabel(title_frame, text="Submenú Matrices", font=ctk.CTkFont(size=14, weight="bold"), text_color="white")
        sub_title.pack(side="left")

        collapse_btn = ctk.CTkButton(title_frame, text="X", width=20, height=20, fg_color="red", text_color="white", corner_radius=10, command=self.toggle_sub_menu2, hover_color="darkred")
        collapse_btn.pack(side="right", padx=(5, 0))

        self.sub_menu_buttons2 = {}
        opciones = [("Solucion Matrices", "principal"), ("Operaciones con Matrices", "sub1"),
                    ("Matriz Traspuesta", "sub_traspuesta"),("Propiedades","Propiedades"),
                    ("Matriz Inversa", "Inversa"),("Determinante Matriz", "DeterminanteMa")]

        for text, sub_name in opciones:
            if sub_name in ["Propiedades", "Ptraspuesta"]:
                command = lambda n=sub_name: self.show_sub_sub_menu(n)
            else:
                command = lambda n=sub_name: self.change_subframe2(n)
            btn = ctk.CTkButton(self.sub_menu_frame2, text=text, fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=30, command=command)
            btn.pack(fill="x", pady=2, padx=10)
            self.sub_menu_buttons2[sub_name] = btn

        salir_btn = ctk.CTkButton(self.sub_menu_frame2, text="Salir de Sub-Menú", fg_color="red", text_color="white", corner_radius=5, height=30, command=self.clear_menu2)
        salir_btn.pack(fill="x", pady=(5, 10), padx=10)

        self.update_sub_menu2(self.current_subframe)
        self.sub_menu_visible2 = True

    def show_sub_sub_menu(self, type_menu):
        self.clear_menu2()
        if type_menu == "Propiedades":
            self.setup_sub_menu2_properties()
        elif type_menu == "Ptraspuesta":
            print("No implementado")

    def volver_a_sub_menu_principal(self):
        self.clear_menu2()
        self.current_subframe = "principal"
        self.setup_sub_menu2()

    def setup_sub_menu2_properties(self):
        num_opciones = 5
        height = num_opciones * 35 + 80

        self.sub_menu_frame2 = ctk.CTkFrame(self.content_frame, width=250, height=height, fg_color=COLOR_FRAME, corner_radius=10, border_width=2, border_color="#333333")
        self.sub_menu_frame2.place(x=10, y=10)

        title_frame = ctk.CTkFrame(self.sub_menu_frame2, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(10, 5))

        sub_title = ctk.CTkLabel(title_frame, text="Propiedades Matrices", font=ctk.CTkFont(size=14, weight="bold"), text_color="white")
        sub_title.pack(side="left")

        collapse_btn = ctk.CTkButton(title_frame, text="X", width=20, height=20, fg_color="red", text_color="white", corner_radius=10, command=self.toggle_sub_menu2, hover_color="darkred")
        collapse_btn.pack(side="right", padx=(5, 0))

        self.sub_menu_buttons2 = {}
        opciones = [("Propiedad Matrices", "Propiedades"), ("Propiedades Traspuesta", "Ptraspuesta"),("Propiedades Determinantes","DeterPropiedades")]

        for text, sub_name in opciones:
            btn = ctk.CTkButton(self.sub_menu_frame2, text=text, fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=30, command=lambda n=sub_name: self.change_subframe2(n))
            btn.pack(fill="x", pady=2, padx=10)
            self.sub_menu_buttons2[sub_name] = btn

        volver_btn = ctk.CTkButton(self.sub_menu_frame2, text="Volver", fg_color="orange", text_color="white", corner_radius=5, height=30, command=self.volver_a_sub_menu_principal)
        volver_btn.pack(fill="x", pady=(5, 10), padx=10)

        salir_btn = ctk.CTkButton(self.sub_menu_frame2, text="Salir de Sub-Menú", fg_color="red", text_color="white", corner_radius=5, height=30, command=self.clear_menu2)
        salir_btn.pack(fill="x", pady=(5, 10), padx=10)

        self.update_sub_menu2(self.current_subframe)
        self.sub_menu_visible2 = True

    def toggle_sub_menu(self):
        if self.sub_menu_visible:
            self.sub_menu_frame.place_forget()
            self.sub_menu_visible = False
        else:
            self.sub_menu_frame.place(x=10, y=10)
            self.sub_menu_visible = True

    def toggle_sub_menu2(self):
        if self.sub_menu_visible2:
            self.sub_menu_frame2.place_forget()
            self.sub_menu_visible2 = False
        else:
            self.sub_menu_frame2.place(x=10, y=10)
            self.sub_menu_visible2 = True

    def change_subframe(self, sub_name):
        if hasattr(self, 'other_app') and self.other_app:
            self.other_app.show_subframe(sub_name)
            self.current_subframe = sub_name
            self.update_sub_menu(sub_name)

    def change_subframe2(self, sub_name):
        if hasattr(self, 'sistema_app') and self.sistema_app:
            self.sistema_app.show_subframe(sub_name)
            self.current_subframe = sub_name
            self.update_sub_menu2(sub_name)
                    
    def update_sub_menu(self, active_name):
        if hasattr(self, 'sub_menu_buttons') and self.sub_menu_buttons:
            for btn in self.sub_menu_buttons.values():
                btn.configure(fg_color=COLOR_BUTTON)
            if active_name in self.sub_menu_buttons:
                self.sub_menu_buttons[active_name].configure(fg_color="#60a5fa")
        else:
            print("sub_menu_buttons no está inicializado. Asegúrate de que setup_sub_menu se ejecute primero.")

    def update_sub_menu2(self, active_name):
        if hasattr(self, 'sub_menu_buttons2') and self.sub_menu_buttons2:
            for btn in self.sub_menu_buttons2.values():
                btn.configure(fg_color=COLOR_BUTTON)
            if active_name in self.sub_menu_buttons2:
                self.sub_menu_buttons2[active_name].configure(fg_color="#60a5fa")
        else:
            print("sub_menu_buttons2 no está inicializado. Asegúrate de que setup_sub_menu2 se ejecute primero.")

    def clear_menu(self):
        if hasattr(self, 'sub_menu_frame') and self.sub_menu_frame.winfo_exists():
            self.sub_menu_frame.destroy()
            del self.sub_menu_frame
            self.sub_menu_buttons = {}
        self.sub_menu_active = False
        self.sub_menu_visible = True

    def clear_menu2(self):
        if hasattr(self, 'sub_menu_frame2') and self.sub_menu_frame2.winfo_exists():
            self.sub_menu_frame2.destroy()
            del self.sub_menu_frame2
            self.sub_menu_buttons2 = {}
        self.sub_menu_active2 = False
        self.sub_menu_visible2 = True

    def open_config_window(self):
        # Placeholder: Reemplaza con tu código de ventana de configuración
        config_window = ctk.CTkToplevel(self)
        config_window.title("Configuración")
        config_window.geometry("400x300")
        ctk.CTkLabel(config_window, text="Ventana de Configuración").pack(pady=20)
        ctk.CTkButton(config_window, text="Cerrar", command=config_window.destroy).pack()

    def open_help_window(self):
        # Placeholder: Reemplaza con tu código de ventana de ayuda
        help_window = ctk.CTkToplevel(self)
        help_window.title("Ayuda")
        help_window.geometry("400x300")
        ctk.CTkLabel(help_window, text="Ventana de Ayuda").pack(pady=20)
        ctk.CTkButton(help_window, text="Cerrar", command=help_window.destroy).pack()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

