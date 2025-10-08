import tkinter as tk
from tkinter import ttk, messagebox
import solverHomogeneo
from solverHomogeneo import solve_linear_system# Importa la función principal del solver

class LinearSystemSolver:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.num_rows = tk.IntVar(value=3)
        self.num_cols = tk.IntVar(value=3)
        self.is_homogeneous = tk.BooleanVar(value=False)
        
        # Entradas
        self.a_entries = None
        self.b_entries = None
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)
        
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        config_frame = ttk.LabelFrame(left_frame, text="Configuración del Sistema", padding=10)
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
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
        
        homo_frame = ttk.Frame(config_frame)
        homo_frame.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(homo_frame, text="Sistema Homogéneo (b = 0)", variable=self.is_homogeneous,
                        command=self.toggle_homogeneous).pack(anchor=tk.W)
        
        button_frame = ttk.Frame(config_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        init_btn = ttk.Button(button_frame, text="Inicializar Matrices", command=self.initialize_matrix)
        init_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(button_frame, text="Limpiar Solución", command=lambda: self.solution_text.delete(1.0, tk.END))
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        resolve_btn = ttk.Button(button_frame, text="Resolver Sistema", command=self.solve_system)
        resolve_btn.pack(side=tk.LEFT)
        
        input_frame = ttk.LabelFrame(left_frame, text="Entrada de Matriz y Vector", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
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
        
        b_frame = ttk.LabelFrame(input_frame, text="Vector de Términos Independientes b (filas x 1)", padding=5)
        b_frame.pack(fill=tk.Y, padx=(5, 0), side=tk.RIGHT)
        
        self.b_canvas = tk.Canvas(b_frame, bg='white', width=150, height=400)
        self.b_scrollbar_v = ttk.Scrollbar(b_frame, orient=tk.VERTICAL, command=self.b_canvas.yview)
        self.b_scrollable_frame = ttk.Frame(self.b_canvas)
        
        self.b_scrollable_frame.bind("<Configure>", lambda e: self.b_canvas.configure(scrollregion=self.b_canvas.bbox("all")))
        self.b_canvas.create_window((0, 0), window=self.b_scrollable_frame, anchor="nw")
        self.b_canvas.configure(yscrollcommand=self.b_scrollbar_v.set)
        
        self.b_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.b_scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        solution_label_frame = ttk.LabelFrame(right_frame, text="Solución del Sistema", padding=10)
        solution_label_frame.pack(fill=tk.BOTH, expand=True)
        solution_label_frame.grid_rowconfigure(0, weight=1)
        solution_label_frame.grid_columnconfigure(0, weight=1)
        
        self.solution_text = tk.Text(solution_label_frame, wrap=tk.WORD, height=40, width=100, font=('Courier', 10))
        self.solution_text.grid(row=0, column=0, sticky="nsew")
        
        v_scrollbar = ttk.Scrollbar(solution_label_frame, orient=tk.VERTICAL, command=self.solution_text.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.solution_text.config(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(solution_label_frame, orient=tk.HORIZONTAL, command=self.solution_text.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.solution_text.config(xscrollcommand=h_scrollbar.set)
        
        self.initialize_matrix()
    
    def update_matrix_size(self, event=None):
        # Placeholder: No hace nada hasta inicializar
        pass
    
    def initialize_matrix(self):
        rows = self.num_rows.get()
        cols = self.num_cols.get()
        
        # Limpiar frames
        for widget in self.a_scrollable_frame.winfo_children():
            widget.destroy()
        for widget in self.b_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Crear entradas para A
        self.a_entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ttk.Entry(self.a_scrollable_frame, width=8, font=('Courier', 10))
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                row_entries.append(entry)
            self.a_entries.append(row_entries)
        
        self.a_canvas.configure(scrollregion=self.a_canvas.bbox("all"))
        self.a_canvas.update_idletasks()
        
        # Crear entradas para b
        self.b_entries = []
        if not self.is_homogeneous.get():
            for i in range(rows):
                entry = ttk.Entry(self.b_scrollable_frame, width=8, font=('Courier', 10))
                entry.grid(row=i, column=0, padx=2, pady=2)
                entry.insert(0, "0")
                self.b_entries.append(entry)
        else:
            for i in range(rows):
                label = ttk.Label(self.b_scrollable_frame, text="0", font=('Courier', 10), relief=tk.SUNKEN, width=8)
                label.grid(row=i, column=0, padx=2, pady=2)
                self.b_entries.append(None)
        
        self.b_canvas.configure(scrollregion=self.b_canvas.bbox("all"))
        self.b_canvas.update_idletasks()
        
        self.solution_text.delete(1.0, tk.END)
    
    def toggle_homogeneous(self):
        rows = self.num_rows.get()
        
        for widget in self.b_scrollable_frame.winfo_children():
            widget.destroy()
        
        self.b_entries = []
        if self.is_homogeneous.get():
            for i in range(rows):
                label = ttk.Label(self.b_scrollable_frame, text="0", font=('Courier', 10), relief=tk.SUNKEN, width=8)
                label.grid(row=i, column=0, padx=2, pady=2)
                self.b_entries.append(None)
        else:
            for i in range(rows):
                entry = ttk.Entry(self.b_scrollable_frame, width=8, font=('Courier', 10))
                entry.grid(row=i, column=0, padx=2, pady=2)
                entry.insert(0, "0")
                self.b_entries.append(entry)
        
        self.b_canvas.configure(scrollregion=self.b_canvas.bbox("all"))
        self.b_canvas.update_idletasks()
    
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
            self.solution_text.delete(1.0, tk.END)
            
            if result['error']:
                self.solution_text.insert(tk.END, f"Error: {result['error']}\n\n")
                self.solution_text.insert(tk.END, "\n".join(result['steps']))
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
            
            self.solution_text.insert(tk.END, output)
            
        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Error en los valores: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LinearSystemSolver(root)
    root.mainloop()
