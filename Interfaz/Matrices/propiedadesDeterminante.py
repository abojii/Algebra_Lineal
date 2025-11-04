import customtkinter as ctk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Models import solverPropiedadesDeterminante as solver

# === COLORES Y ESTILO ===
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PropiedadesDeterminanteApp(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_BG)
        self.parent = parent
        self.entries_a = []
        self.entries_b = []
        self.size_entry = None
        self.propiedad_var = None
        self.setup_ui()

    def setup_ui(self):
        # === TÍTULO PRINCIPAL ===
        titulo = ctk.CTkLabel(
            self,
            text="Propiedades Teóricas del Determinante",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_BUTTON
        )
        titulo.pack(pady=(20, 10))

        subtitulo = ctk.CTkLabel(
            self,
            text="Selecciona una propiedad, genera las matrices y analiza su comportamiento de manera detallada.",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_SUBTEXT
        )
        subtitulo.pack(pady=(0, 20))

        # === FRAME SUPERIOR: Controles ===
        top_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        top_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Sección de tamaño y propiedad
        config_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        config_frame.pack(pady=15, padx=15, fill="x")

        ctk.CTkLabel(config_frame, text="Tamaño de la Matriz (n):", text_color=COLOR_TEXT, font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        self.size_entry = ctk.CTkEntry(config_frame, width=80, placeholder_text="2-10", fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
        self.size_entry.insert(0, "3")
        self.size_entry.grid(row=0, column=1, padx=(0, 20), pady=5)

        ctk.CTkLabel(config_frame, text="Propiedad a Verificar:", text_color=COLOR_TEXT, font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")
        self.propiedad_var = ctk.StringVar(value="Seleccione una propiedad")

        self.propiedad_menu = ctk.CTkOptionMenu(
            config_frame,
            variable=self.propiedad_var,
            values=[
                "1. Fila o columna nula ⇒ det(A)=0",
                "2. Filas o columnas iguales/proporcionales ⇒ det(A)=0",
                "3. Intercambio de filas ⇒ cambia signo",
                "4. Multiplicación de fila por escalar ⇒ det(kA)=k·det(A)",
                "5. Propiedad multiplicativa ⇒ det(AB)=det(A)·det(B)",
                "6. Suma de múltiplo de una fila a otra ⇒ det(A) no cambia"
            ],
            fg_color=COLOR_BUTTON,
            button_color=COLOR_FRAME,
            text_color="white",
            width=400
        )
        self.propiedad_menu.grid(row=1, column=1, padx=(0, 20), pady=5)

        # Sección de botones
        button_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        button_frame.pack(pady=(0, 15), padx=15, fill="x")

        self.generate_btn = ctk.CTkButton(
            button_frame, text="Generar Matrices", command=self.generar_campos, fg_color=COLOR_BUTTON, font=ctk.CTkFont(weight="bold")
        )
        self.generate_btn.pack(side="left", padx=(0, 10))

        self.verify_btn = ctk.CTkButton(
            button_frame, text="Verificar Propiedad", command=self.verificar_propiedad, fg_color="#22c55e", state="disabled", font=ctk.CTkFont(weight="bold")
        )
        self.verify_btn.pack(side="left", padx=(0, 10))

        self.clear_btn = ctk.CTkButton(
            button_frame, text="Limpiar Todo", command=self.limpiar_todo, fg_color="#f97316", font=ctk.CTkFont(weight="bold")
        )
        self.clear_btn.pack(side="left")

        # === FRAME DE MATRICES ===
        self.matrix_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        self.matrix_frame.pack(padx=20, pady=(0, 15), fill="both", expand=True)

        # === FRAME DE RESULTADOS ===
        result_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME, corner_radius=10)
        result_frame.pack(padx=20, pady=(0, 20), fill="x")

        ctk.CTkLabel(result_frame, text="Resultado de la Verificación:", text_color=COLOR_TEXT, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        self.result_box = ctk.CTkTextbox(
            result_frame,
            wrap="word",
            fg_color=COLOR_ENTRY,
            text_color=COLOR_TEXT,
            font=ctk.CTkFont(size=11),
            height=300
        )
        self.result_box.pack(fill="x", padx=15, pady=(0, 15))
        self.result_box.insert("1.0", "Selecciona una propiedad y genera las matrices para comenzar la verificación.\n")

    def generar_campos(self):
        """Genera campos de entrada para matriz A (y B si es propiedad 5)."""
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.entries_a.clear()
        self.entries_b.clear()

        try:
            n = int(self.size_entry.get().strip())
            if n < 2 or n > 10:
                messagebox.showerror("Error", "El tamaño debe estar entre 2 y 10.")
                return
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número entero válido entre 2 y 10.")
            return

        propiedad = self.propiedad_var.get()
        if propiedad == "Seleccione una propiedad":
            messagebox.showerror("Error", "Selecciona una propiedad primero.")
            return

        # Siempre generar A
        frameA = ctk.CTkFrame(self.matrix_frame, fg_color=COLOR_BG, corner_radius=5)
        frameA.pack(side="left", expand=True, padx=10, pady=10)
        ctk.CTkLabel(frameA, text="Matriz A", text_color=COLOR_SUBTEXT, font=ctk.CTkFont(weight="bold")).pack(pady=(5, 10))
        gridA = ctk.CTkFrame(frameA, fg_color="transparent")
        gridA.pack(pady=5)
        for i in range(n):
            row_entries = []
            for j in range(n):
                e = ctk.CTkEntry(gridA, width=60, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
                e.grid(row=i, column=j, padx=3, pady=3)
                row_entries.append(e)
            self.entries_a.append(row_entries)

        # Generar B solo para propiedad 5
        if propiedad.startswith("5."):
            frameB = ctk.CTkFrame(self.matrix_frame, fg_color=COLOR_BG, corner_radius=5)
            frameB.pack(side="left", expand=True, padx=10, pady=10)
            ctk.CTkLabel(frameB, text="Matriz B", text_color=COLOR_SUBTEXT, font=ctk.CTkFont(weight="bold")).pack(pady=(5, 10))
            gridB = ctk.CTkFrame(frameB, fg_color="transparent")
            gridB.pack(pady=5)
            for i in range(n):
                row_entries = []
                for j in range(n):
                    e = ctk.CTkEntry(gridB, width=60, fg_color=COLOR_ENTRY, text_color=COLOR_TEXT)
                    e.grid(row=i, column=j, padx=3, pady=3)
                    row_entries.append(e)
                self.entries_b.append(row_entries)

        # Mensaje inicial y habilitar verificación
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", f"Matrices generadas para tamaño {n}x{n}.\n")
        if propiedad.startswith("5."):
            self.result_box.insert("end", "Ingresa valores en A y B para verificar la propiedad multiplicativa.\n")
        else:
            self.result_box.insert("end", "Ingresa valores en A y presiona 'Verificar Propiedad'.\n")
        self.verify_btn.configure(state="normal")

    def verificar_propiedad(self):
        """Verifica la propiedad seleccionada y muestra resultado en el TextBox."""
        propiedad = self.propiedad_var.get()
        self.result_box.delete("1.0", "end")

        if not self.entries_a:
            self.result_box.insert("1.0", "Genera las matrices primero.\n")
            return

        try:
            A = [[float(entry.get()) for entry in fila] for fila in self.entries_a]
        except ValueError:
            self.result_box.insert("1.0", "Asegúrate de ingresar valores numéricos en la matriz A.\n")
            return

        valido = None
        pasos = ""

        if propiedad.startswith("1."):
            valido, pasos = solver.es_cero_fila_o_columna(A)
        elif propiedad.startswith("2."):
            valido, pasos = solver.son_iguales_o_proporcionales(A)
        elif propiedad.startswith("3."):
            A_copia = [fila[:] for fila in A]
            A_copia[0], A_copia[1] = A_copia[1], A_copia[0]
            valido, pasos = solver.intercambio_signo(A, A_copia)
        elif propiedad.startswith("4."):
            k = self.pedir_escalar("Ingresa el escalar k para multiplicar la matriz:")
            if k is not None:
                valido, pasos = solver.multiplicacion_escalar(A, k)
        elif propiedad.startswith("5."):
            if not self.entries_b:
                self.result_box.insert("1.0", "Genera las matrices primero.\n")
                return
            try:
                B = [[float(entry.get()) for entry in fila] for fila in self.entries_b]
                valido, pasos = solver.propiedad_multiplicativa(A, B, solver.determinante_cofactores)
            except ValueError:
                self.result_box.insert("1.0", "Asegúrate de ingresar valores numéricos en la matriz B.\n")
                return
        elif propiedad.startswith("6."):
            k = self.pedir_escalar("Ingresa el escalar k para sumar múltiplo:")
            fila_origen = self.pedir_fila("Fila origen (1-n):", len(A))
            fila_destino = self.pedir_fila("Fila destino (1-n):", len(A))
            if k is not None and fila_origen is not None and fila_destino is not None:
                valido, pasos = solver.suma_multiplo_fila(A, k, fila_origen-1, fila_destino-1)
        else:
            pasos = "Selecciona una propiedad válida."

        self.result_box.insert("1.0", f"Propiedad Seleccionada: {propiedad}\n\n")
        self.result_box.insert("end", pasos)
        if valido is not None:
            self.result_box.insert("end", f"\nResultado: {'Propiedad Verificada' if valido else 'Propiedad No Verificada'}")

    def pedir_escalar(self, prompt):
        """Pide un escalar al usuario."""
        dialog = ctk.CTkInputDialog(text=prompt, title="Entrada de Escalar")
        value = dialog.get_input()
        if value is None:
            return None
        try:
            return float(value)
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido.")
            return None

    def pedir_fila(self, prompt, n):
        """Pide una fila."""
        dialog = ctk.CTkInputDialog(text=prompt, title="Entrada de Fila")
        value = dialog.get_input()
        if value is None:
            return None
        try:
            fila = int(value)
            if 1 <= fila <= n:
                return fila
            else:
                messagebox.showerror("Error", f"La fila debe estar entre 1 y {n}.")
                return None
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número entero válido.")
            return None

    def limpiar_campos(self):
        """Limpia las matrices."""
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.entries_a = []
        self.entries_b = []
        self.verify_btn.configure(state="disabled")

    def limpiar_todo(self):
        """Limpia todo."""
        self.limpiar_campos()
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", "Interfaz reiniciada. Selecciona una propiedad y genera las matrices nuevamente.\n")
        self.propiedad_var.set("Seleccione una propiedad")
