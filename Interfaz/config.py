import customtkinter as ctk
# Definición de temas con colores personalizados
themes = {
    "Oscuro": {
        "bg": "#1e1e2f",
        "frame": "#2b2b40",
        "text": "#ffffff",
        "subtext": "#bbbbbb",
        "button": "#3b82f6",
        "entry": "#3a3a4f",
        "sidebar_bg": "#1A202C",
        "sidebar_hover": "#1F2937",
        "sidebar_active": "#2563EB",
        "sidebar_text": "#E5E7EB",
        "sidebar_subtext": "#9CA3AF",
        "sidebar_separator": "#1A2234"
    },
    "Claro": {
        "bg": "#f0f0f0",
        "frame": "#ffffff",
        "text": "#000000",
        "subtext": "#666666",
        "button": "#007bff",
        "entry": "#e9ecef",
        "sidebar_bg": "#e0e0e0",
        "sidebar_hover": "#cccccc",
        "sidebar_active": "#0056b3",
        "sidebar_text": "#000000",
        "sidebar_subtext": "#555555",
        "sidebar_separator": "#aaaaaa"
    },
    "Neutro": {
        "bg": "#f5f5f5",
        "frame": "#e0e0e0",
        "text": "#333333",
        "subtext": "#777777",
        "button": "#6c757d",
        "entry": "#d1ecf1",
        "sidebar_bg": "#d0d0d0",
        "sidebar_hover": "#b0b0b0",
        "sidebar_active": "#4a90e2",
        "sidebar_text": "#333333",
        "sidebar_subtext": "#666666",
        "sidebar_separator": "#999999"
    }
}

class ConfiguracionesDashboard:
    def __init__(self, parent, apply_settings_callback):
        self.parent = parent
        self.apply_settings_callback = apply_settings_callback
        self.current_theme = "Oscuro"  # Tema por defecto

        # Configurar el parent con colores del tema actual
        theme = themes[self.current_theme]
        self.parent.configure(fg_color=theme["bg"])
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=0)  # Header
        self.parent.grid_rowconfigure(1, weight=1)  # Scrollable content
        self.parent.grid_rowconfigure(2, weight=0)  # Footer

        # Header: Título y descripción
        self.header_frame = ctk.CTkFrame(self.parent, fg_color=theme["bg"], corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(self.header_frame, text="Configuraciones del Programa", 
                                  font=ctk.CTkFont(size=28, weight="bold"), text_color=theme["text"])
        self.title.grid(row=0, column=0, pady=(10, 5), sticky="w")

        self.desc = ctk.CTkLabel(self.header_frame, text="Personaliza la apariencia y comportamiento de la aplicación para adaptarla a tus necesidades.",
                                 font=ctk.CTkFont(size=14), text_color=theme["subtext"], wraplength=600)
        self.desc.grid(row=1, column=0, pady=(0, 10), sticky="w")

        # Scrollable Frame para el contenido principal
        self.scrollable_frame = ctk.CTkScrollableFrame(self.parent, fg_color=theme["bg"], corner_radius=10)
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

        # Tarjeta 1: Tema de la Interfaz
        self.card_tema = ctk.CTkFrame(self.scrollable_frame, fg_color=theme["frame"], corner_radius=15, border_width=1, border_color=theme["button"])
        self.card_tema.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.card_tema.grid_columnconfigure(0, weight=1)

        self.icon_tema = ctk.CTkLabel(self.card_tema, text="🌙", font=ctk.CTkFont(size=48))
        self.icon_tema.grid(row=0, column=0, pady=(20, 10), sticky="n")

        self.label_tema = ctk.CTkLabel(self.card_tema, text="Tema de la Interfaz", font=ctk.CTkFont(size=18, weight="bold"), text_color=theme["text"])
        self.label_tema.grid(row=1, column=0, pady=(0, 5), sticky="n")

        self.desc_tema = ctk.CTkLabel(self.card_tema, text="Selecciona el modo de apariencia para una experiencia visual óptima.", 
                                      font=ctk.CTkFont(size=12), text_color=theme["subtext"], wraplength=300)
        self.desc_tema.grid(row=2, column=0, pady=(0, 15), sticky="n")

        self.tema_var = ctk.StringVar(value="Oscuro")  # Cambiado a "Oscuro" por defecto
        self.tema_menu = ctk.CTkOptionMenu(self.card_tema, values=["Claro", "Neutro", "Oscuro"], variable=self.tema_var, 
                                           fg_color=theme["button"], button_color=theme["button"], button_hover_color=theme["text"],
                                           command=self.aplicar_tema_auto)
        self.tema_menu.grid(row=3, column=0, pady=(0, 20), padx=20, sticky="ew")

        # Tarjeta 2: Precisión de Cálculos
        self.card_precision = ctk.CTkFrame(self.scrollable_frame, fg_color=theme["frame"], corner_radius=15, border_width=1, border_color=theme["button"])
        self.card_precision.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.card_precision.grid_columnconfigure(0, weight=1)

        self.icon_prec = ctk.CTkLabel(self.card_precision, text="⚙️", font=ctk.CTkFont(size=48))
        self.icon_prec.grid(row=0, column=0, pady=(20, 10), sticky="n")

        self.label_prec = ctk.CTkLabel(self.card_precision, text="Precisión de Cálculos", font=ctk.CTkFont(size=18, weight="bold"), text_color=theme["text"])
        self.label_prec.grid(row=1, column=0, pady=(0, 5), sticky="n")

        self.desc_prec = ctk.CTkLabel(self.card_precision, text="Ajusta la cantidad de decimales en los resultados numéricos.", 
                                      font=ctk.CTkFont(size=12), text_color=theme["subtext"], wraplength=300)
        self.desc_prec.grid(row=2, column=0, pady=(0, 15), sticky="n")

        self.precision_var = ctk.IntVar(value=4)
        self.precision_slider = ctk.CTkSlider(self.card_precision, from_=1, to=10, variable=self.precision_var, 
                                              fg_color=theme["button"], button_color=theme["text"], button_hover_color=theme["subtext"],
                                              command=self.actualizar_precision_label)
        self.precision_slider.grid(row=3, column=0, pady=(0, 5), padx=20, sticky="ew")

        self.precision_label = ctk.CTkLabel(self.card_precision, text=f"Decimales: {self.precision_var.get()}", 
                                            font=ctk.CTkFont(size=12), text_color=theme["subtext"])
        self.precision_label.grid(row=4, column=0, pady=(0, 20), sticky="n")

        # Tarjeta 3: Idioma
        self.card_idioma = ctk.CTkFrame(self.scrollable_frame, fg_color=theme["frame"], corner_radius=15, border_width=1, border_color=theme["button"])
        self.card_idioma.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.card_idioma.grid_columnconfigure(0, weight=1)

        self.icon_idioma = ctk.CTkLabel(self.card_idioma, text="🌍", font=ctk.CTkFont(size=48))
        self.icon_idioma.grid(row=0, column=0, pady=(20, 10), sticky="n")

        self.label_idioma = ctk.CTkLabel(self.card_idioma, text="Idioma de la Interfaz", font=ctk.CTkFont(size=18, weight="bold"), text_color=theme["text"])
        self.label_idioma.grid(row=1, column=0, pady=(0, 5), sticky="n")

        self.desc_idioma = ctk.CTkLabel(self.card_idioma, text="Elige el idioma para los textos y mensajes de la aplicación.", 
                                        font=ctk.CTkFont(size=12), text_color=theme["subtext"], wraplength=300)
        self.desc_idioma.grid(row=2, column=0, pady=(0, 15), sticky="n")

        self.idioma_var = ctk.StringVar(value="Español")
        self.idioma_menu = ctk.CTkOptionMenu(self.card_idioma, values=["Español", "Inglés", "Francés"], variable=self.idioma_var, 
                                             fg_color=theme["button"], button_color=theme["button"], button_hover_color=theme["text"],
                                             command=self.aplicar_idioma_auto)
        self.idioma_menu.grid(row=3, column=0, pady=(0, 20), padx=20, sticky="ew")

        # Tarjeta 4: Notificaciones
        self.card_notif = ctk.CTkFrame(self.scrollable_frame, fg_color=theme["frame"], corner_radius=15, border_width=1, border_color=theme["button"])
        self.card_notif.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.card_notif.grid_columnconfigure(0, weight=1)

        self.icon_notif = ctk.CTkLabel(self.card_notif, text="🔔", font=ctk.CTkFont(size=48))
        self.icon_notif.grid(row=0, column=0, pady=(20, 10), sticky="n")

        self.label_notif = ctk.CTkLabel(self.card_notif, text="Notificaciones", font=ctk.CTkFont(size=18, weight="bold"), text_color=theme["text"])
        self.label_notif.grid(row=1, column=0, pady=(0, 5), sticky="n")

        self.desc_notif = ctk.CTkLabel(self.card_notif, text="Controla si deseas recibir alertas y notificaciones del sistema.", 
                                       font=ctk.CTkFont(size=12), text_color=theme["subtext"], wraplength=300)
        self.desc_notif.grid(row=2, column=0, pady=(0, 15), sticky="n")

        self.notif_var = ctk.BooleanVar(value=True)
        self.notif_switch = ctk.CTkSwitch(self.card_notif, text="Habilitar Notificaciones", variable=self.notif_var, 
                                          fg_color=theme["button"], button_color=theme["text"], button_hover_color=theme["subtext"],
                                          command=self.guardar_notificaciones_auto)
        self.notif_switch.grid(row=3, column=0, pady=(0, 20), padx=20, sticky="w")

        # Footer: Botones globales
        self.footer_frame = ctk.CTkFrame(self.parent, fg_color=theme["bg"], corner_radius=0)
        self.footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        self.footer_frame.grid_columnconfigure(0, weight=1)
        self.footer_frame.grid_columnconfigure(1, weight=0)
        self.footer_frame.grid_columnconfigure(2, weight=0)

        self.footer_label = ctk.CTkLabel(self.footer_frame, text="Versión 1.0 | Cambios aplicados automáticamente", 
                                         font=ctk.CTkFont(size=10), text_color=theme["subtext"])
        self.footer_label.grid(row=0, column=0, pady=10, sticky="w")

        self.btn_restore = ctk.CTkButton(self.footer_frame, text="Restaurar Predeterminados", fg_color=theme["button"], 
                                         command=self.restaurar_predeterminados)
        self.btn_restore.grid(row=0, column=1, padx=(10, 5), pady=10)

        self.btn_save_all = ctk.CTkButton(self.footer_frame, text="Guardar Todo", fg_color=theme["button"], 
                                          command=self.guardar_todo)
        self.btn_save_all.grid(row=0, column=2, padx=(5, 0), pady=10)

    def update_theme(self, colors):
        """Actualiza los colores de todos los widgets en este frame según el tema actual."""
        theme = colors  # 'colors' es el diccionario pasado desde MainApp
        
        # Parent
        self.parent.configure(fg_color=theme["bg"])
        
        # Header
        self.header_frame.configure(fg_color=theme["bg"])
        self.title.configure(text_color=theme["text"])
        self.desc.configure(text_color=theme["subtext"])
        
        # Scrollable frame
        self.scrollable_frame.configure(fg_color=theme["bg"])
        
        # Tarjeta Tema
        self.card_tema.configure(fg_color=theme["frame"], border_color=theme["button"])
        self.label_tema.configure(text_color=theme["text"])
        self.desc_tema.configure(text_color=theme["subtext"])
        self.tema_menu.configure(fg_color=theme["button"], button_color=theme["button"], button_hover_color=theme["text"])
        
        # Tarjeta Precisión
        self.card_precision.configure(fg_color=theme["frame"], border_color=theme["button"])
        self.label_prec.configure(text_color=theme["text"])
        self.desc_prec.configure(text_color=theme["subtext"])
        self.precision_slider.configure(fg_color=theme["button"], button_color=theme["text"], button_hover_color=theme["subtext"])
        self.precision_label.configure(text_color=theme["subtext"])
        
        # Tarjeta Idioma
        self.card_idioma.configure(fg_color=theme["frame"], border_color=theme["button"])
        self.label_idioma.configure(text_color=theme["text"])
        self.desc_idioma.configure(text_color=theme["subtext"])
        self.idioma_menu.configure(fg_color=theme["button"], button_color=theme["button"], button_hover_color=theme["text"])
        
        # Tarjeta Notificaciones
        self.card_notif.configure(fg_color=theme["frame"], border_color=theme["button"])
        self.label_notif.configure(text_color=theme["text"])
        self.desc_notif.configure(text_color=theme["subtext"])
        self.notif_switch.configure(fg_color=theme["button"], button_color=theme["text"], button_hover_color=theme["subtext"])
        
        # Footer
        self.footer_frame.configure(fg_color=theme["bg"])
        self.footer_label.configure(text_color=theme["subtext"])
        self.btn_restore.configure(fg_color=theme["button"])
        self.btn_save_all.configure(fg_color=theme["button"])

    def aplicar_tema_auto(self, value):
        self.current_theme = value
        tema_map = {"Claro": "light", "Neutro": "system", "Oscuro": "dark"}
        modo = tema_map.get(value, "system")
        ctk.set_appearance_mode(modo)
        self.update_theme(themes[self.current_theme])  # Actualiza localmente
        self.apply_settings_callback({"tema": themes[self.current_theme]})

    def actualizar_precision_label(self, value):
        self.precision_label.configure(text=f"Decimales: {int(value)}")
        self.apply_settings_callback({"precision": int(value)})

    def aplicar_idioma_auto(self, value):
        self.apply_settings_callback({"idioma": value})

    def guardar_notificaciones_auto(self):
        notif = self.notif_var.get()
        self.apply_settings_callback({"notificaciones": notif})

    def restaurar_predeterminados(self):
        # Restaurar valores por defecto
        self.tema_var.set("Oscuro")
        self.aplicar_tema_auto("Oscuro")
        self.precision_var.set(4)
        self.actualizar_precision_label(4)
        self.idioma_var.set("Español")
        self.aplicar_idioma_auto("Español")
        self.notif_var.set(True)
        self.guardar_notificaciones_auto()

    def guardar_todo(self):
        # Forzar guardar todos los valores actuales
        self.apply_settings_callback({
            "tema": themes[self.tema_var.get()],
            "precision": self.precision_var.get(),
            "idioma": self.idioma_var.get(),
            "notificaciones": self.notif_var.get()
        })
