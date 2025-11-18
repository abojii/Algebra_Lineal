import customtkinter as ctk
from Interfaz.Errores.errores import ErrorCalculator, Errores
from Interfaz.sistemaApp import Matrices
from Interfaz.menu import MenuDashboard
from Interfaz.constantes import COLOR_BG, COLOR_FRAME
from Interfaz.vectores import Vectores
from Interfaz.sidebar import Sidebar
from Interfaz.submenu import SubMenu

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicacion Calculadora algebra lineal")
        self.geometry("900x600")
        self.configure(fg_color=COLOR_BG)

        # Frame toggle
        self.toggle_frame = ctk.CTkFrame(self, width=30, fg_color=COLOR_FRAME, corner_radius=0)
        self.toggle_frame.pack(side="left", fill="y")
        self.toggle_button = ctk.CTkButton(self.toggle_frame, text="<<", command=self.toggle_menu, fg_color="#2563EB", text_color="white", width=30, height=30, corner_radius=5)
        self.toggle_button.pack(pady=10, padx=5)

        # Sidebar
        self.sidebar = Sidebar(self, self)
        self.sidebar.pack(side="left", fill="y")

        # Content frame
        self.content_frame = ctk.CTkFrame(self, fg_color=COLOR_BG, corner_radius=0, border_width=1, border_color="#374151")
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Frames
        self.frames = {}
        self.submenus = {}  # Diccionario para submenús: {"vectores": SubMenu, "matrices": SubMenu}

        # Menu principal
        frame_menu = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0, border_width=1, border_color="#374151")
        self.frames["menu"] = frame_menu
        self.menu_dashboard = MenuDashboard(frame_menu, lambda name: self.show_frame(name))

        # Matrices
        frame_calc = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0, border_width=1, border_color="#374151")
        self.frames["calc"] = frame_calc
        self.sistema_app = Matrices(frame_calc, lambda name: self.update_submenu("matrices", name))

        # Vectores
        frame_otra = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0, border_width=1, border_color="#374151")
        self.frames["otra"] = frame_otra
        self.other_app = Vectores(frame_otra, lambda name: self.update_submenu("vectores", name))
        
        # Errores
        frame_error = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0, border_width=1, border_color="#374151")
        self.frames["error"] = frame_error
        self.errores_app = Errores(frame_error, lambda name: self.update_submenu("errores", name))

        # Mostrar menu inicial
        self.show_frame("menu")
        self.menu_visible = True

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
        self.sidebar.update_active_button(name)
        for f in self.frames.values():
            f.pack_forget()

        if frame := self.frames.get(name):
            frame.pack(fill="both", expand=True)

        # Gestionar submenús
        if name == "otra":
            self.setup_submenu("vectores", "Submenú Vectores", [("Matriz-Vector (Ax)", "principal"), ("Ecuación Vectorial", "sub1"), ("Propiedades algebraicas de ℝⁿ", "sub2"), ("Ecuaciones Homogéneas", "sub3")])
            self.submenus["vectores"].show()  # Forzar mostrar si estaba oculto
        elif name == "calc":
            self.setup_submenu("matrices", "Submenú Matrices", [("Solucion Matrices", "principal"), ("Operaciones con Matrices", "sub1"), ("Matriz Traspuesta", "sub_traspuesta"), ("Propiedades", "Propiedades"), ("Matriz Inversa", "Inversa"), ("Determinante Matriz", "DeterminanteMa")])
            self.submenus["matrices"].show()  # Forzar mostrar si estaba oculto
        elif name == "error":
            self.setup_submenu("errores", "Submenú Matrices", [("Notacion Posicional", "NotaPosi"), ("Conseptos de Error", "ConsepEr"),("Errores", "Err")])
            self.submenus["errores"].show()  # Forzar mostrar si estaba ocultos
        else:
            self.clear_submenus()

    def setup_submenu(self, key, title, options):
        if key not in self.submenus:
            self.submenus[key] = SubMenu(self.content_frame, title, options, lambda n: self.change_subframe(key, n), None)  # Cambia aquí: callback_clear = None para evitar recursión

    def change_subframe(self, key, sub_name):
        if key == "vectores" and hasattr(self, 'other_app'):
            self.other_app.show_subframe(sub_name)
        elif key == "matrices" and hasattr(self, 'sistema_app'):
            if sub_name == "Propiedades":
                self.show_sub_submenu_matrices()
            else:
                self.sistema_app.show_subframe(sub_name)
        elif key == "errores" and hasattr(self, 'errores_app'):
            self.errores_app.show_subframe(sub_name)
            

    def update_submenu(self, key, active_name):
        if key in self.submenus:
            self.submenus[key].update_active(active_name)

    def clear_submenu(self, key):
        if key in self.submenus:
            submenu = self.submenus[key]
            if submenu.frame and submenu.frame.winfo_exists():
                submenu.frame.destroy()  # Destruye el frame manualmente
            del self.submenus[key]  # Elimina del diccionario

    def clear_submenus(self):
        for key in list(self.submenus.keys()):
            self.clear_submenu(key)

    def show_sub_submenu_matrices(self):
        self.clear_submenu("matrices")
        # Sub-submenú para Propiedades (puedes expandir si hay más lógica)
        self.submenus["matrices_props"] = SubMenu(self.content_frame, "Propiedades Matrices", [("Propiedad Matrices", "Propiedades"), ("Propiedades Traspuesta", "Ptraspuesta"), ("Propiedades Determinantes", "DeterPropiedades")], lambda n: self.change_subframe("matrices", n), lambda: self.volver_submenu_principal())

    def volver_submenu_principal(self):
        self.clear_submenu("matrices_props")
        self.setup_submenu("matrices", "Submenú Matrices", [("Solucion Matrices", "principal"), ("Operaciones con Matrices", "sub1"), ("Matriz Traspuesta", "sub_traspuesta"), ("Propiedades", "Propiedades"), ("Matriz Inversa", "Inversa"), ("Determinante Matriz", "DeterminanteMa")])

    def open_config_window(self):
        config_window = ctk.CTkToplevel(self)
        config_window.title("Configuración")
        config_window.geometry("400x300")
        ctk.CTkLabel(config_window, text="Ventana de Configuración").pack(pady=20)
        ctk.CTkButton(config_window, text="Cerrar", command=config_window.destroy).pack()

    def open_help_window(self):
        help_window = ctk.CTkToplevel(self)
        help_window.title("Ayuda")
        help_window.geometry("400x300")
        ctk.CTkLabel(help_window, text="Ventana de Ayuda").pack(pady=20)
        ctk.CTkButton(help_window, text="Cerrar", command=help_window.destroy).pack()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()