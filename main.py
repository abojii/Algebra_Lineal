import customtkinter as ctk
from Interfaz.sistemaApp import SistemaEcuacionesApp
from Interfaz.sistemaApp import Matrices
from Interfaz.vectores import SubVentana3
from Interfaz.constantes import COLOR_BG, COLOR_FRAME, COLOR_BUTTON
from Interfaz.vectores import Vectores
from PIL import Image
#from Interfaz.config import open_config_window, open_help_window

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicacion Calculadora algebra lineal")
        self.geometry("900x600")
        self.configure(fg_color=COLOR_BG)
    
        self.config_icon = ctk.CTkImage(Image.open("icons/settings.png"), size=(25, 25))  # Ajusta ruta y tamaño
        self.help_icon = ctk.CTkImage(Image.open("icons/help.png"), size=(25, 25))

        # Frame toggle
        self.toggle_frame = ctk.CTkFrame(self, width=30, fg_color=COLOR_FRAME, corner_radius=0)
        self.toggle_frame.pack(side="left", fill="y")

        self.toggle_button = ctk.CTkButton(self.toggle_frame, text="<<", command=self.toggle_menu,
                                           fg_color=COLOR_BUTTON, text_color="white", width=30, height=30, corner_radius=5)
        self.toggle_button.pack(pady=10, padx=5)

        # Frame para el menú lateral
        self.menu_frame = ctk.CTkFrame(self, width=150, fg_color=COLOR_FRAME, corner_radius=0)
        self.menu_frame.pack(side="left", fill="y")

        # Frame para los botones del menú principal
        self.buttons_frame = ctk.CTkFrame(self.menu_frame, fg_color=COLOR_FRAME, corner_radius=0)
        self.buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_menu_buttons()

        # Frame para el contenido principal
        self.content_frame = ctk.CTkFrame(self, fg_color=COLOR_BG, corner_radius=0)
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Crear frames para cada "pantalla"
        self.frames = {}

        # Frame para el menu principal
        frame_menu = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0)
        self.frames["menu"] = frame_menu
        self.sistema_app = SubVentana3(frame_menu)

        # Frame para la calculadora de álgebra lineal (Matrices)
        frame_calc = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0)
        self.frames["calc"] = frame_calc
        
        # Definir el callback como una función interna para capturar 'self' correctamente
        def update_sub_menu2_callback(name):
            self.update_sub_menu2(name)
        
        self.sistema_app = Matrices(frame_calc, update_sub_menu2_callback)

        # Frame para vectores
        frame_otra = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0)
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

    def create_menu_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        # Botones existentes
        btn_menu = ctk.CTkButton(self.buttons_frame, text="Menu",
                                fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=40,
                                command=lambda: self.show_frame("menu"))
        btn_menu.pack(fill="x", pady=5, padx=5)
        
        btn_matrices = ctk.CTkButton(self.buttons_frame, text="Matrices",
                                    fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=40,
                                    command=lambda: self.show_frame("calc"))
        btn_matrices.pack(fill="x", pady=5, padx=5)
        
        btn_vectores = ctk.CTkButton(self.buttons_frame, text="Vectores",
                                    fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=40,
                                    command=lambda: self.show_frame("otra"))
        btn_vectores.pack(fill="x", pady=5, padx=5)
        
        btn_errores = ctk.CTkButton(self.buttons_frame, text="Errores",
                                    fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=40,
                                    command=lambda: self.show_frame("error"))
        btn_errores.pack(fill="x", pady=5, padx=5)

        # Frame para botones inferiores (pequeños y cuadrados)
        self.bottom_buttons_frame = ctk.CTkFrame(self.menu_frame, fg_color=COLOR_FRAME, corner_radius=0)
        self.bottom_buttons_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 10))  # Pegado abajo
        # Botones pequeños con iconos (cuadrados, sin texto o con tooltip)
        btn_config = ctk.CTkButton(self.bottom_buttons_frame, text="",  # Sin texto, solo icono
                                image=self.config_icon, fg_color=COLOR_FRAME, width=40, height=40, corner_radius=5,
                                command=lambda: self.open_config_window())
        btn_config.pack(side="left", padx=1)  # Alineados horizontalmente
        btn_ayuda = ctk.CTkButton(self.bottom_buttons_frame, text="",  # Sin texto, solo icono
                                image=self.help_icon, fg_color=COLOR_FRAME, width=40, height=40, corner_radius=5,
                                command=lambda: self.open_help_window())
        btn_ayuda.pack(side="left", padx=1)

    def toggle_menu(self):
        if self.menu_visible:
            self.menu_frame.pack_forget()
            self.menu_visible = False
            self.toggle_button.configure(text=">>")
        else:
            self.menu_frame.pack(side="left", fill="y", before=self.content_frame)
            self.menu_visible = True
            self.toggle_button.configure(text="<<")

    def show_frame(self, name):
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
        # Crear ventana emergente
        config_window = ctk.CTkToplevel(self)
        config_window.title("Configuración")
        config_window.geometry("400x500")  # Ajusta tamaño según contenido
        config_window.resizable(False, False)
        config_window.transient(self)  # Hace que sea dependiente de la ventana principal
        config_window.grab_set()  # Bloquea interacción con la principal hasta cerrar (opcional, quítalo si quieres no modal)

        # Título
        title_label = ctk.CTkLabel(config_window, text="Configuración de la App", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=10)

        # Opción 1: Cambiar Tema
        theme_frame = ctk.CTkFrame(config_window, fg_color=COLOR_FRAME)
        theme_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(theme_frame, text="Tema:").pack(side="left", padx=10)
        theme_switch = ctk.CTkSwitch(theme_frame, text="Modo Oscuro", command=self.toggle_theme)
        theme_switch.pack(side="right", padx=10)
        # Configura el switch según el tema actual
        current_mode = ctk.get_appearance_mode()
        theme_switch.select() if current_mode == "dark" else theme_switch.deselect()

        # Opción 2: Personalizar Color de Fondo (ejemplo simple con slider para un componente RGB)
        color_frame = ctk.CTkFrame(config_window, fg_color=COLOR_FRAME)
        color_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(color_frame, text="Color de Fondo (Rojo):").pack(pady=5)
        color_slider = ctk.CTkSlider(color_frame, from_=0, to=255, command=self.update_bg_color)
        color_slider.pack(pady=5)
        # Nota: Para RGB completo, agrega más sliders y combina valores.

        # Opción 3: Tamaño de Fuente
        font_frame = ctk.CTkFrame(config_window, fg_color=COLOR_FRAME)
        font_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(font_frame, text="Tamaño de Fuente:").pack(pady=5)
        font_slider = ctk.CTkSlider(font_frame, from_=10, to=20, command=self.update_font_size)
        font_slider.pack(pady=5)

        # Botones de Acción
        buttons_frame = ctk.CTkFrame(config_window, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        save_btn = ctk.CTkButton(buttons_frame, text="Guardar", command=self.save_config)
        save_btn.pack(side="left", padx=5)
        reset_btn = ctk.CTkButton(buttons_frame, text="Resetear", fg_color="orange", command=self.reset_config)
        reset_btn.pack(side="left", padx=5)
        close_btn = ctk.CTkButton(buttons_frame, text="Cerrar", fg_color="red", command=config_window.destroy)
        close_btn.pack(side="right", padx=5)
        

    #Ventana de ayuda
    def open_help_window(self):
        help_window = ctk.CTkToplevel(self)
        help_window.title("Ayuda")
        help_window.geometry("500x400")
        help_window.resizable(False, False)
        help_window.transient(self)

        title_label = ctk.CTkLabel(help_window, text="Ayuda - Calculadora de Álgebra Lineal", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=10)

        # Contenido scrollable
        scrollable_frame = ctk.CTkScrollableFrame(help_window, width=450, height=300)
        scrollable_frame.pack(padx=20, pady=10)

        # Texto de ayuda (ejemplo; personalízalo)
        help_text = """
        Bienvenido a la Calculadora de Álgebra Lineal.

        - Menu: Vista principal.
        - Matrices: Operaciones como suma, multiplicación, inversa, etc.
        - Vectores: Cálculos con vectores, ecuaciones, etc.
        - Errores: Revisa logs de errores.

        Para usar: Selecciona una sección y sigue los submenús.

        Preguntas frecuentes:
        - ¿Cómo resolver una matriz? Ve a Matrices > Solucion Matrices.
        - Contacto: soporte@tuapp.com
        """
        help_label = ctk.CTkLabel(scrollable_frame, text=help_text, wraplength=400, justify="left")
        help_label.pack(pady=10)

        close_btn = ctk.CTkButton(help_window, text="Cerrar", command=help_window.destroy)
        close_btn.pack(pady=10)
    
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
