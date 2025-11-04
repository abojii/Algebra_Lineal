import customtkinter as ctk
from tkinter import messagebox
from Interfaz.Matrices import Inversa
from Interfaz.Matrices.determinante import DeterminantCalculator
from Interfaz.Matrices.operacionesMatrices import MatrixCalculator
from Interfaz.Matrices.propiedadesDeterminante import PropiedadesDeterminanteApp
from Interfaz.constantes import COLOR_BG, COLOR_FRAME, COLOR_TEXT, COLOR_SUBTEXT, COLOR_BUTTON, COLOR_ENTRY
from Interfaz.Vectores import sistema_ecuaciones
from Interfaz.Matrices.matrizTraspuesta import MatrixTranspose
from Interfaz.Matrices.Inversa import MatrixInverseApp
from Interfaz.Matrices.propiedadesMultiplicacion import VectorSpaceProperties
from Interfaz.Matrices.propiedadesTraspuesta import MatrixTransposeProperties# Ajusta si es necesario

class SistemaEcuacionesApp:
    def __init__(self, parent):
        self.parent = parent
        # Configura el fondo del parent explícitamente (en lugar de bg)
        self.parent.configure(fg_color=COLOR_BG)
        self.metodo_var = ctk.StringVar(value="gauss")

        # Título
        titulo = ctk.CTkLabel(self.parent, text="Calculadora de Álgebra Lineal",
                              font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                              text_color=COLOR_BUTTON, fg_color="transparent")  # fg_color="transparent" para no sombrear el parent
        titulo.pack(pady=10)

        # Subtítulo
        subtitulo = ctk.CTkLabel(self.parent,
                                 text="Resuelve sistemas de ecuaciones lineales",
                                 font=ctk.CTkFont(family="Segoe UI", size=10),
                                 text_color=COLOR_SUBTEXT, fg_color="transparent")
        subtitulo.pack()

        # Frame de configuración
        frame_config = ctk.CTkFrame(self.parent, fg_color=COLOR_FRAME, corner_radius=0)
        frame_config.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(frame_config, text="Tamaño de la Matriz:",
                     text_color=COLOR_SUBTEXT, font=ctk.CTkFont(size=12), fg_color="transparent").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.matriz_combo = ctk.CTkOptionMenu(frame_config, values=["2x2", "3x3", "4x4"], width=80)
        self.matriz_combo.set("2x2")
        self.matriz_combo.grid(row=0, column=1, padx=5, pady=10)

        ctk.CTkButton(frame_config, text="Generar", command=self.generar_campos,
                      fg_color=COLOR_BUTTON, text_color="white", width=80, height=30).grid(row=0, column=2, padx=5, pady=10)
        ctk.CTkButton(frame_config, text="Resolver", command=self.resolver,
                      fg_color=COLOR_BUTTON, text_color="white", width=80, height=30).grid(row=0, column=3, padx=5, pady=10)
        ctk.CTkButton(frame_config, text="Limpiar", command=self.limpiar,
                      fg_color=COLOR_BUTTON, text_color="white", width=80, height=30).grid(row=0, column=4, padx=5, pady=10)

        # Frame de métodos
        frame_metodos = ctk.CTkFrame(self.parent, fg_color=COLOR_FRAME, corner_radius=0)
        frame_metodos.pack(padx=20, pady=1, fill="x")

        ctk.CTkLabel(frame_metodos, text="Método de resolución", text_color=COLOR_SUBTEXT,
                     font=ctk.CTkFont(size=12), fg_color="transparent").grid(row=0, column=0, columnspan=2, sticky='w', pady=(10, 5), padx=10)

        # Radio buttons (sin selected_color, con fg_color y border_color)
        ctk.CTkRadioButton(frame_metodos, text="Eliminación Gaussiana",
                           variable=self.metodo_var, value="gauss",
                           fg_color=COLOR_FRAME, text_color=COLOR_TEXT,
                           border_color=COLOR_BUTTON, radiobutton_width=20, radiobutton_height=20).grid(row=1, column=0, sticky='w', padx=15, pady=5)
        ctk.CTkRadioButton(frame_metodos, text="Eliminación Gauss-Jordan",
                           variable=self.metodo_var, value="gaussjordan",
                           fg_color=COLOR_FRAME, text_color=COLOR_TEXT,
                           border_color=COLOR_BUTTON, radiobutton_width=20, radiobutton_height=20).grid(row=2, column=0, sticky='w', padx=15, pady=5)
        ctk.CTkRadioButton(frame_metodos, text="Escalonada Matriz",
                           variable=self.metodo_var, value="Escalonada Matriz",
                           fg_color=COLOR_FRAME, text_color=COLOR_TEXT,
                           border_color=COLOR_BUTTON, radiobutton_width=20, radiobutton_height=20).grid(row=3, column=0, sticky='w', padx=15, pady=5)
        ctk.CTkRadioButton(frame_metodos, text="Escalonada Reducida Matriz",
                           variable=self.metodo_var, value="Escalonada Reducida",
                           fg_color=COLOR_FRAME, text_color=COLOR_TEXT,
                           border_color=COLOR_BUTTON, radiobutton_width=20, radiobutton_height=20).grid(row=4, column=0, sticky='w', padx=15, pady=5)

        # Frame para el sistema
        self.frame_sistema = ctk.CTkFrame(self.parent, fg_color=COLOR_FRAME, corner_radius=0)
        self.frame_sistema.pack(fill="both", padx=20, pady=15, expand=True)

        self.entries = []

        # Frame para resultados
        frame_result = ctk.CTkFrame(self.parent, fg_color=COLOR_FRAME, corner_radius=0)
        ctk.CTkLabel(frame_result, text="Resultado", text_color=COLOR_SUBTEXT, font=ctk.CTkFont(size=14, weight="bold"), fg_color="transparent").pack(pady=(10, 5), padx=10, anchor="w")
        frame_result.pack(padx=20, pady=10, fill="both", expand=True)

        self.result_text = ctk.CTkTextbox(frame_result, height=300, fg_color=COLOR_BG, text_color=COLOR_TEXT,
                                          corner_radius=10, scrollbar_button_color=COLOR_BUTTON, scrollbar_button_hover_color=COLOR_BUTTON)
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)  # Cambié side="left" a fill="both" para mejor ajuste

    # Los métodos restantes (generar_campos, resolver, etc.) permanecen iguales, ya que no usan bg
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

        ctk.CTkLabel(self.frame_sistema, text=f"Ingrese los coeficientes de A ({filas}x{columnas}) y b ({filas}x1):",
                     text_color=COLOR_SUBTEXT, font=ctk.CTkFont(size=12), fg_color="transparent").pack(anchor="w", padx=10, pady=5)

        grid = ctk.CTkFrame(self.frame_sistema, fg_color=COLOR_FRAME, corner_radius=0)
        grid.pack(pady=10)

        for i in range(filas):
            fila = []
            for j in range(columnas):
                e = ctk.CTkEntry(grid, width=60, height=30, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT,
                                 placeholder_text="", corner_radius=5)
                e.grid(row=i, column=j, padx=5, pady=5)
                fila.append(e)
            e = ctk.CTkEntry(grid, width=60, height=30, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT,
                             placeholder_text="", corner_radius=5)
            e.grid(row=i, column=columnas, padx=5, pady=5)
            fila.append(e)
            self.entries.append(fila)

    def resolver(self):
        metodo = self.metodo_var.get()
        if not self.entries:
            messagebox.showwarning("Atención", "Primero genera el sistema.")
            return
        try:
            self._resolver(metodo)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese solo números.")

    def _resolver(self, metodo):
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

        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", resultado)

    def limpiar(self):
        for widget in self.frame_sistema.winfo_children():
            widget.destroy()
        self.entries = []
        self.result_text.delete("1.0", "end")
 

class Matrices:
    def __init__(self, parent, show_subframe_callback):
        self.parent = parent
        self.parent.configure(fg_color=COLOR_BG)  # Corregido: fg_color en lugar de bg
        self.show_subframe_callback = show_subframe_callback  # Callback para cambiar sub-frames
        
        # Frame contenedor para sub-contenido (donde se cargan las sub-ventanas)
        self.sub_content_frame = ctk.CTkFrame(self.parent, fg_color=COLOR_BG, corner_radius=0)
        self.sub_content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Diccionario de sub-frames (se crean lazy, solo cuando se necesitan)
        self.sub_frames = {}
        
        # Mostrar sub-ventana principal por defecto
        self.show_subframe("principal")
        
    def show_subframe(self, name):
        """Muestra/oculta sub-frames dentro de Vectores."""
        # Ocultar todos los sub-frames
        for sub_frame in self.sub_frames.values():
            sub_frame.pack_forget()
        
        # Crear si no existe
        if name not in self.sub_frames:
            if name == "principal":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                SistemaEcuacionesApp(self.sub_frames[name])
            elif name == "sub1":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                # VectorEquationSolver(self.sub_frames[name])  # Descomenta cuando esté adaptado
                MatrixCalculator(self.sub_frames[name])  # Usa placeholder por ahora
            elif name == "sub_traspuesta":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                frame = MatrixTranspose(self.sub_frames[name])
                frame.pack(fill="both", expand=True)
            elif name == "Inversa":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                frame = MatrixInverseApp(self.sub_frames[name])
                frame.pack(fill="both", expand=True)
            elif name == "Propiedades":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                frame = VectorSpaceProperties(self.sub_frames[name])
                frame.pack(fill="both", expand=True)
            elif name == "Ptraspuesta":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                frame = MatrixTransposeProperties(self.sub_frames[name])
                frame.pack(fill="both", expand=True)
            elif name == "DeterminanteMa":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                frame = DeterminantCalculator(self.sub_frames[name])
                frame.pack(fill="both", expand=True)
            elif name == "DeterPropiedades":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                frame = PropiedadesDeterminanteApp(self.sub_frames[name])
                frame.pack(fill="both", expand=True)
            else:
                print("NO SE ABRIO")
                return
        
        # Mostrar el seleccionado
        self.sub_frames[name].pack(fill="both", expand=True)
        
        # Llamar callback para actualizar menú en MainApp (opcional, para sincronizar)
        if self.show_subframe_callback:
            self.show_subframe_callback(name)

            
class SubVentana2:
    """Sub-ventana 2: Propiedades Algebraicas de ℝⁿ (placeholder adaptado; integra VectorAlgebraPropertiesGUI si está adaptado)."""
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color=COLOR_BG)  # Corregido: fg_color en lugar de bg
        
        titulo = ctk.CTkLabel(self.parent, text="Sub-Ventana 2: Propiedades Algebraicas de ℝⁿ",
                              text_color=COLOR_TEXT, fg_color="transparent",
                              font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"))
        titulo.pack(pady=20)
        
        # Placeholder para contenido (integra aquí VectorAlgebraPropertiesGUI si está adaptado a CTk)
        # from .propiedadesAlgb_Rn import VectorAlgebraPropertiesGUI
        # VectorAlgebraPropertiesGUI(self.parent)  # Descomenta cuando esté adaptado
        
        descripcion = ctk.CTkLabel(self.parent, text="Contenido para Propiedades de ℝⁿ (en desarrollo).\nUsa el menú lateral para navegar.",
                                   text_color=COLOR_SUBTEXT, fg_color="transparent",
                                   font=ctk.CTkFont(size=12))
        descripcion.pack(pady=10)
        
        # Ejemplo de input (adaptado)
        entry_ejemplo = ctk.CTkEntry(self.parent, width=300, height=30, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT,
                                      placeholder_text="Ejemplo de entrada...")
        entry_ejemplo.pack(pady=10)
        
        btn_ejemplo = ctk.CTkButton(self.parent, text="Ejemplo de Acción",
                                    fg_color=COLOR_BUTTON, text_color="white", corner_radius=5, height=30)
        btn_ejemplo.pack(pady=5)
