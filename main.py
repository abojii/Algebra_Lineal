import customtkinter as ctk
from Models.sistemaApp import SistemaEcuacionesApp
from Models.sistemaApp import Matrices
from Interfaz.vectores import SubVentana3
from Interfaz.constantes import COLOR_BG, COLOR_FRAME, COLOR_BUTTON
from Interfaz.vectores import Vectores  # Si Vectores usa 'bg', esto fallará; adáptalo a CTk

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicacion Calculadora algebra lineal")
        self.geometry("900x600")
        self.configure(fg_color=COLOR_BG)

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

        frame_calc = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0)
        self.frames["calc"] = frame_calc
        self.sistema_app = SistemaEcuacionesApp(frame_calc)
        
        # Frame para la calculadora de álgebra lineal
        
        # Frame para el menu principal
        frame_menu = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0)
        self.frames["menu"] = frame_menu
        self.sistema_app = SubVentana3(frame_menu)

        # Frame para la calculadora de álgebra lineal (Matrices)
        frame_calc = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0)
        self.frames["calc"] = frame_calc
        self.sistema_app = Matrices(frame_calc, lambda *args: self.update_sub_menu2(*args))

        # Frame para vectores
        frame_otra = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BG, corner_radius=0)
        self.frames["otra"] = frame_otra
        # Corrige el callback para preservar 'self'
        self.other_app = Vectores(frame_otra, lambda *args: self.update_sub_menu(*args))  # Pasa callback enlazado

        # Mostrar inicialmente el menú
        self.show_frame("menu")

        self.menu_visible = True
        self.current_subframe = "principal"
        self.sub_menu_buttons = {}  # Inicializado aquí para seguridad
        self.sub_menu_buttons2 = {}  # Para el segundo submenú
        self.sub_menu_active = False
        self.sub_menu_visible = True
        self.sub_menu_active2 = False
        self.sub_menu_visible2 = True

    def create_menu_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

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
                    self.toggle_sub_menu()  # Expande si estaba colapsado
              # Expande si estaba colapsado
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

        num_opciones = 5
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
        opciones = [("Solucion Matrices", "principal"), ("Operaciones con Matrices", "sub1"),("Matriz Trazpuesta", "sub_traspuesta"),("Matriz Inversa", "Inversa")]

        for text, sub_name in opciones:
            btn = ctk.CTkButton(self.sub_menu_frame2, text=text, fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=30, command=lambda n=sub_name: self.change_subframe2(n))
            btn.pack(fill="x", pady=2, padx=10)
            self.sub_menu_buttons2[sub_name] = btn

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
        if hasattr(self, 'sistema_app') and self.other_app:
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

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()