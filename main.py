import customtkinter as ctk
from Models.sistemaApp import SistemaEcuacionesApp
from Interfaz.constantes import COLOR_BG, COLOR_FRAME, COLOR_BUTTON
from Interfaz.vectores import Vectores  # Si Vectores usa 'bg', esto fallará; adáptalo a CTk

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicacion Calculadora algebra lineal")
        self.geometry("900x600")
        # Configura el fondo de la ventana raíz explícitamente (en lugar de bg)
        self.configure(fg_color=COLOR_BG)

        # Frame toggle (siempre visible)
        self.toggle_frame = ctk.CTkFrame(self, width=30, fg_color=COLOR_FRAME, corner_radius=0)
        self.toggle_frame.pack(side="left", fill="y")

        self.toggle_button = ctk.CTkButton(self.toggle_frame, text="<<", command=self.toggle_menu,
                                           fg_color=COLOR_BUTTON, text_color="white", width=30, height=30, corner_radius=5)
        self.toggle_button.pack(pady=10, padx=5)

        # Frame para el menú lateral (ocultable inicialmente visible)
        self.menu_frame = ctk.CTkFrame(self, width=150, fg_color=COLOR_FRAME, corner_radius=0)
        self.menu_frame.pack(side="left", fill="y")

        # Frame para los botones del menú principal
        self.buttons_frame = ctk.CTkFrame(self.menu_frame, fg_color=COLOR_FRAME, corner_radius=0)
        self.buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_menu_buttons()

        # Frame para el contenido principal (a la derecha)
        self.content_frame = ctk.CTkFrame(self, fg_color=COLOR_BG, corner_radius=0)
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Crear frames para cada "pantalla"
        self.frames = {}

        # Frame para la calculadora de álgebra lineal
        frame_calc = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0)
        self.frames["calc"] = frame_calc
        self.sistema_app = SistemaEcuacionesApp(frame_calc)

        # Frame para vectores (asumiendo Vectores adaptado a CTk)
        frame_otra = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0)
        self.frames["otra"] = frame_otra
        # ADVERTENCIA: Si Vectores no está adaptado (usa 'bg' o tk.widgets), comenta esta línea y agrega un placeholder
        self.other_app = Vectores(frame_otra, self.update_sub_menu)  # Pasa callback para sub-menú

        # Mostrar inicialmente la calculadora
        self.show_frame("calc")

        self.menu_visible = True
        self.current_subframe = "principal"  # Rastrea sub-frame actual

        # Diccionario para botones del sub-menú (para resaltar el activo)
        self.sub_menu_buttons = {}

        # CAMBIO: Flags para manejar overlay y colapso
        self.sub_menu_active = False
        self.sub_menu_visible = True  # Inicialmente visible cuando se activa

    def create_menu_buttons(self):
        """Crea los botones principales del menú lateral."""
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        btn1 = ctk.CTkButton(self.buttons_frame, text="Álgebra Lineal",
                             fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=40,
                             command=lambda: self.show_frame("calc"))
        btn1.pack(fill="x", pady=5, padx=5)

        btn2 = ctk.CTkButton(self.buttons_frame, text="Vectores",
                             fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=40,
                             command=lambda: self.show_frame("otra"))
        btn2.pack(fill="x", pady=5, padx=5)

    def toggle_menu(self):
        """Alterna la visibilidad del menú lateral."""
        if self.menu_visible:
            self.menu_frame.pack_forget()
            self.menu_visible = False
            self.toggle_button.configure(text=">>")
        else:
            self.menu_frame.pack(side="left", fill="y", before=self.content_frame)
            self.menu_visible = True
            self.toggle_button.configure(text="<<")

    def show_frame(self, name):
        """Muestra el frame correspondiente y configura el sub-menú si aplica."""
        # FIX: Ocultar todos los frames directamente (sin verificaciones, es seguro en Tkinter)
        for f in self.frames.values():
            f.pack_forget()
            f.grid_forget()

        if frame := self.frames.get(name):
            # CAMBIO: Siempre usa pack para el contenido (ocupa todo el espacio)
            frame.pack(fill="both", expand=True)

            if name == "otra":
                # Activar modo submenú overlay
                self.setup_sub_menu()  # Crea/actualiza sub-menú como overlay
                self.sub_menu_active = True
                # Si estaba colapsado, mostrarlo de nuevo (opcional)
                if hasattr(self, 'sub_menu_frame') and not self.sub_menu_visible:
                    self.toggle_sub_menu()  # Expande si estaba colapsado
            else:
                self.clear_menu()  # Limpia sub-menú
                self.sub_menu_active = False

    def setup_sub_menu(self):
        """Crea el sub-menú para la sección de Vectores como overlay en superior izquierda."""
        if hasattr(self, 'sub_menu_frame') and self.sub_menu_frame.winfo_exists():
            # Si ya existe, solo posicionarlo si no está visible
            if not self.sub_menu_visible:
                self.sub_menu_frame.place(x=10, y=10)
                self.sub_menu_visible = True
            return

        # CAMBIO: Crear frame para sub-botones como overlay (place en content_frame)
        # Ancho fijo, altura dinámica
        num_opciones = 5  # 4 opciones + 1 salir/colapsar
        height = num_opciones * 35 + 40  # Aprox: 30px botón + padding + título

        self.sub_menu_frame = ctk.CTkFrame(
            self.content_frame,
            width=250,
            height=height,
            fg_color=COLOR_FRAME,
            corner_radius=10,
            border_width=2,  # CAMBIO: Borde para simular elevación/sombra
            border_color="#333333"  # Color oscuro para sombra sutil
        )
        # Posicionar como overlay en superior izquierda (no afecta pack del contenido)
        self.sub_menu_frame.place(x=10, y=10)

        # Título del submenú con botón colapsar
        title_frame = ctk.CTkFrame(self.sub_menu_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(10, 5))

        sub_title = ctk.CTkLabel(
            title_frame,
            text="Submenú Vectores",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        sub_title.pack(side="left")

        # CAMBIO: Botón para colapsar (oculta submenú temporalmente)
        collapse_btn = ctk.CTkButton(
            title_frame,
            text="X",
            width=20, height=20,
            fg_color="red",
            text_color="white",
            corner_radius=10,
            command=self.toggle_sub_menu,
            hover_color="darkred"
        )
        collapse_btn.pack(side="right", padx=(5, 0))

        # Crear botones del sub-menú
        self.sub_menu_buttons = {}
        opciones = [
            ("Matriz-Vector (Ax)", "principal"),
            ("Ecuación Vectorial", "sub1"),
            ("Propiedades algebraicas de ℝⁿ", "sub2"),
            ("Ecuaciones Homogéneas", "sub3")
        ]

        for text, sub_name in opciones:
            btn = ctk.CTkButton(
                self.sub_menu_frame,
                text=text,
                fg_color=COLOR_BUTTON,
                text_color="white",
                corner_radius=5,
                height=30,
                command=lambda n=sub_name: self.change_subframe(n)
            )
            btn.pack(fill="x", pady=2, padx=10)
            self.sub_menu_buttons[sub_name] = btn

        # Botón para salir del sub-menú (destruye completamente)
        salir_btn = ctk.CTkButton(
            self.sub_menu_frame,
            text="Salir de Sub-Menú",
            fg_color="red",
            text_color="white",
            corner_radius=5,
            height=30,
            command=self.clear_menu
        )
        salir_btn.pack(fill="x", pady=(5, 10), padx=10)

        # Marcar la opción actual
        self.update_sub_menu(self.current_subframe)

        self.sub_menu_visible = True

    def toggle_sub_menu(self):
        """CAMBIO: Alterna visibilidad del submenú (colapsa/expande sin destruir)."""
        if self.sub_menu_visible:
            self.sub_menu_frame.place_forget()
            self.sub_menu_visible = False
            # Opcional: Cambiar texto del botón a "+" o algo, pero por simplicidad usamos "X" siempre
        else:
            self.sub_menu_frame.place(x=10, y=10)
            self.sub_menu_visible = True

    def change_subframe(self, sub_name):
        """Cambia a una sub-ventana en la sección de Vectores."""
        if hasattr(self, 'other_app') and self.other_app:
            self.other_app.show_subframe(sub_name)
            self.current_subframe = sub_name
            self.update_sub_menu(sub_name)
        else:
            # Placeholder si Vectores no está disponible
            print(f"Cambiando a subframe: {sub_name} (Vectores no inicializado)")

    def update_sub_menu(self, active_name):
        """Actualiza el sub-menú para resaltar la opción activa (cambia color del botón)."""
        if not hasattr(self, 'sub_menu_buttons') or not self.sub_menu_buttons:
            return

        # Resetear colores de todos los botones a normal
        for btn in self.sub_menu_buttons.values():
            btn.configure(fg_color=COLOR_BUTTON)

        # Resaltar el botón activo con un color más claro
        if active_name in self.sub_menu_buttons:
            self.sub_menu_buttons[active_name].configure(fg_color="#60a5fa")  # Azul claro para resaltar

    def clear_menu(self):
        """Limpia el sub-menú completamente cuando sales de Vectores."""
        if hasattr(self, 'sub_menu_frame') and self.sub_menu_frame.winfo_exists():
            self.sub_menu_frame.destroy()
            del self.sub_menu_frame
            self.sub_menu_buttons = {}
        
        self.current_subframe = "principal"
        self.sub_menu_active = False
        self.sub_menu_visible = True  # Reset para próxima vez


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
