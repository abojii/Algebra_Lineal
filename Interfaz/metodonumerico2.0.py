import customtkinter as ctk
from tkinter import messagebox
import math
import tkinter as tk  
COLOR_BG = "#1e1e2f"
COLOR_MARCO = "#2b2b40"
COLOR_TEXTO = "#ffffff"
SUBTEXTO_COLOR = "#bbbbbb"
BOTON_COLOR = "#3b82f6"
COLOR_ENTRADA = "#3a3a4f"
COLOR_HEADER = "#1e779a" # Nuevo color para el encabezado de la tabla

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def safe_eval(expr, x_val):
    """
    Función segura para evaluar f(x) usando eval con contexto limitado (solo funciones math).
    """
    # Exponer las funciones del módulo math (sin métodos internos __*)
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names['x'] = x_val
    try:
        # Evalúa la expresión solo con el contexto permitido
        return eval(expr, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        # Lanza un error de valor si la expresión es inválida o tiene una función no permitida
        raise ValueError(f"Error en la evaluación de la función: {e}")

class NumericalMethodsCalculator(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_BG)
        self.parent = parent

        # Configuración de la cuadrícula
        self.columnconfigure(0, weight=1)
        
        # ======= TÍTULO =======
        titulo_label = ctk.CTkLabel(
            self,
            text="Calculadora de Métodos Numéricos Cerrados",
            text_color=COLOR_TEXTO,
            font=("Arial", 24, "bold")
        )
        titulo_label.pack(pady=(15, 10))

        subtitulo_label = ctk.CTkLabel(
            self,
            text="Selecciona un método, ingresa los parámetros y obtén el proceso de iteración",
            text_color=SUBTEXTO_COLOR,
            font=("Arial", 14)
        )
        subtitulo_label.pack(pady=(0, 20))

        # ======= SECCIÓN DE MÉTODO =======
        metodo_frame = ctk.CTkFrame(self, fg_color=COLOR_MARCO, corner_radius=10)
        metodo_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(metodo_frame, text="Método:", text_color=COLOR_TEXTO).pack(side="left", padx=5)
        self.metodo_menu = ctk.CTkOptionMenu(metodo_frame, values=["Bisección", "Regla Falsa"], width=120, height=32, font=("Arial", 12))
        self.metodo_menu.pack(side="left", padx=5)

        # ======= ENTRADAS =======
        entradas_frame = ctk.CTkFrame(self, fg_color=COLOR_MARCO, corner_radius=10)
        entradas_frame.pack(pady=10, padx=20, fill="x")
        
        # Grid para alinear mejor las entradas
        entradas_frame.columnconfigure((0, 2, 4), weight=0) # Etiquetas (fijas)
        entradas_frame.columnconfigure((1, 3, 5), weight=1) # Entradas (expansibles)

        # Fila 1: f(x)
        ctk.CTkLabel(entradas_frame, text="f(x):", text_color=COLOR_TEXTO).grid(row=0, column=0, padx=(15, 5), pady=5, sticky="w")
        self.fx_entry = ctk.CTkEntry(entradas_frame, height=32, fg_color=COLOR_ENTRADA, text_color=COLOR_TEXTO, placeholder_text="Ej: math.exp(x) - 3*x")
        self.fx_entry.grid(row=0, column=1, columnspan=5, padx=(0, 15), pady=5, sticky="ew")

        # Fila 2: a, b, Tolerancia
        ctk.CTkLabel(entradas_frame, text="a:", text_color=COLOR_TEXTO).grid(row=1, column=0, padx=(15, 5), pady=5, sticky="w")
        self.a_entry = ctk.CTkEntry(entradas_frame, width=100, height=32, fg_color=COLOR_ENTRADA, text_color=COLOR_TEXTO, placeholder_text="Ej: 1.0")
        self.a_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(entradas_frame, text="b:", text_color=COLOR_TEXTO).grid(row=1, column=2, padx=(15, 5), pady=5, sticky="w")
        self.b_entry = ctk.CTkEntry(entradas_frame, width=100, height=32, fg_color=COLOR_ENTRADA, text_color=COLOR_TEXTO, placeholder_text="Ej: 2.0")
        self.b_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(entradas_frame, text="Tolerancia (Error Deseado):", text_color=COLOR_TEXTO).grid(row=1, column=4, padx=(15, 5), pady=5, sticky="w")
        self.tol_entry = ctk.CTkEntry(entradas_frame, width=100, height=32, fg_color=COLOR_ENTRADA, text_color=COLOR_TEXTO, placeholder_text="Ej: 0.0001")
        self.tol_entry.grid(row=1, column=5, padx=(0, 15), pady=5, sticky="ew")


        # ======= BOTONES DE ACCIÓN =======
        accion_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        accion_frame.pack(pady=10)

        self.ejecutar_button = ctk.CTkButton(accion_frame, text="Ejecutar Método", command=self.ejecutar_metodo, width=150, height=32, fg_color=BOTON_COLOR)
        self.ejecutar_button.pack(side="left", padx=10)

        self.limpiar_button = ctk.CTkButton(accion_frame, text="Limpiar", command=self.limpiar_todo, width=90, height=32, fg_color="#ef4444")
        self.limpiar_button.pack(side="left", padx=10)

        # ======= RESULTADOS =======
        self.resultados_frame = ctk.CTkScrollableFrame(self, fg_color=COLOR_MARCO, corner_radius=10, label_text="📈 Proceso de Iteraciones y Resultado Final", label_text_color=COLOR_TEXTO)
        self.resultados_frame.pack(padx=20, pady=15, fill="both", expand=True)
        self.resultados_frame.columnconfigure(0, weight=1) # Permite centrar los contenidos
        self.summary_label = ctk.CTkLabel(self.resultados_frame, text="Ingrese los datos y presione 'Ejecutar Método'.", text_color=SUBTEXTO_COLOR, font=("Arial", 14))
        self.summary_label.grid(row=0, column=0, pady=20, padx=20)


    # ======= 2. LÓGICA NUMÉRICA Y VISUALIZACIÓN =======
    
    def calcular_error_relativo(self, xr, xr_prev):
        """Calcula el error relativo porcentual."""
        if xr_prev is None or xr == 0:
            return float('inf')
        return abs((xr - xr_prev) / xr) * 100

    def ejecutar_metodo(self):
        """Valida entradas y lanza el método seleccionado."""
        metodo = self.metodo_menu.get()
        f_expr = self.fx_entry.get().strip()
        
        # 1. Validación de entradas
        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tol = float(self.tol_entry.get())
        except ValueError:
            messagebox.showerror("Error de Entrada", "El intervalo (a, b) y la Tolerancia deben ser números válidos.")
            return

        if not f_expr:
            messagebox.showerror("Error de Entrada", "Ingresa la función f(x).")
            return
            
        if a >= b:
             messagebox.showerror("Error de Validación", "El límite inferior 'a' debe ser menor que el superior 'b'.")
             return

        # Limpiar resultados anteriores
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        
        # 2. Ejecutar el método
        if metodo == "Bisección":
            self.biseccion(f_expr, a, b, tol)
        elif metodo == "Regla Falsa":
            self.regla_falsa(f_expr, a, b, tol)

    # ======= MÉTODO DE BISECCIÓN =======
    def biseccion(self, f_expr, a_inicial, b_inicial, tol, max_iter=100):
        a, b = a_inicial, b_inicial
        
        try:
            fa = safe_eval(f_expr, a)
            fb = safe_eval(f_expr, b)
        except ValueError as e:
            messagebox.showerror("Error de Función", str(e))
            return

        # 3. Verificar condición f(a) * f(b) < 0 [cite: 13]
        if fa * fb >= 0:
            messagebox.showerror("Error de Algoritmo", "El intervalo no es válido. f(a) * f(b) debe ser < 0.")
            self.summary_label = ctk.CTkLabel(self.resultados_frame, text="❌ El intervalo no es válido.", text_color="#ef4444", font=("Arial", 14, "bold"))
            self.summary_label.grid(row=0, column=0, pady=20)
            return

        iter_count = 0
        xr_prev = None
        error_rel = float('inf')

        # 4. Configurar la tabla
        ctk.CTkLabel(self.resultados_frame, text="Iteraciones - Método de Bisección", text_color=COLOR_TEXTO, font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)
        iter_frame = ctk.CTkFrame(self.resultados_frame, fg_color=COLOR_ENTRADA)
        iter_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        headers = ["Iter", "a", "b", "xr (Punto Medio)", "f(xr)", "Error Rel (%)", "Nuevo Intervalo"]
        
        for i, header in enumerate(headers):
            lbl = ctk.CTkLabel(iter_frame, text=header, text_color=COLOR_TEXTO, font=("Arial", 12, "bold"))
            lbl.grid(row=0, column=i, padx=5, pady=2, sticky="ew")
            iter_frame.grid_columnconfigure(i, weight=1)

        row = 1
        while error_rel > tol and iter_count < max_iter:
            iter_count += 1
            a_prev, b_prev = a, b # Guardar el intervalo inicial de la iteración
            
            # Cálculo del punto medio
            xr = (a + b) / 2
            fxr = safe_eval(f_expr, xr)

            # Cálculo del error
            error_rel = self.calcular_error_relativo(xr, xr_prev)

            # Actualización del intervalo [cite: 17]
            if fa * fxr < 0:
                b = xr
                # No es necesario actualizar fb en bisección
            else:
                a = xr
                fa = fxr # Actualizar f(a) para la siguiente comprobación
            
            nuevo_intervalo_str = f"[{a:.8f}, {b:.8f}]" # El intervalo DESPUÉS de la actualización

            # Mostrar fila con mayor precisión para los valores (Requerimiento 65)
            error_str = f"{error_rel:.8f}" if error_rel != float('inf') else "N/A"
            values = [iter_count, f"{a_prev:.8f}", f"{b_prev:.8f}", f"{xr:.8f}", f"{fxr:.8f}", error_str, nuevo_intervalo_str]
            
            for i, val in enumerate(values):
                bg_color = COLOR_FRAME if row % 2 == 0 else COLOR_ENTRADA
                ctk.CTkLabel(iter_frame, text=val, text_color=COLOR_TEXTO, font=("Courier New", 11), fg_color=bg_color).grid(row=row, column=i, padx=2, pady=1, sticky="ew")
            
            row += 1
            xr_prev = xr # Actualizar para el siguiente cálculo de error

        # 5. Resultados finales [cite: 49]
        resultado_text = (
            f"Raíz aproximada: {xr:.10f}\n" # Raíz aproximada [cite: 50]
            f"Iteraciones totales: {iter_count}\n" # Iteraciones totales [cite: 51]
            f"Error relativo final: {error_rel:.8f}%\n" # Error relativo final [cite: 52]
            f"Intervalo donde se encierra la raíz: [{a:.10f}, {b:.10f}]" # Intervalo final [cite: 53]
        )
        ctk.CTkLabel(self.resultados_frame, text="Resultado Final:", text_color=COLOR_TEXTO, font=("Arial", 16, "bold")).grid(row=row, column=0, pady=10, sticky="w")
        ctk.CTkLabel(self.resultados_frame, text=resultado_text, text_color="#22c55e", font=("Arial", 12)).grid(row=row + 1, column=0, pady=5, padx=10, sticky="w")


    # ======= MÉTODO DE REGLA FALSA =======
    def regla_falsa(self, f_expr, a_inicial, b_inicial, tol, max_iter=100):
        a, b = a_inicial, b_inicial
        
        try:
            fa = safe_eval(f_expr, a)
            fb = safe_eval(f_expr, b)
        except ValueError as e:
            messagebox.showerror("Error de Función", str(e))
            return

        # 3. Verificar condición f(a) * f(b) < 0 [cite: 13]
        if fa * fb >= 0:
            messagebox.showerror("Error de Algoritmo", "El intervalo no es válido. f(a) * f(b) debe ser < 0.")
            self.summary_label = ctk.CTkLabel(self.resultados_frame, text="El intervalo no es válido.", text_color="#ef4444", font=("Arial", 14, "bold"))
            self.summary_label.grid(row=0, column=0, pady=20)
            return

        iter_count = 0
        xr_prev = None
        error_rel = float('inf')

        # 4. Configurar la tabla
        ctk.CTkLabel(self.resultados_frame, text="Iteraciones - Método de Regla Falsa", text_color=COLOR_TEXTO, font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)
        iter_frame = ctk.CTkFrame(self.resultados_frame, fg_color=COLOR_ENTRADA)
        iter_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        headers = ["Iter", "a", "b", "xr (Intersección)", "f(xr)", "Error Rel (%)", "Nuevo Intervalo"]
        
        for i, header in enumerate(headers):
            lbl = ctk.CTkLabel(iter_frame, text=header, text_color=COLOR_TEXTO, font=("Arial", 12, "bold"))
            lbl.grid(row=0, column=i, padx=5, pady=2, sticky="ew")
            iter_frame.grid_columnconfigure(i, weight=1)

        row = 1
        while error_rel > tol and iter_count < max_iter:
            iter_count += 1
            a_prev, b_prev = a, b # Guardar el intervalo inicial de la iteración
            
            # Cálculo del punto de Regla Falsa
            xr = b - (fb * (b - a)) / (fb - fa)
            fxr = safe_eval(f_expr, xr)

            # Cálculo del error
            error_rel = self.calcular_error_relativo(xr, xr_prev)

            # Actualización del intervalo [cite: 17]
            if fa * fxr < 0:
                b = xr
                fb = fxr # Actualizar f(b)
            else:
                a = xr
                fa = fxr # Actualizar f(a)
            
            nuevo_intervalo_str = f"[{a:.8f}, {b:.8f}]" # El intervalo DESPUÉS de la actualización

            # Mostrar fila con mayor precisión (Requerimiento 65)
            error_str = f"{error_rel:.8f}" if error_rel != float('inf') else "N/A"
            values = [iter_count, f"{a_prev:.8f}", f"{b_prev:.8f}", f"{xr:.8f}", f"{fxr:.8f}", error_str, nuevo_intervalo_str]
            
            for i, val in enumerate(values):
                bg_color = COLOR_FRAME if row % 2 == 0 else COLOR_ENTRADA
                # Usamos fuente monoespaciada ("Courier New") para que los números decimales se alineen mejor
                ctk.CTkLabel(iter_frame, text=val, text_color=COLOR_TEXTO, font=("Courier New", 11), fg_color=bg_color).grid(row=row, column=i, padx=2, pady=1, sticky="ew")
            
            row += 1
            xr_prev = xr # Actualizar para el siguiente cálculo de error

        # 5. Resultados finales [cite: 49]
        resultado_text = (
            f"Raíz aproximada: {xr:.10f}\n" # Raíz aproximada [cite: 50]
            f"Iteraciones totales: {iter_count}\n" # Iteraciones totales [cite: 51]
            f"Error relativo final: {error_rel:.8f}%\n" # Error relativo final [cite: 52]
            f"Intervalo donde se encierra la raíz: [{a:.10f}, {b:.10f}]" # Intervalo final [cite: 53]
        )
        ctk.CTkLabel(self.resultados_frame, text="Resultado Final:", text_color=COLOR_TEXTO, font=("Arial", 16, "bold")).grid(row=row, column=0, pady=10, sticky="w")
        ctk.CTkLabel(self.resultados_frame, text=resultado_text, text_color="#22c55e", font=("Arial", 12)).grid(row=row + 1, column=0, pady=5, padx=10, sticky="w")

    # ======= LIMPIAR =======
    def limpiar_todo(self):
        """Limpia las entradas y los resultados."""
        self.fx_entry.delete(0, tk.END)
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.tol_entry.delete(0, tk.END)
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        
        self.summary_label = ctk.CTkLabel(self.resultados_frame, text="Ingrese los datos y presione 'Ejecutar Método'.", text_color=SUBTEXTO_COLOR, font=("Arial", 14))
        self.summary_label.grid(row=0, column=0, pady=20, padx=20)


# Función principal de inicio
def main():
    root = ctk.CTk()
    root.title("Calculadora de Raíces (Programa 9)")
    root.geometry("900x750")

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    calculator = NumericalMethodsCalculator(root)
    calculator.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()