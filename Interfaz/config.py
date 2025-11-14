import customtkinter as ctk
from Interfaz.constantes import COLOR_FRAME

def open_config_window(self):
    # Crear ventana emergente
    config_window = ctk.CTkToplevel(self)
    config_window.title("Configuración")
    config_window.geometry("400x500")  # Ajusta tamaño según contenido
    config_window.resizable(False, False)
    config_window.transient(self)  # Hace que sea dependiente de la ventana principal
    config_window.grab_set()  # Bloquea interacción con la principal hasta cerrar (opcional, quítalo si quieres no modal)

    # Título
    title_label = ctk.CTkLabel(config_window, text="Configuración de la App", font=ctk.CTkFont(size=16, weight="bold"))
    title_label.pack(pady=10)

    # Opción 1: Cambiar Tema
    theme_frame = ctk.CTkFrame(config_window, fg_color=COLOR_FRAME)
    theme_frame.pack(fill="x", padx=20, pady=5)
    ctk.CTkLabel(theme_frame, text="Tema:").pack(side="left", padx=10)
    theme_switch = ctk.CTkSwitch(theme_frame, text="Modo Oscuro", command=self.toggle_theme)
    theme_switch.pack(side="right", padx=10)
    # Configura el switch según el tema actual
    current_mode = ctk.get_appearance_mode()
    theme_switch.select() if current_mode == "dark" else theme_switch.deselect()

    # Opción 2: Personalizar Color de Fondo (ejemplo simple con slider para un componente RGB)
    color_frame = ctk.CTkFrame(config_window, fg_color=COLOR_FRAME)
    color_frame.pack(fill="x", padx=20, pady=5)
    ctk.CTkLabel(color_frame, text="Color de Fondo (Rojo):").pack(pady=5)
    color_slider = ctk.CTkSlider(color_frame, from_=0, to=255, command=self.update_bg_color)
    color_slider.pack(pady=5)
    # Nota: Para RGB completo, agrega más sliders y combina valores.

    # Opción 3: Tamaño de Fuente
    font_frame = ctk.CTkFrame(config_window, fg_color=COLOR_FRAME)
    font_frame.pack(fill="x", padx=20, pady=5)
    ctk.CTkLabel(font_frame, text="Tamaño de Fuente:").pack(pady=5)
    font_slider = ctk.CTkSlider(font_frame, from_=10, to=20, command=self.update_font_size)
    font_slider.pack(pady=5)

    # Botones de Acción
    buttons_frame = ctk.CTkFrame(config_window, fg_color="transparent")
    buttons_frame.pack(fill="x", padx=20, pady=20)
    save_btn = ctk.CTkButton(buttons_frame, text="Guardar", command=self.save_config)
    save_btn.pack(side="left", padx=5)
    reset_btn = ctk.CTkButton(buttons_frame, text="Resetear", fg_color="orange", command=self.reset_config)
    reset_btn.pack(side="left", padx=5)
    close_btn = ctk.CTkButton(buttons_frame, text="Cerrar", fg_color="red", command=config_window.destroy)
    close_btn.pack(side="right", padx=5)
    

#Ventana de ayuda
def open_help_window(self):
    help_window = ctk.CTkToplevel(self)
    help_window.title("Ayuda")
    help_window.geometry("500x400")
    help_window.resizable(False, False)
    help_window.transient(self)

    title_label = ctk.CTkLabel(help_window, text="Ayuda - Calculadora de Álgebra Lineal", font=ctk.CTkFont(size=16, weight="bold"))
    title_label.pack(pady=10)

    # Contenido scrollable
    scrollable_frame = ctk.CTkScrollableFrame(help_window, width=450, height=300)
    scrollable_frame.pack(padx=20, pady=10)

    # Texto de ayuda (ejemplo; personalízalo)
    help_text = """
    Bienvenido a la Calculadora de Álgebra Lineal.

    - Menu: Vista principal.
    - Matrices: Operaciones como suma, multiplicación, inversa, etc.
    - Vectores: Cálculos con vectores, ecuaciones, etc.
    - Errores: Revisa logs de errores.

    Para usar: Selecciona una sección y sigue los submenús.

    Preguntas frecuentes:
    - ¿Cómo resolver una matriz? Ve a Matrices > Solucion Matrices.
    - Contacto: soporte@tuapp.com
    """
    help_label = ctk.CTkLabel(scrollable_frame, text=help_text, wraplength=400, justify="left")
    help_label.pack(pady=10)

    close_btn = ctk.CTkButton(help_window, text="Cerrar", command=help_window.destroy)
    close_btn.pack(pady=10)