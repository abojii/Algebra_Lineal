import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from Interfaz import sistema_ecuaciones
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

# clase de la calculadora de sistemas(la interfaz Tkinter)
class SistemaEcuacionesApp:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg=COLOR_BG)
        self.metodo_var = tk.StringVar(value="gauss")

        titulo = tk.Label(parent, text="Calculadora de Álgebra Lineal",
                          font=("Segoe UI", 18, "bold"),
                          fg=COLOR_BUTTON, bg=COLOR_BG)
        titulo.pack(pady=10)

        subtitulo = tk.Label(parent,
                             text="Resuelve sistemas de ecuaciones lineales",
                             font=("Segoe UI", 10),
                             fg=COLOR_SUBTEXT, bg=COLOR_BG)
        subtitulo.pack()

        frame_config = tk.Frame(parent, bg=COLOR_FRAME, bd=1, relief="solid")
        frame_config.pack(fill="x", padx=20, pady=15)

        tk.Label(frame_config, text="Tamaño de la Matriz:",
                 fg=COLOR_SUBTEXT, bg=COLOR_FRAME).grid(row=0, column=0, padx=10, pady=10)

        self.matriz_combo = ttk.Combobox(frame_config, values=["2x2", "3x3", "4x4"], width=10)
        self.matriz_combo.set("2x2")
        self.matriz_combo.grid(row=0, column=1, padx=5, pady=10)

        ttk.Button(frame_config, text="Generar", command=self.generar_campos).grid(row=0, column=2, padx=5)
        ttk.Button(frame_config, text="Resolver", command=self.resolver).grid(row=0, column=3, padx=5)
        ttk.Button(frame_config, text="Limpiar", command=self.limpiar).grid(row=0, column=4, padx=5)

        frame_metodos = tk.LabelFrame(parent, bg=COLOR_FRAME, bd=1, relief="solid")
        frame_metodos.pack(padx=20, pady=1, fill="x")

        tk.Label(frame_metodos, text="Método de resolución", fg=COLOR_SUBTEXT, bg=COLOR_FRAME).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))

        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Eliminación Gaussiana",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="gauss", padx=10).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Eliminación Gauss-Jordan",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="gaussjordan", padx=10).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Escalonada Matriz",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="Escalonada Matriz", padx=10).grid(row=3, column=0, sticky='w', padx=5, pady=2)
        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Escalonada Reducida Matriz",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="Escalonada Reducida", padx=10).grid(row=1, column=1, sticky='w', padx=5, pady=2)

        self.frame_sistema = tk.Frame(parent, bg=COLOR_FRAME, bd=1, relief="solid")
        self.frame_sistema.pack(fill="both", padx=20, pady=15, expand=True)

        self.entries = []
        # Frame para resultados
        frame_result = tk.LabelFrame(parent, text="Resultado", fg=COLOR_SUBTEXT, bg=COLOR_FRAME)
        frame_result.pack(padx=20, pady=10, fill="both", expand=True)

        # Cuadro de texto con scrollbar
        self.result_text = tk.Text(frame_result, height=15, bg=COLOR_BG, fg=COLOR_TEXT,
                           insertbackground="white", wrap="word")
        self.result_text.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(frame_result, command=self.result_text.yview)
        scroll.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scroll.set)

    def generar_campos(self):
        for widget in self.frame_sistema.winfo_children():
            widget.destroy()
        self.entries = []

        dim_text = self.matriz_combo.get().lower().replace(" ", "")
        try:
            filas_str, columnas_str = dim_text.split("x")
            filas = int(filas_str)
            columnas = int(columnas_str)
        except Exception:
            messagebox.showerror("Error", "Formato inválido. Use 'filas x columnas'.")
            return

        tk.Label(self.frame_sistema, text=f"Ingrese los coeficientes de A ({filas}x{columnas}) y b ({filas}x1):",
                 fg=COLOR_SUBTEXT, bg=COLOR_FRAME).pack(anchor="w", padx=10, pady=5)

        grid = tk.Frame(self.frame_sistema, bg=COLOR_FRAME)
        grid.pack(pady=10)

        for i in range(filas):
            fila = []
            for j in range(columnas):
                e = tk.Entry(grid, width=5, bg=COLOR_ENTRY, fg=COLOR_TEXT,
                             insertbackground="white", justify="center")
                e.grid(row=i, column=j, padx=5, pady=5)
                fila.append(e)
            e = tk.Entry(grid, width=5, bg=COLOR_ENTRY, fg=COLOR_TEXT,
                         insertbackground="white", justify="center")
            e.grid(row=i, column=columnas, padx=5, pady=5)
            fila.append(e)
            self.entries.append(fila)

    def resolver(self):
        metodo = self.metodo_var.get()
        if not self.entries:
            messagebox.showwarning("Atención", "Primero genera el sistema.")
            return
        try:
            self._extracted_from_resolver_7(metodo)
        except ValueError:
         messagebox.showerror("Error", "Por favor ingrese solo números.")

    # TODO Rename this here and in `resolver`
    def _extracted_from_resolver_7(self, metodo):
        filas = len(self.entries)
        columnas = len(self.entries[0]) - 1
        A = []
        b = []
        for fila in self.entries:
            A.append([float(fila[j].get()) for j in range(columnas)])
            b.append(float(fila[columnas].get()))

        pasos, solucion, clasificacion = [], None, ""

        if metodo == "gauss":
            pasos, solucion, clasificacion = sistema_ecuaciones.gauss(A, b)
        elif metodo == "gaussjordan":
            pasos, solucion, clasificacion = sistema_ecuaciones.gauss_jordan(A, b)
        elif metodo == "Escalonada Matriz":
            pasos, solucion, clasificacion = sistema_ecuaciones.forma_escalonada(A, b)
        elif metodo == "Escalonada Reducida":
            pasos, solucion, clasificacion = sistema_ecuaciones.forma_escalonada_reducida(A, b)

        resultado = "\n".join(pasos)
        if solucion is not None:
            resultado += f"\n\nSolución: {solucion}"
        resultado += f"\n\nClasificación: {clasificacion}"

        self.result_text.delete(1.0, tk.END)   # Limpia antes de mostrar
        self.result_text.insert(tk.END, resultado)

    def limpiar(self):
        for widget in self.frame_sistema.winfo_children():
            widget.destroy()
        self.entries = []
        self.result_text.delete(1.0, tk.END)


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
        self.sub_menu.add_command(label="Ecuaciones Homogenias",command=lambda: self.change_subframe("sub3"))
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



