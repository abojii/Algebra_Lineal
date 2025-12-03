import customtkinter as ctk
import os
import sys

# Configurar CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Colores
COLOR_BG = "#1e1e2f"
COLOR_FRAME = "#2b2b40"
COLOR_TEXT = "#ffffff"
COLOR_SUBTEXT = "#bbbbbb"
COLOR_BUTTON = "#3b82f6"
COLOR_ENTRY = "#3a3a4f"

# Configurar sys.path (para imports de Interfaz)
project_root = os.path.dirname(os.path.dirname(__file__))  # Asume que config.py está en la raíz
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'Interfaz'))

themes = {
    "Oscuro": {
        "bg": "#1e1e2f",
        "frame": "#2b2b40",
        "text": "#ffffff",
        "subtext": "#bbbbbb",
        "button": "#3b82f6",
        "entry": "#3a3a4f",
        # Nuevos para sidebar
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
        # Nuevos para sidebar (ajustados para tema claro)
        "sidebar_bg": "#e0e0e0",  # Gris claro para fondo
        "sidebar_hover": "#cccccc",  # Gris más claro para hover
        "sidebar_active": "#0056b3",  # Azul más oscuro para activo
        "sidebar_text": "#000000",  # Negro para texto
        "sidebar_subtext": "#555555",  # Gris oscuro para subtexto
        "sidebar_separator": "#aaaaaa"  # Gris medio para separador
    },
    "Neutro": {
        "bg": "#f5f5f5",
        "frame": "#e0e0e0",
        "text": "#333333",
        "subtext": "#777777",
        "button": "#6c757d",
        "entry": "#d1ecf1",
        # Nuevos para sidebar (intermedios)
        "sidebar_bg": "#d0d0d0",
        "sidebar_hover": "#b0b0b0",
        "sidebar_active": "#4a90e2",
        "sidebar_text": "#333333",
        "sidebar_subtext": "#666666",
        "sidebar_separator": "#999999"
    }
}