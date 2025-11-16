import customtkinter as ctk
from Interfaz.constantes import COLOR_BG, COLOR_FRAME, COLOR_BUTTON, COLOR_TEXT, COLOR_SUBTEXT

class MenuDashboard:
    def __init__(self, parent, show_frame_callback):
        self.parent = parent
        self.show_frame_callback = show_frame_callback

        # Configurar el parent con color y grid
        self.parent.configure(fg_color=COLOR_BG)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_rowconfigure(2, weight=1)

        # Título principal
        title = ctk.CTkLabel(self.parent, text="Bienvenido a la Calculadora de Álgebra Lineal", 
                             font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_TEXT)
        title.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="n")

        # Descripción
        desc = ctk.CTkLabel(self.parent, text="Selecciona una sección para empezar a calcular matrices, vectores y más.",
                            font=ctk.CTkFont(size=14), text_color=COLOR_SUBTEXT, wraplength=400)
        desc.grid(row=1, column=0, columnspan=2, pady=(0, 30), padx=20, sticky="n")

        # Tarjeta 1: Matrices
        card_matrices = ctk.CTkFrame(self.parent, fg_color=COLOR_FRAME, corner_radius=10)
        card_matrices.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        icon_mat = ctk.CTkLabel(card_matrices, text="📊", font=ctk.CTkFont(size=40))
        icon_mat.pack(pady=(20, 10))
        label_mat = ctk.CTkLabel(card_matrices, text="Matrices", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_TEXT)
        label_mat.pack(pady=(0, 10))
        desc_mat = ctk.CTkLabel(card_matrices, text="Operaciones, inversas, determinantes", font=ctk.CTkFont(size=12), text_color=COLOR_SUBTEXT)
        desc_mat.pack(pady=(0, 20))
        btn_mat = ctk.CTkButton(card_matrices, text="Ir a Matrices", fg_color=COLOR_BUTTON, command=lambda: self.show_frame_callback("calc"))
        btn_mat.pack(pady=(0, 20), padx=20, fill="x")

        # Tarjeta 2: Vectores
        card_vectores = ctk.CTkFrame(self.parent, fg_color=COLOR_FRAME, corner_radius=10)
        card_vectores.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")
        icon_vec = ctk.CTkLabel(card_vectores, text="➡️", font=ctk.CTkFont(size=40))
        icon_vec.pack(pady=(20, 10))
        label_vec = ctk.CTkLabel(card_vectores, text="Vectores", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_TEXT)
        label_vec.pack(pady=(0, 10))
        desc_vec = ctk.CTkLabel(card_vectores, text="Ecuaciones, propiedades, operaciones", font=ctk.CTkFont(size=12), text_color=COLOR_SUBTEXT)
        desc_vec.pack(pady=(0, 20))
        btn_vec = ctk.CTkButton(card_vectores, text="Ir a Vectores", fg_color=COLOR_BUTTON, command=lambda: self.show_frame_callback("otra"))
        btn_vec.pack(pady=(0, 20), padx=20, fill="x")

        # Pie de página (opcional)
        footer = ctk.CTkLabel(self.parent, text="Usa el menú lateral para más opciones | Versión 1.0", 
                              font=ctk.CTkFont(size=10), text_color=COLOR_SUBTEXT)
        footer.grid(row=3, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="s")
