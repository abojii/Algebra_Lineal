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
