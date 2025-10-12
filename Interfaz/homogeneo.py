import customtkinter as ctk
from tkinter import messagebox  # Mantengo para errores (compatible con CTk)
from Models.solverHomogeneo import solve_linear_system  # Importa la función principal del solver

# Configuración global de tema (agrega esto solo una vez en tu app principal si no lo tienes)
ctk.set_appearance_mode("dark")  # Tema oscuro
ctk.set_default_color_theme("blue")  # Colores azules (ajusta si quieres)

class LinearSystemSolver:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color="#2b2b40")  # Fondo como en original
        
        # Variables (tkinter vars funcionan en CTk, pero uso ctk para consistencia)
        self.num_rows = ctk.IntVar(value=3)
        self.num_cols = ctk.IntVar(value=3)
        self.is_homogeneous = ctk.BooleanVar(value=False)
        
        # Entradas
        self.a_entries = None
        self.b_entries = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame principal
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")  # Transparente para heredar fondo
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configurar grid en main_frame (como original)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Left frame (config + input)
        left_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b40", corner_radius=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Config frame (simula LabelFrame con borde)
        config_frame = ctk.CTkFrame(left_frame, fg_color="#2b2b40", corner_radius=10,
                                    border_width=2, border_color="#555555")  # FIX: Borde visible
        config_frame.pack(fill="x", padx=10, pady=10)
        
        # Título para config (simula LabelFrame)
        config_title = ctk.CTkLabel(config_frame, text="Configuración del Sistema", font=ctk.CTkFont(size=14, weight="bold"))
        config_title.pack(pady=(10, 5))
        
        size_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        size_frame.pack(fill="x", pady=5)
        
        # Spinbox simulado con CTkEntry para rows
        ctk.CTkLabel(size_frame, text="Número de ecuaciones (filas):", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=5)
        self.row_entry = ctk.CTkEntry(size_frame, textvariable=self.num_rows, width=80, fg_color="white", text_color="black")
        self.row_entry.grid(row=0, column=1, padx=5, pady=5)
        self.row_entry.bind('<KeyRelease>', self.update_matrix_size)  # Simula cambio dinámico
        # Validación: Solo números 1-10
        self.row_entry.bind('<KeyRelease>', self.validate_spin_entry)
        
        # Spinbox simulado para cols
        ctk.CTkLabel(size_frame, text="Número de variables (columnas A):", font=ctk.CTkFont(size=12)).grid(row=0, column=2, sticky="w", padx=(20, 5), pady=5)
        self.col_entry = ctk.CTkEntry(size_frame, textvariable=self.num_cols, width=80, fg_color="white", text_color="black")
        self.col_entry.grid(row=0, column=3, padx=5, pady=5)
        self.col_entry.bind('<KeyRelease>', self.update_matrix_size)
        self.col_entry.bind('<KeyRelease>', self.validate_spin_entry)
        
        # Homogeneous checkbox
        homo_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        homo_frame.pack(fill="x", pady=5)
        self.homo_checkbox = ctk.CTkCheckBox(homo_frame, text="Sistema Homogéneo (b = 0)", variable=self.is_homogeneous,
                                            command=self.toggle_homogeneous, checkbox_width=20, checkbox_height=20)
        self.homo_checkbox.pack(anchor="w", pady=5)
        
        # Buttons frame
        button_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=5)
        
        self.init_btn = ctk.CTkButton(button_frame, text="Inicializar Matrices", command=self.initialize_matrix,
                                    fg_color="blue", text_color="white", corner_radius=8, height=30)
        self.init_btn.pack(side="left", padx=(0, 10), pady=5)
        
        clear_btn = ctk.CTkButton(button_frame, text="Limpiar Solución", command=self.clear_solution,
                                fg_color="gray", text_color="white", corner_radius=8, height=30)
        clear_btn.pack(side="left", padx=(0, 10), pady=5)
        
        self.resolve_btn = ctk.CTkButton(button_frame, text="Resolver Sistema", command=self.solve_system,
                                        fg_color="green", text_color="white", corner_radius=8, height=30)
        self.resolve_btn.pack(side="left", pady=5)
        
        # Input frame (simula LabelFrame con borde)
        input_frame = ctk.CTkFrame(left_frame, fg_color="#2b2b40", corner_radius=10,
                                border_width=2, border_color="#555555")  # FIX: Borde visible
        input_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        input_title = ctk.CTkLabel(input_frame, text="Entrada de Matriz y Vector", font=ctk.CTkFont(size=14, weight="bold"))
        input_title.pack(pady=(10, 5))
        
        # A frame (matriz con borde)
        a_frame = ctk.CTkFrame(input_frame, fg_color="#2b2b40", corner_radius=10,
                            border_width=2, border_color="#555555")  # FIX: Borde visible
        a_frame.pack(fill="both", expand=True, padx=(10, 5), side="left", pady=5)
        
        a_title = ctk.CTkLabel(a_frame, text="Matriz de Coeficientes A (filas x columnas)", font=ctk.CTkFont(size=12, weight="bold"))
        a_title.pack(pady=(10, 5))
        
        # Scrollable para A
        self.a_scrollable = ctk.CTkScrollableFrame(a_frame, fg_color="#2b2b40", scrollbar_button_color="gray")
        self.a_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # B frame (vector con borde)
        b_frame = ctk.CTkFrame(input_frame, fg_color="#2b2b40", corner_radius=10,
                            border_width=2, border_color="#555555")  # FIX: Borde visible
        b_frame.pack(fill="y", padx=(5, 10), side="right", pady=5)
        
        b_title = ctk.CTkLabel(b_frame, text="Vector de Términos Independientes b (filas x 1)", font=ctk.CTkFont(size=12, weight="bold"))
        b_title.pack(pady=(10, 5))
        
        # Scrollable para b
        self.b_scrollable = ctk.CTkScrollableFrame(b_frame, fg_color="#2b2b40", scrollbar_button_color="gray")
        self.b_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Right frame (solución)
        right_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b40", corner_radius=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Solution frame (simula LabelFrame con borde)
        solution_frame = ctk.CTkFrame(right_frame, fg_color="#2b2b40", corner_radius=10,
                                    border_width=2, border_color="#555555")  # FIX: Borde visible
        solution_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # FIX: Configurar grid en solution_frame antes de agregar widgets
        solution_frame.grid_rowconfigure(0, weight=0)  # Fila 0 para título (fija)
        solution_frame.grid_rowconfigure(1, weight=1)  # Fila 1 para textbox (expande)
        solution_frame.grid_columnconfigure(0, weight=1)  # Columna 0 expande
        
        solution_title = ctk.CTkLabel(solution_frame, text="Solución del Sistema", font=ctk.CTkFont(size=14, weight="bold"))
        solution_title.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))  # FIX: Cambiado a grid (no pack)
        
        # Textbox para solución (con scroll integrado)
        self.solution_text = ctk.CTkTextbox(solution_frame, wrap="word", font=ctk.CTkFont(family="Courier", size=10),
                                            fg_color="white", text_color="black", height=400)
        self.solution_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)  # Mantiene grid
        
        self.initialize_matrix()  # Inicializar al final

    def validate_spin_entry(self, event=None):
        """Valida entradas de spinbox: solo números enteros 1-10."""
        entry = event.widget
        value = entry.get().strip()
        if value.isdigit():
            val = int(value)
            if val < 1:
                entry.delete(0, "end")
                entry.insert(0, "1")
            elif val > 10:
                entry.delete(0, "end")
                entry.insert(0, "10")
        else:
            # Remover no-dígitos (mantener solo el último dígito válido)
            digits = ''.join(filter(str.isdigit, value))
            entry.delete(0, "end")
            if digits:
                val = int(digits)
                if 1 <= val <= 10:
                    entry.insert(0, str(val))
                else:
                    entry.insert(0, "1" if val < 1 else "10")
            else:
                entry.insert(0, "1")
    
    def update_matrix_size(self, event=None):
        # Actualiza al cambiar tamaño (llama a initialize si se presiona Enter o cambia)
        if event and event.keysym == "Return":
            self.initialize_matrix()
        # Para cambios dinámicos, opcional: debounce si quieres, pero por ahora solo inicializa en botón
    
    def initialize_matrix(self):
        rows = self.num_rows.get()
        cols = self.num_cols.get()
        
        # Limpiar A
        for widget in self.a_scrollable.winfo_children():
            widget.destroy()
        
        # Crear entradas para A
        self.a_entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ctk.CTkEntry(self.a_scrollable, width=60, height=25, fg_color="white", text_color="black",
                                     font=ctk.CTkFont(family="Courier", size=10))
                entry.grid(row=i, column=j, padx=2, pady=2, sticky="ew")
                entry.insert(0, "0")
                row_entries.append(entry)
            self.a_entries.append(row_entries)
        
        # Configurar columnas para expansión uniforme
        for j in range(cols):
            self.a_scrollable.grid_columnconfigure(j, weight=1)
        
        # Limpiar B
        for widget in self.b_scrollable.winfo_children():
            widget.destroy()
        
        # Crear entradas para b
        self.b_entries = []
        if not self.is_homogeneous.get():
            for i in range(rows):
                entry = ctk.CTkEntry(self.b_scrollable, width=60, height=25, fg_color="white", text_color="black",
                                     font=ctk.CTkFont(family="Courier", size=10))
                entry.grid(row=i, column=0, padx=2, pady=2, sticky="ew")
                entry.insert(0, "0")
                self.b_entries.append(entry)
        else:
            for i in range(rows):
                label = ctk.CTkLabel(self.b_scrollable, text="0", font=ctk.CTkFont(family="Courier", size=10),
                                     fg_color="gray", text_color="white", width=60, height=25, anchor="center")
                label.grid(row=i, column=0, padx=2, pady=2, sticky="ew")
                self.b_entries.append(None)
        
        self.b_scrollable.grid_columnconfigure(0, weight=1)
        
        self.clear_solution()
    
    def toggle_homogeneous(self):
        rows = self.num_rows.get()
        
        # Limpiar B
        for widget in self.b_scrollable.winfo_children():
            widget.destroy()
        
        self.b_entries = []
        if self.is_homogeneous.get():
            for i in range(rows):
                label = ctk.CTkLabel(self.b_scrollable, text="0", font=ctk.CTkFont(family="Courier", size=10),
                                     fg_color="gray", text_color="white", width=60, height=25, anchor="center")
                label.grid(row=i, column=0, padx=2, pady=2, sticky="ew")
                self.b_entries.append(None)
        else:
            for i in range(rows):
                entry = ctk.CTkEntry(self.b_scrollable, width=60, height=25, fg_color="white", text_color="black",
                                     font=ctk.CTkFont(family="Courier", size=10))
                entry.grid(row=i, column=0, padx=2, pady=2, sticky="ew")
                entry.insert(0, "0")
                self.b_entries.append(entry)
        
        self.b_scrollable.grid_columnconfigure(0, weight=1)
    
    def clear_solution(self):
        self.solution_text.delete("1.0", "end")
    
    def solve_system(self):
        """AQUÍ ESTÁ LA LLAMADA PRINCIPAL AL SOLVER"""
        try:
            rows = self.num_rows.get()
            cols = self.num_cols.get()
            
            # Leer matriz A (lista de listas de floats)
            A = []
            for i in range(rows):
                row = []
                for j in range(cols):
                    val_str = self.a_entries[i][j].get().strip()
                    try:
                        val = float(val_str) if val_str else 0.0
                        row.append(val)
                    except ValueError:
                        raise ValueError(f"Valor inválido en A[{i}][{j}]: '{val_str}'")
                A.append(row)
            
            # Leer vector b (lista de floats)
            b = []
            homogeneous = self.is_homogeneous.get()
            if homogeneous:
                b = [0.0] * rows
            else:
                for i in range(rows):
                    if self.b_entries[i] is None:
                        b.append(0.0)
                    else:
                        val_str = self.b_entries[i].get().strip()
                        try:
                            val = float(val_str) if val_str else 0.0
                            b.append(val)
                        except ValueError:
                            raise ValueError(f"Valor inválido en b[{i}]: '{val_str}'")
            
            # LIMITE: AQUÍ SE LLAMA AL SOLVER (línea clave)
            result = solve_linear_system(A, b, homogeneous=homogeneous)
            
            # Limpiar y mostrar resultados formateados
            self.clear_solution()
            
            if result['error']:
                self.solution_text.insert("end", f"Error: {result['error']}\n\n")
                self.solution_text.insert("end", "\n".join(result['steps']))
                return
            
            # Formatear salida
            output = "=== PASOS PASO A PASO (Eliminación Gauss-Jordan) ===\n"
            output += "\n".join(result['steps']) + "\n\n"
            
            output += "=== RESULTADOS ===\n"
            output += f"Rango de A: {result['rank']}\n"
            output += f"Variables libres: {result['free_vars']}\n"
            output += f"Columnas de A linealmente independientes: {result['linear_independent']}\n\n"
            
            output += f"Solución trivial: {result['solution_trivial']}\n\n"
            output += f"Solución particular: {result['particular_solution']}\n\n"
            output += f"Solución general: {result['solution_general']}\n"
            
            self.solution_text.insert("end", output)
            
        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Error en los valores: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver: {str(e)}")


if __name__ == "__main__":
    # Para testing standalone: Crea una ventana CTk
    root = ctk.CTk()
    app = LinearSystemSolver(root)
    root.mainloop()
