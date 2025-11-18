import tkinter as tk
from tkinter import messagebox, ttk

class VectorAlgebraPropertiesGUI:
    def __init__(self, root):
        self.root = root
        
        # Tamaño adecuado para múltiples secciones
        
        # Variables para dimensión
        self.n_var = tk.IntVar(value=2)  # Dimensión n de ℝⁿ
        
        # Frames para secciones
        self.create_dimension_frame()
        self.create_buttons_frame()
        self.vectors_frame = None
        self.scalar_frame = None
        self.result_frame = None
        self.result_text = None
        
        # Almacenamiento de entradas
        self.vector_entries = {}  # Diccionario: 'u': [entries], 'v': [...], etc.
        self.scalar_entry = None
        self.vectors = ['u', 'v', 'w']  # Vectores disponibles
        self.current_operation = None  # Para rastrear qué operación se está realizando
        
    def create_dimension_frame(self):
        
        dim_frame = tk.LabelFrame(self.root, text="Dimensión", padx=10, pady=10)
        dim_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(dim_frame, text="Dimensión n de ℝⁿ:").grid(row=0, column=0, sticky="w")
        tk.Entry(dim_frame, textvariable=self.n_var, width=5).grid(row=0, column=1)
        
    def create_buttons_frame(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Botones para generar entradas
        tk.Button(btn_frame, text="Generar Entradas para Vectores (u, v, w)", 
                  command=self.generate_vector_entries).grid(row=0, column=0, sticky="w",padx=5, pady= 5)
        tk.Button(btn_frame, text="Generar Entrada para Escalar k", 
                  command=self.generate_scalar_entry).grid(row=1, column=0, sticky="w",padx=5, pady=5)
        
        # Botones para operaciones
        tk.Button(btn_frame, text="Calcular Suma u + v", command=lambda: self.perform_operation('sum_uv'), 
                  bg="lightblue").grid(row=0, column=1, sticky="w",padx=5, pady=5)
        tk.Button(btn_frame, text="Calcular k * u", command=lambda: self.perform_operation('scalar_u'), 
                  bg="lightblue").grid(row=1, column=1, sticky="w", pady=5)
        
        # Botones para verificaciones
        tk.Button(btn_frame, text="Verificar Conmutativa (u + v = v + u)", 
                  command=lambda: self.perform_operation('commutative'), bg="lightgreen").grid(row=0, column=2, sticky="w",padx=5, pady=5)
        tk.Button(btn_frame, text="Verificar Asociativa ((u + v) + w = u + (v + w))", 
                  command=lambda: self.perform_operation('associative'), bg="lightgreen").grid(row=1, column=2, sticky="w",padx=5, pady=5)
        tk.Button(btn_frame, text="Verificar Vector Cero (0 + u = u)", 
                  command=lambda: self.perform_operation('zero'), bg="lightgreen").grid(row=0, column=3, sticky="w",padx=5, pady=5)
        tk.Button(btn_frame, text="Verificar Vector Opuesto (u + (-u) = 0)", 
                  command=lambda: self.perform_operation('opposite'), bg="lightgreen").grid(row=1, column=3, sticky="w",padx=5, pady=5)
        
        tk.Button(btn_frame, text="Limpiar", command=self.clear_all, bg="lightcoral").grid(row=0, column=4, sticky="w",padx=5, pady=5)
        
    def generate_vector_entries(self):
        n = self.n_var.get()
        if n <= 0:
            messagebox.showerror("Error", "La dimensión n debe ser positiva.")
            return
        
        # Limpiar frame anterior si existe
        if self.vectors_frame:
            self.vectors_frame.destroy()
        self.vector_entries = {}
        
        self.vectors_frame = tk.LabelFrame(self.root, text=f"Vectores en ℝ^{n}", padx=10, pady=10)
        self.vectors_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Crear entradas para cada vector (u, v, w)
        for vec_name in self.vectors:
            vec_frame = tk.LabelFrame(self.vectors_frame, text=f"Vector {vec_name} ({n} x 1)", padx=5, pady=5)
            vec_frame.pack(fill="x", pady=2)
            
            entries = []
            for i in range(n):
                entry = tk.Entry(vec_frame, width=6)
                entry.grid(row=i, column=0, padx=2, pady=1)
                entries.append(entry)
            self.vector_entries[vec_name] = entries
    
    def generate_scalar_entry(self):
        if self.n_var.get() <= 0:
            messagebox.showerror("Error", "La dimensión n debe ser positiva primero.")
            return
        
        # Limpiar frame anterior si existe
        if self.scalar_frame:
            self.scalar_frame.destroy()
        
        self.scalar_frame = tk.LabelFrame(self.root, text="Escalar k", padx=10, pady=10)
        self.scalar_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(self.scalar_frame, text="k:").pack()
        self.scalar_entry = tk.Entry(self.scalar_frame, width=10)
        self.scalar_entry.pack(pady=5)
    
    def read_vector(self, vec_name):
        n = self.n_var.get()
        entries = self.vector_entries.get(vec_name, [])
        if len(entries) != n:
            messagebox.showerror("Error", f"Entradas para vector {vec_name} no generadas o incorrectas.")
            return None
        
        vec = []
        for i in range(n):
            val_str = entries[i].get().strip()
            if not val_str:
                messagebox.showerror("Error", f"Elemento {vec_name}[{i+1}] vacío.")
                return None
            try:
                vec.append(float(val_str))
            except ValueError:
                messagebox.showerror("Error", f"Elemento {vec_name}[{i+1}] no es numérico: {val_str}")
                return None
        return vec
    
    def read_scalar(self):
        if self.scalar_entry is None:
            messagebox.showerror("Error", "Entrada para escalar k no generada.")
            return None
        val_str = self.scalar_entry.get().strip()
        if not val_str:
            messagebox.showerror("Error", "Escalar k vacío.")
            return None
        try:
            return float(val_str)
        except ValueError:
            messagebox.showerror("Error", f"Escalar k no es numérico: {val_str}")
            return None
    
    def add_vectors(self, vec1, vec2):
        n = len(vec1)
        if len(vec2) != n:
            return None
        return [vec1[i] + vec2[i] for i in range(n)]
    
    def scalar_multiply(self, k, vec):
        return [k * vec[i] for i in range(len(vec))]
    
    def negate_vector(self, vec):
        return [-vec[i] for i in range(len(vec))]
    
    def zero_vector(self, n):
        return [0.0] * n
    
    def get_operation_title(self, op_type):
        titles = {
            'sum_uv': 'Suma de Vectores u + v',
            'scalar_u': 'Multiplicación por Escalar k * u',
            'commutative': 'Verificación de Propiedad Conmutativa',
            'associative': 'Verificación de Propiedad Asociativa',
            'zero': 'Verificación de Vector Cero',
            'opposite': 'Verificación de Vector Opuesto'
        }
        return titles.get(op_type, 'Operación Desconocida')

    def perform_operation(self, op_type):
        self.current_operation = op_type
        data = {}
        
        if op_type in ['sum_uv', 'commutative']:
            # Necesita u y v
            u = self.read_vector('u')
            if u is None:
                return
            v = self.read_vector('v')
            if v is None:
                return
            data['u'] = u
            data['v'] = v
        elif op_type == 'associative':
            # Necesita u, v, w
            u = self.read_vector('u')
            v = self.read_vector('v')
            w = self.read_vector('w')
            if any(x is None for x in [u, v, w]):
                return
            data['u'] = u
            data['v'] = v
            data['w'] = w
        elif op_type in ['scalar_u', 'opposite', 'zero']:
            # Necesita u (y k para scalar)
            u = self.read_vector('u')
            if u is None:
                return
            data['u'] = u
            if op_type == 'scalar_u':
                k = self.read_scalar()
                if k is None:
                    return
                data['k'] = k
        else:
            messagebox.showerror("Error", "Operación no soportada.")
            return
        
        # Realizar cálculo y mostrar
        self.compute_and_display(op_type, data)
    
    def compute_and_display(self, op_type, data):
        n = self.n_var.get()
        
        result_str = f"=== {self.get_operation_title(op_type)} ===\n\n"
        
        # Mostrar vectores involucrados
        if 'u' in data:
            result_str += self.format_vector("Vector u", data['u'])
        if 'v' in data:
            result_str += self.format_vector("Vector v", data['v'])
        if 'w' in data:
            result_str += self.format_vector("Vector w", data['w'])
        if 'k' in data:
            result_str += f"Escalar k: {data['k']:.6f}\n\n"
        
        if op_type == 'sum_uv':
            result_str += "Cálculo de suma u + v (componente por componente):\n"
            sum_vec = self.add_vectors(data['u'], data['v'])
            for i in range(n):
                result_str += f"  u[{i+1}] + v[{i+1}] = {data['u'][i]:.6f} + {data['v'][i]:.6f} = {sum_vec[i]:.6f}\n"
            result_str += "\n" + self.format_vector("Resultado u + v", sum_vec)
        
        elif op_type == 'scalar_u':
            result_str += "Cálculo de k * u (componente por componente):\n"
            scaled_vec = self.scalar_multiply(data['k'], data['u'])
            for i in range(n):
                result_str += f"  k * u[{i+1}] = {data['k']:.6f} * {data['u'][i]:.6f} = {scaled_vec[i]:.6f}\n"
            result_str += "\n" + self.format_vector("Resultado k * u", scaled_vec)
        
        elif op_type == 'commutative':
            result_str += "Verificación de propiedad conmutativa: u + v =? v + u\n\n"
            sum1 = self.add_vectors(data['u'], data['v'])
            sum2 = self.add_vectors(data['v'], data['u'])
            result_str += "u + v:\n"
            for i in range(n):
                result_str += f"  {data['u'][i]:.6f} + {data['v'][i]:.6f} = {sum1[i]:.6f}\n"
            result_str += "\nv + u:\n"
            for i in range(n):
                result_str += f"  {data['v'][i]:.6f} + {data['u'][i]:.6f} = {sum2[i]:.6f}\n"
            is_equal = sum1 == sum2
            result_str += f"\n¿Iguales? {'Sí (propiedad conmutativa se verifica)' if is_equal else 'No'}\n"
            result_str += self.format_vector("u + v", sum1)
            result_str += self.format_vector("v + u", sum2)
        
        elif op_type == 'associative':
            result_str += "Verificación de propiedad asociativa: (u + v) + w =? u + (v + w)\n\n"
            uv = self.add_vectors(data['u'], data['v'])
            left = self.add_vectors(uv, data['w'])
            vw = self.add_vectors(data['v'], data['w'])
            right = self.add_vectors(data['u'], vw)
            
            result_str += "(u + v) + w:\n"
            result_str += "Primero, u + v:\n"
            for i in range(n):
                result_str += f"  {data['u'][i]:.6f} + {data['v'][i]:.6f} = {uv[i]:.6f}\n"
            result_str += "Luego, (u + v) + w:\n"
            for i in range(n):
                result_str += f"  {uv[i]:.6f} + {data['w'][i]:.6f} = {left[i]:.6f}\n"
            
            result_str += "\nu + (v + w):\n"
            result_str += "Primero, v + w:\n"
            for i in range(n):
                result_str += f"  {data['v'][i]:.6f} + {data['w'][i]:.6f} = {vw[i]:.6f}\n"
            result_str += "Luego, u + (v + w):\n"
            for i in range(n):
                result_str += f"  {data['u'][i]:.6f} + {vw[i]:.6f} = {right[i]:.6f}\n"
            
            is_equal = left == right
            result_str += f"\n¿Iguales? {'Sí (propiedad asociativa se verifica)' if is_equal else 'No'}\n"
        
            is_equal = left == right
            result_str += f"\n¿Iguales? {'Sí (propiedad asociativa se verifica)' if is_equal else 'No'}\n"
            result_str += self.format_vector("(u + v) + w", left)
            result_str += self.format_vector("u + (v + w)", right)
        
        elif op_type == 'zero':
            result_str += "Verificación de vector cero: 0 + u =? u\n\n"
            zero = self.zero_vector(n)
            sum_zero_u = self.add_vectors(zero, data['u'])
            result_str += self.format_vector("Vector cero (0)", zero, compact=True)
            result_str += "\n0 + u:\n"
            for i in range(n):
                result_str += f"  0[{i+1}] + u[{i+1}] = 0.000000 + {data['u'][i]:.6f} = {sum_zero_u[i]:.6f}\n"
            is_equal = sum_zero_u == data['u']
            result_str += f"\n¿Igual a u? {'Sí (propiedad del vector cero se verifica)' if is_equal else 'No'}\n"
            result_str += self.format_vector("0 + u", sum_zero_u)
            result_str += self.format_vector("u", data['u'])
        
        elif op_type == 'opposite':
            result_str += "Verificación de vector opuesto: u + (-u) =? 0\n\n"
            neg_u = self.negate_vector(data['u'])
            sum_opp = self.add_vectors(data['u'], neg_u)
            result_str += self.format_vector("Vector opuesto (-u)", neg_u)
            result_str += "\nu + (-u):\n"
            for i in range(n):
                result_str += f"  u[{i+1}] + (-u)[{i+1}] = {data['u'][i]:.6f} + {neg_u[i]:.6f} = {sum_opp[i]:.6f}\n"
            is_equal = all(abs(x) < 1e-10 for x in sum_opp)  # Tolerancia para flotantes
            result_str += f"\n¿Igual al vector cero? {'Sí (propiedad del vector opuesto se verifica)' if is_equal else 'No'}\n"
            result_str += self.format_vector("u + (-u)", sum_opp)
            result_str += self.format_vector("Vector cero (0)", self.zero_vector(n), compact=True)
        
        # Mostrar en GUI
        self.display_result(result_str)
    
    def format_vector(self, label, vec, compact=False):
        n = len(vec)
        if compact:
            vec_str = f"{label} = ["
            for i, val in enumerate(vec):
                vec_str += f"{val:.6f}"
                if i < n - 1:
                    vec_str += ", "
            vec_str += "]\n\n"
            return vec_str
        
        vec_str = f"{label}:\n"
        vec_str += "  [ "
        for i, val in enumerate(vec):
            if i > 0:
                vec_str += "\n    "
            vec_str += f"{val:.6f} "
        vec_str += "]\n\n"
        return vec_str
    
    def display_result(self, result_str):
        if self.result_frame:
            self.result_frame.destroy()
        
        self.result_frame = tk.LabelFrame(self.root, text="Resultado (Paso a Paso)", padx=10, pady=10)
        self.result_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Widget de texto con scrollbar
        result_text = tk.Text(self.result_frame, height=25, width=100, wrap=tk.WORD, font=("Courier", 9))
        result_text.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_text.config(yscrollcommand=scrollbar.set)
        
        result_text.insert(tk.END, result_str)
        result_text.config(state=tk.DISABLED)
    
    def clear_all(self):
        if self.vectors_frame:
            self.vectors_frame.destroy()
        if self.scalar_frame:
            self.scalar_frame.destroy()
        if self.result_frame:
            self.result_frame.destroy()
        self.vector_entries = {}
        self.scalar_entry = None
        # Mantener dimensión por defecto

if __name__ == "__main__":
    root = tk.Tk()
    app = VectorAlgebraPropertiesGUI(root)
    root.mainloop()