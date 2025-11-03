import customtkinter as ctk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from Models import solverPropDeterminantes as solver


# === COLORES Y ESTILO ===
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class PropiedadesDeterminanteApp(ctk.CTkFrame):
    """Interfaz interactiva para seleccionar y explorar propiedades del determinante."""

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
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXT
        )
        titulo.pack(pady=20)

        subtitulo = ctk.CTkLabel(
            self,
            text="Selecciona una propiedad, genera las matrices y analiza su comportamiento.",
            font=ctk.CTkFont(size=11),
            text_color=COLOR_SUBTEXT
        )
        subtitulo.pack(pady=(0, 15))

        # === FRAME SUPERIOR ===
        top_frame = ctk.CTkFrame(self, fg_color=COLOR_FRAME)
        top_frame.pack(fill="x", padx=20, pady=10)

        # Campo tamaño matriz
        ctk.CTkLabel(top_frame, text="Tamaño (n):", text_color=COLOR_TEXT).grid(row=0, column=0, padx=10, pady=10)
        self.size_entry = ctk.CTkEntry(top_frame, width=60, placeholder_text="n", fg_color=COLOR_ENTRY)
        self.size_entry.insert(0, "3")
        self.size_entry.grid(row=0, column=1, padx=5, pady=10)

        # Selección de propiedad
        ctk.CTkLabel(top_frame, text="Propiedad:", text_color=COLOR_TEXT).grid(row=0, column=2, padx=10, pady=10)
        self.propiedad_var = ctk.StringVar(value="Seleccione una propiedad")

        self.propiedad_menu = ctk.CTkOptionMenu(
            top_frame,
            variable=self.propiedad_var,
            values=[
                "1️⃣ Fila o columna nula ⇒ det(A)=0",
                "2️⃣ Filas o columnas iguales/proporcionales ⇒ det(A)=0",
                "3️⃣ Intercambio de filas ⇒ cambia signo",
                "4️⃣ Multiplicación de fila por escalar ⇒ det(kA)=k·det(A)",
                "5️⃣ Propiedad multiplicativa ⇒ det(AB)=det(A)·det(B)",
                "6️⃣ Suma de múltiplo de una fila a otra ⇒ det(A) no cambia"
            ],
            fg_color=COLOR_BUTTON,
            button_color=COLOR_FRAME,
            text_color="white",
            width=350
        )
        self.propiedad_menu.grid(row=0, column=3, padx=10, pady=10)

        # Botones de acción
        self.generate_btn = ctk.CTkButton(
            top_frame, text="Generar Campos", command=self.generar_campos, fg_color=COLOR_BUTTON
        )
        self.generate_btn.grid(row=0, column=4, padx=10)

        self.verify_btn = ctk.CTkButton(
            top_frame, text="Verificar Propiedad", command=self.verificar_propiedad, fg_color="#22c55e"
        )
        self.verify_btn.grid(row=0, column=5, padx=10)

        self.clear_btn = ctk.CTkButton(
            top_frame, text="Limpiar", command=self.limpiar_todo, fg_color="#f97316"
        )
        self.clear_btn.grid(row=0, column=6, padx=10)

        # === MATRICES ===
        self.frame_matrices = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_matrices.pack(fill="both", padx=20, pady=10, expand=True)

        label_a = ctk.CTkLabel(
            self.frame_matrices,
            text="Matriz A:",
            font=ctk.CTkFont(weight="bold"),
            text_color=COLOR_TEXT
        )
        label_a.pack(pady=(5, 5))

        self.entries_a_frame = ctk.CTkScrollableFrame(self.frame_matrices, fg_color=COLOR_FRAME)
        self.entries_a_frame.pack(fill="x", padx=10, pady=5)

        # Frame para Matriz B (inicialmente oculto)
        self.entries_b_frame = ctk.CTkScrollableFrame(self.frame_matrices, fg_color=COLOR_FRAME)

        # === RESULTADOS ===
        self.result_box = ctk.CTkTextbox(
            self,
            wrap="word",
            fg_color=COLOR_ENTRY,
            font=ctk.CTkFont(size=12),
            text_color=COLOR_TEXT,
            height=250
        )
        self.result_box.pack(fill="both", padx=20, pady=15, expand=True)
        self.result_box.insert("1.0", "Selecciona una propiedad y genera las matrices para iniciar.\n")

    # === FUNCIONES ===
    def generar_campos(self):
        """Genera campos de entrada para matriz A (y B si es propiedad 5)."""
        try:
            n = int(self.size_entry.get().strip())
            if n < 2:
                messagebox.showerror("Error", "El tamaño debe ser al menos 2.")
                return

            self.limpiar_campos()
            self.entries_a = []
            self.entries_b = []

            propiedad = self.propiedad_var.get()

            # === Generar matriz A ===
            for i in range(n):
                fila_a = []
                for j in range(n):
                    e_a = ctk.CTkEntry(self.entries_a_frame, width=60, height=30, placeholder_text=f"a{i+1}{j+1}")
                    e_a.grid(row=i, column=j, padx=2, pady=2)
                    fila_a.append(e_a)
                self.entries_a.append(fila_a)

            # === Mostrar y generar matriz B si es propiedad 5 ===
            if propiedad.startswith("5️⃣"):
                label_b = ctk.CTkLabel(
                    self.frame_matrices,
                    text="Matriz B:",
                    font=ctk.CTkFont(weight="bold"),
                    text_color=COLOR_TEXT
                )
                label_b.pack(pady=(10, 5))
                self.entries_b_frame.pack(fill="x", padx=10, pady=5)

                for i in range(n):
                    fila_b = []
                    for j in range(n):
                        e_b = ctk.CTkEntry(self.entries_b_frame, width=60, height=30, placeholder_text=f"b{i+1}{j+1}")
                        e_b.grid(row=i, column=j, padx=2, pady=2)
                        fila_b.append(e_b)
                    self.entries_b.append(fila_b)
            else:
                self.entries_b_frame.pack_forget()

            # Mensaje inicial
            self.result_box.delete("1.0", "end")
            self.result_box.insert("1.0", f"Campos generados para matriz A de {n}x{n}.\n")
            if propiedad.startswith("5️⃣"):
                self.result_box.insert("end", "También se generó la matriz B necesaria para esta propiedad.\n")
            self.result_box.insert("end", "Llena los valores y luego presiona 'Verificar Propiedad'.\n")

        except ValueError:
            messagebox.showerror("Error", "Ingresa un número entero válido.")

    def verificar_propiedad(self):
        """Verifica la propiedad seleccionada y muestra resultado en el TextBox."""
        propiedad = self.propiedad_var.get()
        self.result_box.delete("1.0", "end")

        try:
            A = [[int(entry.get()) for entry in fila] for fila in self.entries_a]
        except ValueError:
            self.result_box.insert("1.0", "❌ Error: Asegúrate de llenar todas las entradas numéricamente.\n")
            return

        if propiedad.startswith("1️⃣"):
            valido, pasos = solver.es_cero_fila_o_columna(A)
        elif propiedad.startswith("2️⃣"):
            valido, pasos = solver.son_iguales_o_proporcionales(A)
        elif propiedad.startswith("3️⃣"):
            A_copia = [fila[:] for fila in A]
            A_copia[0], A_copia[1] = A_copia[1], A_copia[0]
            valido, pasos = solver.intercambio_signo(A, A_copia)
        elif propiedad.startswith("4️⃣"):
            pasos = "⚠️ Propiedad 4 aún no implementada completamente."
            valido = None
        elif propiedad.startswith("5️⃣"):
            try:
                B = [[int(entry.get()) for entry in fila] for fila in self.entries_b]
                valido, pasos = solver.propiedad_multiplicativa(A, B, determinante_cofactores)
            except Exception as e:
                pasos = f"❌ Error al leer matriz B o calcular: {e}"
                valido = None
        elif propiedad.startswith("6️⃣"):
            pasos = (
                "✅ Propiedad 6: Suma de múltiplo de una fila a otra\n\n"
                "Si se suma un múltiplo escalar de una fila a otra, el determinante no cambia.\n"
                "Ejemplo: F2 ← F2 + k·F1  ⇒ det(A) se mantiene igual.\n"
            )
            valido = None
        else:
            pasos = "⚠️ Selecciona una propiedad válida desde el menú desplegable."

        self.result_box.insert("1.0", f"🔍 Propiedad seleccionada:\n{propiedad}\n\n")
        self.result_box.insert("end", pasos)

    def limpiar_campos(self):
        for frame in [self.entries_a_frame, self.entries_b_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

    def limpiar_todo(self):
        self.limpiar_campos()
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", "Interfaz reiniciada. Selecciona una propiedad y genera las matrices nuevamente.\n")


# === EJECUTAR APP ===
if __name__ == "__main__":
    ventana = ctk.CTk()
    ventana.title("Propiedades del Determinante")
    ventana.geometry("1000x850")
    ventana.configure(fg_color=COLOR_BG)

    app = PropiedadesDeterminanteApp(ventana)
    app.pack(fill="both", expand=True)

    ventana.mainloop()