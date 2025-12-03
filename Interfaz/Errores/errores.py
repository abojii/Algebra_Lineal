import customtkinter as ctk
import math
import numpy as np  # Ahora permitido usar NumPy
from tkinter import messagebox

from Interfaz.Errores.calculos_notacion import PositionalNotation
from Interfaz.Errores.errores_numericos import NumericalErrors
from Interfaz.Errores.metodonumerico2 import NumericalMethodsCalculator

# ===== Colores personalizados =====
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"
COLOR_BUTTON1 = "#f87171"
COLOR_BUTTON2 = "#4ade80"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ErrorCalculator(ctk.CTkFrame):
    def __init__(self, parent, callback=None):  # Agregado callback opcional para integración
        super().__init__(parent, fg_color=COLOR_BG)
        self.parent = parent
        self.callback = callback  # No se usa en esta clase, pero permite integración
        self.pack(fill="both", expand=True)  # Mantiene el pack para que aparezca en el frame padre

        # --- Título ---
        title_label = ctk.CTkLabel(self,
                                   text="Calculadora de Errores",
                                   font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                                   text_color=COLOR_BUTTON)
        title_label.pack(pady=(10))

        # --- Controles superiores ---
        header = ctk.CTkFrame(self, fg_color=COLOR_FRAME)
        header.pack(padx=10, pady=10, fill="x")

        # Entradas dinámicas
        self.label1 = ctk.CTkLabel(header, text="Valor verdadero (x_v):", text_color=COLOR_TEXT)
        self.label1.grid(row=0, column=0, padx=10, pady=10)
        self.entry1 = ctk.CTkEntry(header, width=100, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT, placeholder_text="Ej: 1.0")
        self.entry1.grid(row=0, column=1, padx=5)

        self.label2 = ctk.CTkLabel(header, text="Valor aproximado (x_a):", text_color=COLOR_TEXT)
        self.label2.grid(row=0, column=2, padx=10)
        self.entry2 = ctk.CTkEntry(header, width=100, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT, placeholder_text="Ej: 0.9")
        self.entry2.grid(row=0, column=3, padx=5)

        # Selección de método de error
        ctk.CTkLabel(header, text="Método:", text_color=COLOR_TEXT).grid(row=0, column=4, padx=10)
        self.method_var = ctk.StringVar(value="Error absoluto")
        self.method_menu = ctk.CTkOptionMenu(header,
                                             values=["Error absoluto", "Error relativo", "Propagación de error"],
                                             variable=self.method_var,
                                             fg_color=COLOR_BUTTON,
                                             command=self.update_ui)
        self.method_menu.grid(row=0, column=5, padx=5)

        # Menú para función f(x), inicialmente oculto
        self.func_label = ctk.CTkLabel(header, text="Función f(x):", text_color=COLOR_TEXT)
        self.func_var = ctk.StringVar(value="sin(x)")
        self.func_menu = ctk.CTkOptionMenu(header,
                                           values=["sin(x)", "sin(x) + x^2", "x^2", "cos(x)"],
                                           variable=self.func_var,
                                           fg_color=COLOR_BUTTON)
        # Inicialmente ocultar
        self.func_label.grid_remove()
        self.func_menu.grid_remove()

        # Botones
        ctk.CTkButton(header, text="Calcular", fg_color=COLOR_BUTTON2, text_color="black",
                      command=self.calcular).grid(row=0, column=6, padx=10)
        ctk.CTkButton(header, text="Limpiar", fg_color=COLOR_BUTTON1, text_color="black",
                      command=self.clear_all).grid(row=0, column=7, padx=10)

        # --- Área de resultados ---
        result_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME)
        result_frame.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(result_frame, text="Pasos y resultados:", text_color=COLOR_TEXT).pack(anchor="w", padx=10, pady=5)
        self.result_box = ctk.CTkTextbox(result_frame, height=400, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT,
                                         font=ctk.CTkFont(size=16))  # Tamaño de fuente aumentado
        self.result_box.pack(fill="both", padx=10, pady=5, expand=True)

    def update_ui(self, selected_method):
        if selected_method == "Propagación de error":
            self.label1.configure(text="x:")
            self.entry1.configure(placeholder_text="Ej: 0.5")
            self.label2.configure(text="Δx:")
            self.entry2.configure(placeholder_text="Ej: 0.002")
            self.func_label.grid(row=0, column=8, padx=10)
            self.func_menu.grid(row=0, column=9, padx=5)
        else:
            self.label1.configure(text="Valor verdadero (x_v):")
            self.entry1.configure(placeholder_text="Ej: 1.0")
            self.label2.configure(text="Valor aproximado (x_a):")
            self.entry2.configure(placeholder_text="Ej: 0.9")
            self.func_label.grid_remove()
            self.func_menu.grid_remove()

    # Función para evaluar f(x) según selección
    def f(self, x):
        func = self.func_var.get()
        if func == "sin(x)":
            return np.sin(x)
        elif func == "sin(x) + x^2":
            return np.sin(x) + x**2
        elif func == "x^2":
            return x**2
        elif func == "cos(x)":
            return np.cos(x)
        else:
            return 0  # Default

    # Función para evaluar f'(x) según selección
    def f_prime(self, x):
        func = self.func_var.get()
        if func == "sin(x)":
            return np.cos(x)
        elif func == "sin(x) + x^2":
            return np.cos(x) + 2 * x
        elif func == "x^2":
            return 2 * x
        elif func == "cos(x)":
            return -np.sin(x)
        else:
            return 0  # Default

    # Función auxiliar para obtener la cadena de la derivada
    def get_derivative_str(self):
        func = self.func_var.get()
        if func == "sin(x)":
            return "cos(x)"
        elif func == "sin(x) + x^2":
            return "cos(x) + 2x"
        elif func == "x^2":
            return "2x"
        elif func == "cos(x)":
            return "-sin(x)"
        else:
            return "0"

    # Función para calcular el error absoluto
    def calcular_error_absoluto(self, x_v, x_a):
        return abs(x_v - x_a)

    # Función para calcular el error relativo
    def calcular_error_relativo(self, x_v, x_a):
        if x_v == 0:
            return float('inf')  # Evitar división por cero
        return abs(x_v - x_a) / abs(x_v)

    # Función principal para calcular y mostrar resultados
    def calcular(self):
        try:
            method = self.method_var.get()
            val1 = float(self.entry1.get())
            val2 = float(self.entry2.get())
            
            # Limpiar el área de resultados
            self.result_box.delete("1.0", ctk.END)
            
            steps_text = "Cálculos paso a paso:\n\n"
            
            if method == "Error absoluto":
                x_v = val1
                x_a = val2
                steps_text += f"Valor verdadero (x_v): {x_v}\n"
                steps_text += f"Valor aproximado (x_a): {x_a}\n\n"
                e_a = self.calcular_error_absoluto(x_v, x_a)
                steps_text += "Error absoluto (E_a = |x_v - x_a|):\n"
                steps_text += f"E_a = |{x_v} - {x_a}| = {e_a}\n\n"
                steps_text += "Interpretación:\n"
                steps_text += f"- El error absoluto ({e_a:.6f}) mide la magnitud del error en la aproximación.\n"
            
            elif method == "Error relativo":
                x_v = val1
                x_a = val2
                steps_text += f"Valor verdadero (x_v): {x_v}\n"
                steps_text += f"Valor aproximado (x_a): {x_a}\n\n"
                e_r = self.calcular_error_relativo(x_v, x_a)
                steps_text += "Error relativo (E_r = |x_v - x_a| / |x_v|):\n"
                if x_v == 0:
                    steps_text += "E_r = indefinido (división por cero)\n\n"
                    steps_text += "Interpretación:\n"
                    steps_text += "- El error relativo es indefinido porque el valor verdadero es cero.\n"
                else:
                    steps_text += f"E_r = |{x_v} - {x_a}| / |{x_v}| = {abs(x_v - x_a)} / {abs(x_v)} = {e_r}\n\n"
                    steps_text += "Interpretación:\n"
                    steps_text += f"- El error relativo ({e_r:.6f}) indica la fracción del error respecto al valor verdadero.\n"
            
            elif method == "Propagación de error":
                x = val1
                delta_x = val2
                func_str = self.func_var.get()
                steps_text += f"Propagación del error en f(x) = {func_str}:\n"
                steps_text += f"**Datos:** f(x) = {func_str}, x = {x}, Δx = {delta_x}\n"
                steps_text += "**Calcular:** Δy ≈ f'(x) Δx\n\n"
                steps_text += "**Solución:**\n\n"
                
                # Paso 1: Calcular f'(x)
                f_prime_val = self.f_prime(x)
                steps_text += f"1. f'(x) = {self.get_derivative_str()}, Para x = {x}, f'({x}) = {f_prime_val:.6f}\n\n"
                
                # Paso 2: Aproximación lineal
                delta_y_approx = f_prime_val * delta_x
                steps_text += f"2. Aproximación lineal (diferencial): Δy ≈ f'({x}) · {delta_x} = {f_prime_val:.6f} · {delta_x} = {delta_y_approx:.6f}\n\n"
                
                # Paso 3: Cálculo exacto
                f_x = self.f(x)
                f_x_plus_delta = self.f(x + delta_x)
                delta_y_exact = f_x_plus_delta - f_x
                steps_text += f"3. Cálculo exacto (valor real): f({x + delta_x}) - f({x}) = {f_x_plus_delta:.6f} - {f_x:.6f} = {delta_y_exact:.6f}\n\n"
                
                # Análisis del error
                error_abs = abs(delta_y_exact - delta_y_approx)
                steps_text += f"**Análisis del error:** Error absoluto |Δy_real - Δy_aprox| = |{delta_y_exact:.6f} - {delta_y_approx:.6f}| = {error_abs:.6f}\n\n"
                
                steps_text += "Interpretación:\n"
                steps_text += f"- La propagación del error ({abs(delta_y_approx):.6f}) estima cómo el cambio Δx en x afecta a f(x), usando diferenciales.\n"
                steps_text += f"  (f(x) = {f_x:.6f}, f(x + Δx) = {f_x_plus_delta:.6f})\n"
            
            self.result_box.insert("end", steps_text)
            
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos.")

    # --- Limpiar todo ---
    def clear_all(self):
        self.entry1.delete(0, "end")
        self.entry2.delete(0, "end")
        self.result_box.delete("1.0", "end")


class Errores(ctk.CTkFrame):
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
        self.show_subframe("NotaPosi")
        
    def show_subframe(self, name):
        """Muestra/oculta sub-frames dentro de Vectores."""
        # Ocultar todos los sub-frames
        for sub_frame in self.sub_frames.values():
            sub_frame.pack_forget()
        
        # Crear si no existe
        if name not in self.sub_frames:
            if name == "NotaPosi":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                frame = PositionalNotation(self.sub_frames[name])
                frame.pack(fill="both", expand=True)
            elif name == "ConsepEr":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                frame = NumericalErrors(self.sub_frames[name])
                frame.pack(fill="both", expand=True)
            elif name == "Err":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                frame = ErrorCalculator(self.sub_frames[name])
                frame.pack(fill="both", expand=True)
            elif name == "metoNum":
                self.sub_frames[name] = ctk.CTkFrame(self.sub_content_frame, fg_color=COLOR_BG, corner_radius=0)
                frame = NumericalMethodsCalculator(self.sub_frames[name])
                frame.pack(fill="both", expand=True)
            else:
                print("NO SE ABRIO")
                return
        
        # Mostrar el seleccionado
        self.sub_frames[name].pack(fill="both", expand=True)
        
        # Llamar callback para actualizar menú en MainApp (opcional, para sincronizar)
        if self.show_subframe_callback:
            self.show_subframe_callback(name)

            
