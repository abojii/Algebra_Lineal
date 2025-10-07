import tkinter as tk
from tkinter import ttk, messagebox

class LinearSystemSolver:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg= "#2b2b40")
        
        # Variables para tamaños
        self.num_rows = tk.IntVar(value=3)
        self.num_cols = tk.IntVar(value=3)
        self.is_homogeneous = tk.BooleanVar(value=False)  # False: no homogéneo, True: homogéneo
        
        # Listas para entradas (sin NumPy)
        self.a_entries = None
        self.b_entries = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal dividido en izquierdo (config + input) y derecho (solución)
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Usar grid para main_frame con pesos para dar más espacio a la solución (derecha)
        main_frame.grid_columnconfigure(0, weight=1)  # Izquierda: peso 1 (menor expansión)
        main_frame.grid_columnconfigure(1, weight=2)  # Derecha: peso 2 (más espacio, ~2/3 del ancho)
        main_frame.grid_rowconfigure(0, weight=1)     # Fila única expande verticalmente
        
        # Frame izquierdo: Configuración + Entrada
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))  # Usar grid en lugar de pack
        
        # Configuración (arriba)
        config_frame = ttk.LabelFrame(left_frame, text="Configuración del Sistema", padding=10)
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Selección de tamaños (solo filas y columnas A)
        size_frame = ttk.Frame(config_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(size_frame, text="Número de ecuaciones (filas):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        row_spin = ttk.Spinbox(size_frame, from_=1, to=10, textvariable=self.num_rows, width=10)
        row_spin.grid(row=0, column=1, padx=5)
        row_spin.bind('<Return>', self.update_matrix_size)
        row_spin.bind('<<Any-Change>>', self.update_matrix_size)
        
        ttk.Label(size_frame, text="Número de variables (columnas A):").grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        col_spin = ttk.Spinbox(size_frame, from_=1, to=10, textvariable=self.num_cols, width=10)
        col_spin.grid(row=0, column=3, padx=5)
        col_spin.bind('<Return>', self.update_matrix_size)
        col_spin.bind('<<Any-Change>>', self.update_matrix_size)
        
        # Opción homogéneo/no homogéneo
        homo_frame = ttk.Frame(config_frame)
        homo_frame.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(homo_frame, text="Sistema Homogéneo (b = 0)", variable=self.is_homogeneous,
                        command=self.toggle_homogeneous).pack(anchor=tk.W)
        
        # Botón para inicializar matriz
        init_btn = ttk.Button(config_frame, text="Inicializar Matrices", command=self.initialize_matrix)
        init_btn.pack(pady=5)
        
        # Entrada de Datos (abajo)
        input_frame = ttk.LabelFrame(left_frame, text="Entrada de Matriz y Vector", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para matriz A (izquierda)
        a_frame = ttk.LabelFrame(input_frame, text="Matriz de Coeficientes A (filas x columnas)", padding=5)
        a_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 5), side=tk.LEFT)
        
        self.a_canvas = tk.Canvas(a_frame, bg='white', width=400, height=400)
        self.a_scrollbar_v = ttk.Scrollbar(a_frame, orient=tk.VERTICAL, command=self.a_canvas.yview)
        self.a_scrollbar_h = ttk.Scrollbar(a_frame, orient=tk.HORIZONTAL, command=self.a_canvas.xview)
        self.a_scrollable_frame = ttk.Frame(self.a_canvas)
        
        self.a_scrollable_frame.bind("<Configure>", lambda e: self.a_canvas.configure(scrollregion=self.a_canvas.bbox("all")))
        self.a_canvas.create_window((0, 0), window=self.a_scrollable_frame, anchor="nw")
        self.a_canvas.configure(yscrollcommand=self.a_scrollbar_v.set, xscrollcommand=self.a_scrollbar_h.set)
        
        self.a_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.a_scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.a_scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Frame para vector b (derecha, solo 1 columna)
        b_frame = ttk.LabelFrame(input_frame, text="Vector de Términos Independientes b (filas x 1)", padding=5)
        b_frame.pack(fill=tk.Y, padx=(5, 0), side=tk.RIGHT)
        
        self.b_canvas = tk.Canvas(b_frame, bg='white', width=150, height=400)  # Ancho reducido para vector simple
        self.b_scrollbar_v = ttk.Scrollbar(b_frame, orient=tk.VERTICAL, command=self.b_canvas.yview)
        self.b_scrollable_frame = ttk.Frame(self.b_canvas)
        
        self.b_scrollable_frame.bind("<Configure>", lambda e: self.b_canvas.configure(scrollregion=self.b_canvas.bbox("all")))
        self.b_canvas.create_window((0, 0), window=self.b_scrollable_frame, anchor="nw")
        self.b_canvas.configure(yscrollcommand=self.b_scrollbar_v.set)
        
        self.b_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.b_scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame derecho (solución) más grande y expandible
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 3))  # Usar grid para expansión
        right_frame.grid_rowconfigure(0, weight=1)      # Expande verticalmente
        right_frame.grid_columnconfigure(0, weight=1)   # Expande horizontalmente
        
        solution_label_frame = ttk.LabelFrame(right_frame, text="Solución del Sistema", padding=5)
        solution_label_frame.pack(fill=tk.BOTH, expand=True)  # O usa grid si prefieres
        # Configurar para expansión total
        solution_label_frame.grid_rowconfigure(0, weight=1)
        solution_label_frame.grid_columnconfigure(0, weight=1)
        
        # Text más grande (height=40 líneas, width=100 chars) y con grid para expansión
        self.solution_text = tk.Text(solution_label_frame, wrap=tk.WORD, height=40, width=100, font=('Courier', 10))
        self.solution_text.grid(row=0, column=0, sticky="nsew")  # Sticky para llenar el frame
        
        # Scrollbars para manejar el tamaño grande (vertical y horizontal)
        v_scrollbar = ttk.Scrollbar(solution_label_frame, orient=tk.VERTICAL, command=self.solution_text.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.solution_text.config(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(solution_label_frame, orient=tk.HORIZONTAL, command=self.solution_text.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.solution_text.config(xscrollcommand=h_scrollbar.set)
        
        # Botón en la parte inferior del left_frame (sin función de resolución; puedes agregar lógica aquí si quieres)
        # resolve_btn = ttk.Button(left_frame, text="Resolver Sistema", command=self.solve_system)  # Comentado: sin resolución
        clear_btn = ttk.Button(left_frame, text="Resolver Sistema", command=lambda: self.solution_text.delete(1.0, tk.END))
        clear_btn.pack(pady=10)
        
        # Inicializar con valores por defecto
        self.initialize_matrix()
        
    def update_matrix_size(self, event=None):
        # Actualizar tamaños, pero no reinicializar hasta que se presione inicializar
        pass
    
    def initialize_matrix(self):
        rows = self.num_rows.get()
        cols = self.num_cols.get()
        
        # Limpiar frames anteriores
        for widget in self.a_scrollable_frame.winfo_children():
            widget.destroy()
        for widget in self.b_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Crear entradas para A (grid de rows x cols)
        self.a_entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ttk.Entry(self.a_scrollable_frame, width=8, font=('Courier', 10))
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")  # Valor inicial
                row_entries.append(entry)
            self.a_entries.append(row_entries)
        
        # Ajustar canvas size para A
        self.a_canvas.configure(scrollregion=self.a_canvas.bbox("all"))
        self.a_canvas.update_idletasks()
        
        # Crear entradas para b (solo 1 columna)
        self.b_entries = []
        if not self.is_homogeneous.get():
            for i in range(rows):
                entry = ttk.Entry(self.b_scrollable_frame, width=8, font=('Courier', 10))
                entry.grid(row=i, column=0, padx=2, pady=2)
                entry.insert(0, "0")
                self.b_entries.append(entry)
        else:
            # Para homogéneo, mostrar b=vector cero fijo
            for i in range(rows):
                label = ttk.Label(self.b_scrollable_frame, text="0", font=('Courier', 10), relief=tk.SUNKEN, width=8)
                label.grid(row=i, column=0, padx=2, pady=2)
                self.b_entries.append(None)  # Placeholder
        
        # Ajustar canvas size para b
        self.b_canvas.configure(scrollregion=self.b_canvas.bbox("all"))
        self.b_canvas.update_idletasks()
        
        # Limpiar solución anterior
        self.solution_text.delete(1.0, tk.END)
        
    def toggle_homogeneous(self):
        rows = self.num_rows.get()
        
        # Limpiar b frame
        for widget in self.b_scrollable_frame.winfo_children():
            widget.destroy()
        
        self.b_entries = []
        if self.is_homogeneous.get():
            # Setear b a vector ceros y deshabilitar entradas
            for i in range(rows):
                label = ttk.Label(self.b_scrollable_frame, text="0", font=('Courier', 10), relief=tk.SUNKEN, width=8)
                label.grid(row=i, column=0, padx=2, pady=2)
                self.b_entries.append(None)  # Placeholder
        else:
            # Habilitar entradas de b
            for i in range(rows):
                entry = ttk.Entry(self.b_scrollable_frame, width=8, font=('Courier', 10))
                entry.grid(row=i, column=0, padx=2, pady=2)
                entry.insert(0, "0")  # Valor inicial
                self.b_entries.append(entry)
        
        self.b_canvas.configure(scrollregion=self.b_canvas.bbox("all"))
        self.b_canvas.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = LinearSystemSolver(root)
    root.mainloop()
