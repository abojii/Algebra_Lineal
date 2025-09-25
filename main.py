import tkinter as tk
import os
import sys
from Interfaz.sistema_ecuaciones import SistemaEcuacionesApp
from Interfaz.vectores import Vectores
from Interfaz.vectores import SubVentana1,SubVentana2

COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"



# Configurar sys.path (como antes)
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'Interfaz'))



class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicacion Calculadora algebra lineal")
        self.geometry("900x600")
        self.configure(bg=COLOR_BG)

        # MenúBar global (inicialmente vacío)
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)  # Asocia el menú a la ventana raíz
        self.sub_menu = None  # Sub-menú para 'Otra Opción'

        # Frame para el botón toggle (siempre visible)
        self.toggle_frame = tk.Frame(self, width=30, bg=COLOR_FRAME)
        self.toggle_frame.pack(side="left", fill="y")

        self.toggle_button = tk.Button(self.toggle_frame, text="<<", command=self.toggle_menu,
                                       bg=COLOR_BUTTON, fg="white", relief="flat")
        self.toggle_button.pack(pady=10)

        # Frame para el menú lateral (ocultable)
        self.menu_frame = tk.Frame(self, width=150, bg=COLOR_FRAME)
        self.menu_frame.pack(side="left", fill="y")

        # Frame para los botones del menú
        self.buttons_frame = tk.Frame(self.menu_frame, bg=COLOR_FRAME)
        self.buttons_frame.pack(fill="both", expand=True)

        self.create_menu_buttons()

        # Frame para el contenido principal (a la derecha)
        self.content_frame = tk.Frame(self, bg=COLOR_BG)
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Crear frames para cada "pantalla"
        self.frames = {}

        # Frame para la calculadora
        frame_calc = tk.Frame(self.content_frame, bg=COLOR_BG)
        self.frames["calc"] = frame_calc
        self.sistema_app = SistemaEcuacionesApp(frame_calc)

        # Frame para otra ventana (ahora con callback para sub-frames)
        frame_otra = tk.Frame(self.content_frame, bg=COLOR_BG)
        self.frames["otra"] = frame_otra
        self.other_app = Vectores(frame_otra, self.update_sub_menu)  # Pasa callback para menú

        # Mostrar inicialmente solo la calculadora (menú vacío)
        self.show_frame("calc")

        self.menu_visible = True
        self.current_subframe = "principal"  # Rastrea sub-frame actual

    def create_menu_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        btn1 = tk.Button(self.buttons_frame, text="Álgebra Lineal",
                         bg=COLOR_BUTTON, fg="white", relief="flat",
                         command=lambda: self.show_frame("calc"))
        btn1.pack(fill="x", pady=5, padx=5)

        btn2 = tk.Button(self.buttons_frame, text="Vectores",
                         bg=COLOR_BUTTON, fg="white", relief="flat",
                         command=lambda: self.show_frame("otra"))
        btn2.pack(fill="x", pady=5, padx=5)

    def toggle_menu(self):
        if self.menu_visible:
            self.menu_frame.pack_forget()
            self.menu_visible = False
            self.toggle_button.config(text=">>")
        else:
            self.menu_frame.pack(side="left", fill="y", before=self.content_frame)
            self.menu_visible = True
            self.toggle_button.config(text="<<")

    def show_frame(self, name):
        # Ocultar todos los frames
        for f in self.frames.values():
            f.pack_forget()

        if frame := self.frames.get(name):
            frame.pack(fill="both", expand=True)

            # Configurar menú dinámicamente
            if name == "otra":
                self.setup_sub_menu()  # Crea/actualiza menú para sub-ventanas
            else:
                self.clear_menu()  # Limpia menú para otras ventanas (ej: calc)

    def setup_sub_menu(self):
        """Crea el sub-menú para 'Otra Opción' (si no existe)."""
        if self.sub_menu:
            return  # Ya existe
        
        # Crear menú principal (ej: "Archivo" o directamente opciones)
        self.sub_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Sub-Menú (Otra Opción)", menu=self.sub_menu)
        
        # Opciones del menú (puedes agregar más)
        self.sub_menu.add_command(label="Matriz-Vector (Ax)", command=lambda: self.change_subframe("principal"))
        self.sub_menu.add_command(label="Ecucaion Vectorial", command=lambda: self.change_subframe("sub1"))
        self.sub_menu.add_command(label="Propiedades algebraicas de ℝⁿ", command=lambda: self.change_subframe("sub2"))
        self.sub_menu.add_separator()
        self.sub_menu.add_command(label="Salir de Sub-Menú", command=self.clear_menu)  # Opcional: ocultar menú
        
        # Marcar la actual
        self.update_sub_menu(self.current_subframe)

    def change_subframe(self, sub_name):
        """Cambia a una sub-ventana en OtherScreen."""
        if hasattr(self, 'other_app'):
            self.other_app.show_subframe(sub_name)
            self.current_subframe = sub_name
            self.update_sub_menu(sub_name)

    def update_sub_menu(self, active_name):
        """Actualiza el menú para resaltar la opción activa (simulado con enable/disable)."""
        if not self.sub_menu:
            return
        # Deshabilita todas y habilita la activa (ejemplo simple)
        for item in self.sub_menu.entryconfig("label"):
            self.sub_menu.entryconfig(item, state="normal")  # O usa underline para resaltar
        # Puedes agregar lógica para checkbuttons si quieres radio-buttons

    def clear_menu(self):
        """Limpia el sub-menú cuando sales de 'Otra Opción'."""
        if self.sub_menu:
            self.menubar.delete(0, tk.END)  # Borra todo el menú
            self.sub_menu = None
            self.current_subframe = "principal"

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
