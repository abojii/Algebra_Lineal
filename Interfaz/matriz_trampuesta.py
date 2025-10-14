import customtkinter as ctk  # type: ignore # Importa CustomTkinter
from customtkinter import CTkLabel, CTkEntry, CTkButton, CTkComboBox, CTkTextbox, CTkRadioButton # type: ignore

# Colores para el diseño
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

class MatrizTraspuestaApp:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg=COLOR_BG)
        
        # Título
        titulo = CTkLabel(parent, text="Calculadora de Matriz Traspuesta",
                          font=("Segoe UI", 18, "bold"),
                          text_color= COLOR_BUTTON)
        titulo.pack(pady=10)
        
        subtitulo = CTkLabel(parent,
                             text="Ingrese una matriz y calcule su traspuesta",
                             font=("Segoe UI", 10),
                             text_color= COLOR_SUBTEXT)
        subtitulo.pack()
        
        # Frame de configuración
        frame_config = ctk.CTkFrame(parent, fg_color= COLOR_FRAME)
        frame_config.pack(fill="x", padx=20, pady=15)
        
        CTkLabel(frame_config, text="Tamaño de la Matriz:",
                 text_color= COLOR_SUBTEXT).grid(row=0, column=0, padx=10, pady=10)
        
        self.matriz_combo = CTkComboBox(frame_config, values=["2x2", "3x3", "4x4"], width=120)
        self.matriz_combo.set("2x2")
        self.matriz_combo.grid(row=0, column=1, padx=5, pady=10)
        
        CTkButton(frame_config, text="Generar", command=self.generar_campos).grid(row=0, column=2, padx=5)
        CTkButton(frame_config, text="Calcular Traspuesta", command=self.calcular_traspuesta).grid(row=0, column=3, padx=5)
        CTkButton(frame_config, text="Limpiar", command=self.limpiar).grid(row=0, column=4, padx=5)
        
        # Frame para ingresar la matriz
        self.frame_sistema = ctk.CTkFrame(parent, fg_color= COLOR_FRAME)
        self.frame_sistema.pack(fill="both", padx=20, pady=15, expand=True)
        
        self.entries = []  # Para guardar las casillas de entrada
        
        # Área para resultados
        self.result_textbox = ctk.CTkTextbox(parent, height=200, width=400, fg_color= COLOR_FRAME, text_color= COLOR_TEXT)
        self.result_textbox.pack(pady=10)
    
    def generar_campos(self):
        # Limpiar frame anterior
        for widget in self.frame_sistema.winfo_children():
            widget.destroy()
        self.entries = []
        
        dim_text = self.matriz_combo.get().lower().replace(" ", "")  # Ej: "2x2"
        try:
            filas_str, columnas_str = dim_text.split("x")
            filas = int(filas_str)
            columnas = int(columnas_str)
        except Exception:
            ctk.CTkMessagebox(title="Error", message="Formato inválido. Use 'filas x columnas', por ejemplo '2x2'.")
            return
        
        CTkLabel(self.frame_sistema, text=f"Ingrese los elementos de la matriz ({filas}x{columnas}):",
                 text_color= COLOR_SUBTEXT).pack(anchor="w", padx=10, pady=5)
        
        grid = ctk.CTkFrame(self.frame_sistema, fg_color= COLOR_FRAME)
        grid.pack(pady=10)
        
        # Crear casillas para la matriz
        for i in range(filas):
            fila = []
            for j in range(columnas):
                e = CTkEntry(grid, width=50, fg_color= COLOR_ENTRY, text_color= COLOR_TEXT)
                e.grid(row=i, column=j, padx=5, pady=5)
                fila.append(e)
            self.entries.append(fila)
    
    def calcular_traspuesta(self):
        if not self.entries:
            ctk.CTkMessagebox(title="Atención", message="Primero genera los campos para la matriz.")
            return
        
        try:
            filas = len(self.entries)
            columnas = len(self.entries[0])  # Solo la matriz A
            matriz_original = []
            for fila in self.entries:
                matriz_original.append([float(fila[j].get()) for j in range(columnas)])
            
            # Mostrar la matriz original en los resultados
            self.result_textbox.delete(1.0, ctk.END)  # Limpiar el área de texto
            self.result_textbox.insert(ctk.END, "Matriz original:\n")
            self.mostrar_matriz(matriz_original)
            
            # Calcular la traspuesta
            matriz_traspuesta = self.obtener_traspuesta(matriz_original)
            
            self.result_textbox.insert(ctk.END, "\nObteniendo la traspuesta (intercambiando filas por columnas):\n")
            self.result_textbox.insert(ctk.END, "La matriz traspuesta es:\n")
            self.mostrar_matriz(matriz_traspuesta)
            
            # Verificar propiedades
            matriz_traspuesta_de_traspuesta = self.obtener_traspuesta(matriz_traspuesta)
            propiedad_cumplida = matriz_traspuesta_de_traspuesta == matriz_original
            self.result_textbox.insert(ctk.END, f"\nVerificación: La traspuesta de la traspuesta es igual a la original: {'Sí' if propiedad_cumplida else 'No'}")
            self.result_textbox.insert(ctk.END, "\nPropiedad: (Aᵀ)ᵀ = A se cumple.")
            
        except ValueError:
            ctk.CTkMessagebox(title="Error", message="Por favor, ingrese solo números en los campos.")
    
    def obtener_traspuesta(self, matriz):
        # Función para calcular la traspuesta: intercambia filas por columnas
        return [[matriz[j][i] for j in range(len(matriz))] for i in range(len(matriz[0]))]
    
    def mostrar_matriz(self, matriz):
        for fila in matriz:
            self.result_textbox.insert(ctk.END, str(fila) + "\n")
    
    def limpiar(self):
        for widget in self.frame_sistema.winfo_children():
            widget.destroy()
        self.entries = []
        self.result_textbox.delete(1.0, ctk.END)  # Limpiar el área de texto

# Ejecutar la aplicación
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Puedes cambiar a "light" si prefieres
    app = ctk.CTk()
    MatrizTraspuestaApp(app)
    app.mainloop()
