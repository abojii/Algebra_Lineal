import tkinter as tk
from tkinter import ttk, messagebox
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

class SistemaEcuacionesApp:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg=COLOR_BG)
        self.metodo_var = tk.StringVar()

        # Título
        titulo = tk.Label(parent, text="Calculadora de Álgebra Lineal",
                          font=("Segoe UI", 18, "bold"),
                          fg=COLOR_BUTTON, bg=COLOR_BG)
        titulo.pack(pady=10)

        subtitulo = tk.Label(parent,
                             text="Resuelve sistemas de ecuaciones lineales",
                             font=("Segoe UI", 10),
                             fg=COLOR_SUBTEXT, bg=COLOR_BG)
        subtitulo.pack()

        # Frame de configuración
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
        
        # Metodos para resolver
        frame_metodos = tk.LabelFrame(parent, bg=COLOR_FRAME, bd=1, relief="solid")
        frame_metodos.pack(padx=20, pady=1, fill="x")
        
        LabelTituloMetodo = tk.Label(frame_metodos, text="Metodo de resolucion", fg=COLOR_SUBTEXT, bg=COLOR_FRAME)
        LabelTituloMetodo.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        self.metodo_var = tk.StringVar(value="gauss")  # Corregido: usar self.metodo_var

        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Eliminación Gaussiana",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="gauss", padx=10).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Eliminación Gauss-Jordan",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="gaussjordan", padx=10).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Escalonada Matriz (Forma escalonada)",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="Escalonada Matriz", padx=10).grid(row=3, column=0, sticky='w', padx=5, pady=2)
        tk.Radiobutton(frame_metodos, bg=COLOR_FRAME, fg=COLOR_TEXT, text="Escalonada Reducida Matriz",
                       variable=self.metodo_var, selectcolor=COLOR_FRAME, value="Escalonada Reducida", padx=10).grid(row=1, column=1, sticky='w', padx=5, pady=2)  # Corregido: row=4 para evitar superposición

        # Frame sistema de ecuaciones
        self.frame_sistema = tk.Frame(parent, bg=COLOR_FRAME, bd=1, relief="solid")
        self.frame_sistema.pack(fill="both", padx=20, pady=15, expand=True)

        self.entries = []  # Guardar casillas

        # Label de resultados
        self.result_label = tk.Label(parent, text="", font=("Segoe UI", 12),
                                     fg=COLOR_TEXT, bg=COLOR_BG)
        self.result_label.pack(pady=10)

    def generar_campos(self):
        # Limpiar frame anterior
        for widget in self.frame_sistema.winfo_children():
            widget.destroy()
        self.entries = []

        # Obtener tamaño
        dim_text = self.matriz_combo.get().lower().replace(" ", "")  # Ej: "2x2"
        try:
            filas_str, columnas_str = dim_text.split("x")
            filas = int(filas_str)
            columnas = int(columnas_str)
        except Exception:
            messagebox.showerror("Error", "Formato inválido. Use 'filas x columnas', por ejemplo '2x2'.")
            return

        tk.Label(self.frame_sistema, text=f"Ingrese los coeficientes de la matriz A ({filas}x{columnas}) y el vector b ({filas}x1):",
                 fg=COLOR_SUBTEXT, bg=COLOR_FRAME).pack(anchor="w", padx=10, pady=5)
        
        grid = tk.Frame(self.frame_sistema, bg=COLOR_FRAME)
        grid.pack(pady=10)

        # Crear casillas de A y b
        for i in range(filas):
            fila = []
            for j in range(columnas):
                e = tk.Entry(grid, width=5, bg=COLOR_ENTRY, fg=COLOR_TEXT,
                             insertbackground="white", justify="center")
                e.grid(row=i, column=j, padx=5, pady=5)
                fila.append(e)
            # Vector b
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
            filas = len(self.entries)
            columnas = len(self.entries[0]) - 1  # Última columna es vector b
            A = []
            b = []
            for fila in self.entries:
                A.append([float(fila[j].get()) for j in range(columnas)])
                b.append(float(fila[columnas].get()))
            
            if metodo == "gauss":
                messagebox.showinfo("Info", "Método Gauss implementado (pendiente de completar).")  # Corregido: showinfo en lugar de showerror
            # Aquí puedes agregar lógica para otros métodos
            
            self.result_label.config(text=f"Matriz A: {A}\nVector b: {b}")  # Ejemplo de resultado básico
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese solo números.")
            
    def limpiar(self):
        for widget in self.frame_sistema.winfo_children():
            widget.destroy()
        self.entries = []
        self.result_label.config(text="")
