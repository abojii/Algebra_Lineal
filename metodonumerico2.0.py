import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox, ttk, Scrollbar
import math
import tkinter as tk

from Models.biseccion import metodo_biseccion
from Models.regla_falsa import metodo_regla_falsa

COLOR_BG = "#1e1e2f"
COLOR_MARCO = "#2b2b40"
COLOR_TEXTO = "#ffffff"
SUBTEXTO_COLOR = "#bbbbbb"
BOTON_COLOR = "#3b82f6"
COLOR_ENTRADA = "#3a3a4f"
COLOR_HEADER = "#1e779a"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def safe_eval(expr: str, x_val: float) -> float:
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names["x"] = x_val
    return eval(expr, {"__builtins__": {}}, allowed_names)


class NumericalMethodsCalculator(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_BG)
        self.parent = parent
        self.historial = []

        self.columnconfigure(0, weight=1)

        # ---------------- TITULO ----------------
        ctk.CTkLabel(
            self,
            text="Calculadora de Métodos Numéricos Cerrados",
            text_color=COLOR_TEXTO,
            font=("Arial", 24, "bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            self,
            text="Selecciona un método, ingresa los datos y obtén la raíz",
            text_color=SUBTEXTO_COLOR,
            font=("Arial", 14)
        ).pack(pady=(0, 15))

        # ---------------- MÉTODO ----------------
        metodo_frame = ctk.CTkFrame(self, fg_color=COLOR_MARCO, corner_radius=10)
        metodo_frame.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(metodo_frame, text="Método:", text_color=COLOR_TEXTO)\
            .pack(side="left", padx=5)

        self.metodo_menu = ctk.CTkOptionMenu(
            metodo_frame,
            values=["Bisección", "Regla Falsa"],
            width=140
        )
        self.metodo_menu.pack(side="left", padx=5)

        # ---------------- ENTRADAS ----------------
        entradas = ctk.CTkFrame(self, fg_color=COLOR_MARCO, corner_radius=10)
        entradas.pack(pady=10, padx=20, fill="x")
        entradas.columnconfigure((0, 2, 4), weight=0)
        entradas.columnconfigure((1, 3, 5), weight=1)

        ctk.CTkLabel(entradas, text="f(x):", text_color=COLOR_TEXTO)\
            .grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.fx_entry = ctk.CTkEntry(
            entradas,
            placeholder_text="Ej: x**3 - 4*x - 1  (usa ** para potencias)",
            fg_color=COLOR_ENTRADA
        )
        self.fx_entry.grid(row=0, column=1, columnspan=5, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(entradas, text="a:", text_color=COLOR_TEXTO)\
            .grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.a_entry = ctk.CTkEntry(entradas, placeholder_text="Ej: 1.0", fg_color=COLOR_ENTRADA)
        self.a_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(entradas, text="b:", text_color=COLOR_TEXTO)\
            .grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.b_entry = ctk.CTkEntry(entradas, placeholder_text="Ej: 2.0", fg_color=COLOR_ENTRADA)
        self.b_entry.grid(row=1, column=3, padx=5, pady=5)

        ctk.CTkLabel(entradas, text="Tolerancia:", text_color=COLOR_TEXTO)\
            .grid(row=1, column=4, padx=10, pady=5, sticky="w")
        self.tol_entry = ctk.CTkEntry(entradas, placeholder_text="Ej: 0.0001", fg_color=COLOR_ENTRADA)
        self.tol_entry.grid(row=1, column=5, padx=10, pady=5)

        # ---------------- BOTONES ----------------
        accion_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        accion_frame.pack(pady=10)

        ctk.CTkButton(
            accion_frame, text="Ejecutar Método",
            command=self.ejecutar_metodo, fg_color=BOTON_COLOR
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            accion_frame, text="Limpiar",
            command=self.limpiar_todo, fg_color="#ef4444"
        ).pack(side="left", padx=10)

        # ---------------- RESULTADOS ----------------
        self.resultados_frame = ctk.CTkScrollableFrame(
            self, fg_color=COLOR_MARCO, corner_radius=10,
            label_text_color=COLOR_TEXTO
        )
        self.resultados_frame.pack(padx=20, pady=15, fill="both", expand=True)

        # Cuadro de procedimiento paso a paso
        self.procedimiento_frame = ctk.CTkScrollableFrame(
            self.resultados_frame, fg_color=COLOR_ENTRADA,
            corner_radius=5, height=140
        )
        self.procedimiento_frame.pack(fill="x", padx=10, pady=(5, 10))
        self.procedimiento_frame.pack_propagate(False)

        self.info_textbox = ctk.CTkTextbox(
            self.procedimiento_frame, wrap="word",
            fg_color=COLOR_ENTRADA, text_color=COLOR_TEXTO,
            font=("Arial", 12)
        )
        self.info_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.info_textbox.insert("0.0", "Ingrese los datos y presione 'Ejecutar Método'.")
        self.info_textbox.configure(state="disabled")

        # Tabla + botón expandir
        tabla_frame = ctk.CTkFrame(self.resultados_frame, fg_color=COLOR_MARCO)
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ctk.CTkButton(
            tabla_frame, text="Expandir Tabla",
            command=self.expandir_tabla, fg_color=BOTON_COLOR, width=120
        ).pack(pady=(5, 10))

        columnas = ("Iter", "xl", "xu", "xr", "Ea", "vl", "vu", "vr")
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor="center")

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview", background=COLOR_ENTRADA, foreground=COLOR_TEXTO,
            fieldbackground=COLOR_ENTRADA, borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background=COLOR_HEADER, foreground=COLOR_TEXTO,
            font=("Arial", 10, "bold")
        )
        style.map("Treeview", background=[("selected", BOTON_COLOR)])

        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # -------- MODAL TABLA COMPLETA --------
    def expandir_tabla(self):
        if not self.historial:
            messagebox.showerror("Error", "No hay datos para expandir. Ejecute un método primero.")
            return

        modal = ctk.CTkToplevel(self)
        modal.title("Tabla Expandida de Iteraciones")
        modal.geometry("1200x800")
        modal.transient(self.parent)
        modal.grab_set()

        frame = ctk.CTkFrame(modal, fg_color=COLOR_MARCO)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        columnas = ("Iter", "xl", "xu", "xr", "Ea", "vl", "vu", "vr")
        tree_modal = ttk.Treeview(frame, columns=columnas, show="headings", height=20)

        for col in columnas:
            tree_modal.heading(col, text=col)
            tree_modal.column(col, width=120, anchor="center")

        style_modal = ttk.Style()
        style_modal.configure(
            "Treeview", background=COLOR_ENTRADA, foreground=COLOR_TEXTO,
            fieldbackground=COLOR_ENTRADA, font=("Arial", 12), borderwidth=0
        )
        style_modal.configure(
            "Treeview.Heading",
            background=COLOR_HEADER, foreground=COLOR_TEXTO,
            font=("Arial", 12, "bold")
        )
        style_modal.map("Treeview", background=[("selected", BOTON_COLOR)])

        v_scroll = Scrollbar(frame, orient="vertical", command=tree_modal.yview)
        h_scroll = Scrollbar(frame, orient="horizontal", command=tree_modal.xview)
        tree_modal.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        tree_modal.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

        for it in self.historial:
            tree_modal.insert(
                "", "end",
                values=(it["iter"], it["xl"], it["xu"], it["xr"],
                        it["Ea"], it["vl"], it["vu"], it["vr"])
            )

        ctk.CTkButton(frame, text="Cerrar", command=modal.destroy, fg_color="#ef4444")\
            .pack(pady=10)

    # -------- EJECUTAR MÉTODO --------
    def ejecutar_metodo(self):
        metodo = self.metodo_menu.get()
        f_expr = self.fx_entry.get().strip().replace("^", "**")

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

        # Verificar signos de f(a) y f(b)
        try:
            fa = safe_eval(f_expr, a)
            fb = safe_eval(f_expr, b)
        except Exception as e:
            messagebox.showerror("Error de Función", f"{e}")
            return

        if fa * fb >= 0:
            messagebox.showerror("Error", "f(a) y f(b) deben tener signos opuestos.")
            return

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Limpiar cuadro de texto arriba
        self.info_textbox.configure(state="normal")
        self.info_textbox.delete("1.0", "end")   # <-- usa 1.0 por si acaso
        self.info_textbox.insert("end", "Calculando, un momento...\n\n")
        self.info_textbox.configure(state="disabled")
        self.historial = []

        try:
            # Ejecutar método y obtener paso a paso
            if metodo == "Bisección":
                xr, iter_count, error_rel, historial, paso_a_paso_str = metodo_biseccion(
                    f_expr, a, b, tol
                )
            elif metodo == "Regla Falsa":
                xr, iter_count, error_rel, historial, paso_a_paso_str = metodo_regla_falsa(
                    f_expr, a, b, tol
                )
            else:
                messagebox.showerror("Error", "Método no reconocido.")
                return

            self.historial = historial
#POR AQUI ANDA EL MADAFOKER ERROR MIERDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            # Construir el texto que irá ARRIBA
            info = (
                f"Método: {metodo} | f(x) = {f_expr}\n"
                f"Intervalo inicial: [{a}, {b}] | Tolerancia: {tol}\n"
                f"Raíz aproximada: {xr:.6f} | Iteraciones: {iter_count} | "
                f"Error relativo final: {error_rel:.6f}%\n\n"
                "Procedimiento paso a paso detallado:\n\n"
                f"{paso_a_paso_str if paso_a_paso_str else '(No se generó detalle de iteraciones)'}"
            )

            # AHORA SÍ escribir el procedimiento arriba
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("1.0", "end")
            self.info_textbox.insert("end", info)
            self.info_textbox.see("1.0")   # ir al inicio del texto
            self.info_textbox.configure(state="disabled")

            # Llenar tabla con historial
            for it in historial:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        it["iter"],
                        it["xl"],
                        it["xu"],
                        it["xr"],
                        it["Ea"],
                        it["vl"],
                        it["vu"],
                        it["vr"],
                    ),
                )

        except Exception as e:
            messagebox.showerror("Error en el Método", f"Ocurrió un error al ejecutar el método: {e}")
            self.info_textbox.configure(state="normal")
            self.info_textbox.delete("1.0", "end")
            self.info_textbox.insert("end", "Error al ejecutar el método. Verifique los datos.")
            self.info_textbox.configure(state="disabled")

    # -------- LIMPIAR --------
    def limpiar_todo(self):
        self.fx_entry.delete(0, tk.END)
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.tol_entry.delete(0, tk.END)

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.info_textbox.configure(state="normal")
        self.info_textbox.delete("0.0", "end")
        self.info_textbox.insert("0.0", "Ingrese los datos y presione 'Ejecutar Método'.")
        self.info_textbox.configure(state="disabled")
        self.historial = []


def main():
    root = ctk.CTk()
    root.title("Calculadora de Raíces")
    root.geometry("900x700")
    app = NumericalMethodsCalculator(root)
    app.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
