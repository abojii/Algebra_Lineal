import customtkinter as ctk
from Interfaz.Errores.errores import ErrorCalculator, Errores
from Interfaz.sistemaApp import Matrices
from Interfaz.menu import MenuDashboard
from Interfaz.constantes import COLOR_BG, COLOR_FRAME  # Nota: Estas constantes ahora se usan solo inicialmente; los colores se actualizan dinámicamente.
from Interfaz.vectores import Vectores
from Interfaz.sidebar import Sidebar
from Interfaz.submenu import SubMenu
from Interfaz.config import ConfiguracionesDashboard

# Diccionario de temas (debe coincidir con el de ConfiguracionesDashboard para consistencia)
themes = {
    "Oscuro": {
        "bg": "#1e1e2f", "frame": "#2b2b40", "text": "#ffffff", "subtext": "#bbbbbb", "button": "#3b82f6", "entry": "#3a3a4f",
        "sidebar_bg": "#1A202C", "sidebar_hover": "#1F2937", "sidebar_active": "#2563EB", "sidebar_text": "#E5E7EB", "sidebar_subtext": "#9CA3AF", "sidebar_separator": "#1A2234"
    },
    "Claro": {
        "bg": "#f0f0f0", "frame": "#ffffff", "text": "#000000", "subtext": "#666666", "button": "#007bff", "entry": "#e9ecef",
        "sidebar_bg": "#e0e0e0", "sidebar_hover": "#cccccc", "sidebar_active": "#0056b3", "sidebar_text": "#000000", "sidebar_subtext": "#555555", "sidebar_separator": "#aaaaaa"
    },
    "Neutro": {
        "bg": "#f5f5f5", "frame": "#e0e0e0", "text": "#333333", "subtext": "#777777", "button": "#6c757d", "entry": "#d1ecf1",
        "sidebar_bg": "#d0d0d0", "sidebar_hover": "#b0b0b0", "sidebar_active": "#4a90e2", "sidebar_text": "#333333", "sidebar_subtext": "#666666", "sidebar_separator": "#999999"
    }
}

      
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicacion Calculadora algebra lineal")
        self.geometry("900x600")
        
        # Variables para colores y settings (inicialmente con tema oscuro)
        self.colors = themes["Oscuro"].copy()  # Copia para evitar modificar el original
        self.precision = 4  # Valor por defecto
        self.idioma = "Español"  # Valor por defecto
        self.notificaciones = True  # Valor por defecto
        
        self.configure(fg_color=self.colors["bg"])
        
        # Frame toggle
        self.toggle_frame = ctk.CTkFrame(self, width=30, fg_color=self.colors["frame"], corner_radius=0)
        self.toggle_frame.pack(side="left", fill="y")
        self.toggle_button = ctk.CTkButton(self.toggle_frame, text="<<", command=self.toggle_menu, fg_color=self.colors["button"], text_color=self.colors["text"], width=30, height=30, corner_radius=5)
        self.toggle_button.pack(pady=10, padx=5)

        # Sidebar
        self.sidebar = Sidebar(self, self, colors=self.colors)  # Pasa self.colors
        self.sidebar.pack(side="left", fill="y")
        
        self.border_frame = ctk.CTkFrame(self, fg_color="#374151", corner_radius=0)  # Borde fijo
        self.border_frame.pack(side="left", fill="both", expand=True)

        # Content frame
        self.content_frame = ctk.CTkFrame(self.border_frame, fg_color=self.colors["bg"], corner_radius=0)
        self.content_frame.pack(fill="both", expand=True, padx=1, pady=1)

        # Frames
        self.frames = {}
        self.submenus = {}  # Diccionario para submenús

        # Menu principal
        frame_menu = ctk.CTkFrame(self.content_frame, fg_color=self.colors["bg"])
        self.frames["menu"] = frame_menu
        self.menu_dashboard = MenuDashboard(frame_menu, lambda name: self.show_frame(name))

        # Matrices
        frame_calc = ctk.CTkFrame(self.content_frame, fg_color=self.colors["bg"])
        self.frames["calc"] = frame_calc
        self.sistema_app = Matrices(frame_calc, lambda name: self.update_submenu("matrices", name))

        # Vectores
        frame_otra = ctk.CTkFrame(self.content_frame, fg_color=self.colors["bg"], corner_radius=0)
        self.frames["otra"] = frame_otra
        self.other_app = Vectores(frame_otra, lambda name: self.update_submenu("vectores", name))
        
        # Errores
        frame_error = ctk.CTkFrame(self.content_frame, fg_color=self.colors["bg"])
        self.frames["error"] = frame_error
        self.errores_app = Errores(frame_error, lambda name: self.update_submenu("errores", name))
        
        # Configuraciones (cambia el callback aquí)
        frame_config = ctk.CTkFrame(self.content_frame, fg_color=self.colors["bg"])
        self.frames["config"] = frame_config
        self.config_app = ConfiguracionesDashboard(frame_config, self.apply_settings)  # Nuevo callback
        
        # Mostrar menu inicial
        self.show_frame("menu")
        self.menu_visible = True

    def apply_settings(self, settings):
        if "tema" in settings:
            self.colors = settings["tema"].copy()
            self.update_all_themes()
      # ... (resto igual para precision, idioma, notificaciones)
  
        
        if "precision" in settings:
            self.precision = settings["precision"]
            # Aplicar a clases relevantes (ej. Matrices, Vectores) si tienen cálculos
            # Ej: self.sistema_app.set_precision(self.precision)
        
        if "idioma" in settings:
            self.idioma = settings["idioma"]
            # Aplicar idioma (puede requerir recargar textos en frames)
        
        if "notificaciones" in settings:
            self.notificaciones = settings["notificaciones"]
            # Aplicar notificaciones (ej. habilitar/deshabilitar alerts en la app)

    def update_all_themes(self):
        """Actualiza los colores en la ventana principal y todos los frames."""
        self.configure(fg_color=self.colors["bg"])
        self.content_frame.configure(fg_color=self.colors["bg"])  # Solo el interior cambia
        self.toggle_frame.configure(fg_color=self.colors["frame"])
        self.toggle_button.configure(fg_color=self.colors["button"], text_color=self.colors["text"])
        
        # Actualizar frames principales (sus bordes cambian con tema)
        for frame in self.frames.values():
            frame.configure(fg_color=self.colors["bg"], border_color=self.colors["subtext"])
        
        # Actualizar instancias de frames (llama a su método update_theme si existe)
        if hasattr(self.menu_dashboard, 'update_theme'):
            self.menu_dashboard.update_theme(self.colors)
        if hasattr(self.sistema_app, 'update_theme'):
            self.sistema_app.update_theme(self.colors)
        if hasattr(self.other_app, 'update_theme'):
            self.other_app.update_theme(self.colors)
        if hasattr(self.errores_app, 'update_theme'):
            self.errores_app.update_theme(self.colors)
        if hasattr(self.config_app, 'update_theme'):
            self.config_app.update_theme(self.colors)  # Ya implementado en ConfiguracionesDashboard
        if hasattr(self.sidebar, 'update_theme'):
            self.sidebar.update_theme(self.colors)
        
        # Actualizar submenús activos
        for submenu in self.submenus.values():
            if hasattr(submenu, 'update_theme') and submenu.frame and submenu.frame.winfo_exists():
                submenu.update_theme(self.colors)
        
        # Forzar redibujo
        self.update_idletasks()

    def toggle_menu(self):
        if self.menu_visible:
            self.sidebar.pack_forget()
            self.menu_visible = False
            self.toggle_button.configure(text=">>")
        else:
            self.sidebar.pack(side="left", fill="y")
            self.sidebar.pack_configure(before=self.border_frame)
            self.menu_visible = True
            self.toggle_button.configure(text="<<")

    def show_frame(self, name):
        self.sidebar.update_active_button(name)
        for f in self.frames.values():
            f.pack_forget()

        if frame := self.frames.get(name):
            frame.pack(fill="both", expand=True)
            print(f"Mostrando frame: {name}")
        else:
            print("No se muestra nada")
        
        # Gestionar submenús (igual que antes)
        if name == "otra":
            self.setup_submenu("vectores", "Submenú Vectores", [("Matriz-Vector (Ax)", "principal"), ("Ecuación Vectorial", "sub1"), ("Propiedades algebraicas de ℝⁿ", "sub2"), ("Ecuaciones Homogéneas", "sub3")])
            self.submenus["vectores"].show()
        elif name == "calc":
            self.setup_submenu("matrices", "Submenú Matrices", [("Solucion Matrices", "principal"), ("Operaciones con Matrices", "sub1"), ("Matriz Traspuesta", "sub_traspuesta"), ("Propiedades", "Propiedades"), ("Matriz Inversa", "Inversa"), ("Determinante Matriz", "DeterminanteMa"),("Propiedades2", "Ppp")])
            self.submenus["matrices"].show()
        elif name == "error":
            self.setup_submenu("errores", "Submenú Matrices", [("Notacion Posicional", "NotaPosi"), ("Conseptos de Error", "ConsepEr"), ("Errores", "Err"), ("Metodos Numericos","metoNum")])
            self.submenus["errores"].show()
        else:
            self.clear_submenus()

    def setup_submenu(self, key, title, options):
        if key not in self.submenus:
            self.submenus[key] = SubMenu(self.content_frame, title, options, lambda n: self.change_subframe(key, n), None)

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
                submenu.frame.destroy()
            del self.submenus[key]

    def clear_submenus(self):
        for key in list(self.submenus.keys()):
            self.clear_submenu(key)

    def show_sub_submenu_matrices(self):
        self.clear_submenu("matrices")
        self.submenus["matrices_props"] = SubMenu(self.content_frame, "Propiedades Matrices", [("Propiedad Matrices", "Propiedades"), ("Propiedades Traspuesta", "Ptraspuesta"), ("Propiedades Determinantes", "DeterPropiedades"),("Propiedades2", "Ppp")], lambda n: self.change_subframe("matrices", n), lambda: self.volver_submenu_principal())

    def volver_submenu_principal(self):
        self.clear_submenu("matrices_props")
        self.setup_submenu("matrices", "Submenú Matrices", [("Solucion Matrices", "principal"), ("Operaciones con Matrices", "sub1"), ("Matriz Traspuesta", "sub_traspuesta"), ("Propiedades", "Propiedades"), ("Matriz Inversa", "Inversa"), ("Determinante Matriz", "DeterminanteMa")])

    # Métodos open_config_window y open_help_window permanecen igual...

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()