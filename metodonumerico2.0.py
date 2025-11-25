import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter as ctk
from tkinter import messagebox
import math
import tkinter as tk  
from Models import biseccion
from Models import regla_falsa
from Models.biseccion import metodo_biseccion
from Models.regla_falsa import metodo_regla_falsa

COLOR_BG = "#1e1e2f"
COLOR_MARCO = "#2b2b40"
COLOR_TEXTO = "#ffffff"
SUBTEXTO_COLOR = "#bbbbbb"
BOTON_COLOR = "#3b82f6"
COLOR_ENTRADA = "#3a3a4f"
COLOR_HEADER = "#1e779a"  # Nuevo color para el encabezado de la tabla

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def safe_eval(expr, x_val):
    """Evalúa f(x) de forma segura."""
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names['x'] = x_val
    try:
        return eval(expr, {"__builtins__": {}}, allowed_names)
    except SyntaxError as e:
        raise ValueError(f"Error de sintaxis en la función: {e}")
    except Exception as e:
        raise ValueError(f"Error en la función: {e}")

class NumericalMethodsCalculator(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_BG)
        self.parent = parent

        self.columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(self, text="Calculadora de Métodos Numéricos Cerrados",
                     text_color=COLOR_TEXTO, font=("Arial", 24, "bold")).pack(pady=(15, 5))

        ctk.CTkLabel(self, text="Selecciona un método, ingresa los datos y obtén la raíz",
                     text_color=SUBTEXTO_COLOR, font=("Arial", 14)).pack(pady=(0, 15))

        # Menú de método
        metodo_frame = ctk.CTkFrame(self, fg_color=COLOR_MARCO, corner_radius=10)
        metodo_frame.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(metodo_frame, text="Método:", text_color=COLOR_TEXTO).pack(side="left", padx=5)
        self.metodo_menu = ctk.CTkOptionMenu(metodo_frame, values=["Bisección", "Regla Falsa"], width=140)
        self.metodo_menu.pack(side="left", padx=5)

        # Entradas
        entradas = ctk.CTkFrame(self, fg_color=COLOR_MARCO, corner_radius=10)
        entradas.pack(pady=10, padx=20, fill="x")
        entradas.columnconfigure((0, 2, 4), weight=0)
        entradas.columnconfigure((1, 3, 5), weight=1)

        ctk.CTkLabel(entradas, text="f(x):", text_color=COLOR_TEXTO).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.fx_entry = ctk.CTkEntry(entradas, placeholder_text="Ej: math.exp(x) - 3*x", fg_color=COLOR_ENTRADA)
        self.fx_entry.grid(row=0, column=1, columnspan=5, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(entradas, text="a:", text_color=COLOR_TEXTO).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.a_entry = ctk.CTkEntry(entradas, placeholder_text="Ej: 1.0", fg_color=COLOR_ENTRADA)
        self.a_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(entradas, text="b:", text_color=COLOR_TEXTO).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.b_entry = ctk.CTkEntry(entradas, placeholder_text="Ej: 2.0", fg_color=COLOR_ENTRADA)
        self.b_entry.grid(row=1, column=3, padx=5, pady=5)

        ctk.CTkLabel(entradas, text="Tolerancia:", text_color=COLOR_TEXTO).grid(row=1, column=4, padx=10, pady=5, sticky="w")
        self.tol_entry = ctk.CTkEntry(entradas, placeholder_text="Ej: 0.0001", fg_color=COLOR_ENTRADA)
        self.tol_entry.grid(row=1, column=5, padx=10, pady=5)

        # Botones
        accion_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        accion_frame.pack(pady=10)
        ctk.CTkButton(accion_frame, text="Ejecutar Método", command=self.ejecutar_metodo,
                      fg_color=BOTON_COLOR).pack(side="left", padx=10)
        ctk.CTkButton(accion_frame, text="Limpiar", command=self.limpiar_todo,
                      fg_color="#ef4444").pack(side="left", padx=10)

        # Resultados
        self.resultados_frame = ctk.CTkScrollableFrame(self, fg_color=COLOR_MARCO, corner_radius=10,
                                                       label_text="📈 Resultado",
                                                       label_text_color=COLOR_TEXTO)
        self.resultados_frame.pack(padx=20, pady=15, fill="both", expand=True)
        self.result_textbox = ctk.CTkTextbox(self.resultados_frame, wrap="word", fg_color=COLOR_ENTRADA, text_color=COLOR_TEXTO)
        self.result_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.result_textbox.insert("0.0", "Ingrese los datos y presione 'Ejecutar Método'.")
        self.result_textbox.configure(state="disabled")  # Solo lectura inicialmente

    def ejecutar_metodo(self):
        metodo = self.metodo_menu.get()
        f_expr = self.fx_entry.get().strip()

        if not f_expr:
            messagebox.showerror("Error", "La función f(x) no puede estar vacía.")
            return

        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tol = float(self.tol_entry.get())
        except ValueError:
            messagebox.showerror("Error", "a, b y tolerancia deben ser números válidos.")
            return

        if a >= b:
            messagebox.showerror("Error", "El límite inferior 'a' debe ser menor que 'b'.")
            return

        try:
            fa = safe_eval(f_expr, a)
            fb = safe_eval(f_expr, b)
        except ValueError as e:
            messagebox.showerror("Error de Función", str(e))
            return

        if fa * fb >= 0:
            messagebox.showerror("Error", "f(a) y f(b) deben tener signos opuestos.")
            return

        # Limpiar resultados anteriores
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")

        # Ejecutar el método seleccionado
        try:
            if metodo == "Bisección":
                # Asumiendo que metodo_biseccion devuelve xr, iter_count, error_rel, historial
                xr, iter_count, error_rel, historial = metodo_biseccion(f_expr, a, b, tol)
            elif metodo == "Regla Falsa":
                xr, iter_count, error_rel, historial = metodo_regla_falsa(f_expr, a, b, tol)
            else:
                messagebox.showerror("Error", "Método no reconocido.")
                return

            # Formatear el resultado
            resultado = f"Método: {metodo}\n"
            resultado += f"Función: f(x) = {f_expr}\n"
            resultado += f"Intervalo: [{a}, {b}]\n"
            resultado += f"Tolerancia: {tol}\n"
            resultado += f"Raíz aproximada: {xr:.6f}\n"
            resultado += f"Iteraciones realizadas: {iter_count}\n"
            resultado += f"Error relativo final: {error_rel:.6f}%\n\n"
            resultado += "Historial de iteraciones:\n"
            resultado += f"{'Iter':<5} {'a':<10} {'b':<10} {'xr':<10} {'f(xr)':<10} {'Error (%)':<12}\n"
            resultado += "-" * 60 + "\n"
            for it in historial:
                resultado += f"{it['iter']:<5} {it['a']:<10.6f} {it['b']:<10.6f} {it['xr']:<10.6f} {it['f_xr']:<10.6f} {it['error']:<12.6f}\n"

            self.result_textbox.insert("0.0", resultado)
            self.result_textbox.configure(state="disabled")

        except Exception as e:
            messagebox.showerror("Error en el Método", f"Ocurrió un error al ejecutar el método: {e}")
            self.result_textbox.insert("0.0", "Error al ejecutar el método. Verifique los datos.")
            self.result_textbox.configure(state="disabled")

    def limpiar_todo(self):
        self.fx_entry.delete(0, tk.END)
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.tol_entry.delete(0, tk.END)
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", "Ingrese los datos y presione 'Ejecutar Método'.")
        self.result_textbox.configure(state="disabled")

def main():
    root = ctk.CTk()
    root.title("Calculadora de Raíces")
    root.geometry("800x700")
    calculator = NumericalMethodsCalculator(root)
    calculator.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
