from tkinter import *
from tkinter import font, messagebox
from time import strftime
import webbrowser
import subprocess
import sys
from scraping_tmdb import hacer_scraping, crear_bd_y_cargar

# Paleta de colores futuristas
COLOR_FONDO = "#0F0F1B"
COLOR_PRIMARIO = "#1A1A2E"
COLOR_SECUNDARIO = "#4ECDC4"
COLOR_TERCIARIO = "#FF6B6B"
COLOR_ACENTO = "#6B5B95"
COLOR_TEXTO = "#E2F3F5"
COLOR_HOVER = "#3D7EA6"

root = Tk()
root.title("TMDB Manager - Neon Edition")
root.geometry("700x600")
root.configure(bg=COLOR_FONDO)

try:
    fuente_titulo = font.Font(family="Orbitron", size=22, weight="bold")
    fuente_botones = font.Font(family="Rajdhani", size=14, weight="bold")
    fuente_texto = font.Font(family="Exo 2", size=10)
except:
    fuente_titulo = font.Font(family="Impact", size=22, weight="bold")
    fuente_botones = font.Font(family="Arial Narrow", size=14, weight="bold")
    fuente_texto = font.Font(family="Verdana", size=10)

def crear_boton(parent, text, command, bg_color):
    btn = Button(parent, text=text, command=command,
                bg=bg_color, fg=COLOR_TEXTO, activebackground=COLOR_HOVER,
                font=fuente_botones, borderwidth=0, padx=25, pady=12)
    btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
    return btn

def actualizar_hora():
    label_hora.config(text=strftime('⏱ %H:%M:%S'))
    label_hora.after(1000, actualizar_hora)

main_frame = Frame(root, bg=COLOR_FONDO, padx=40, pady=30)
main_frame.pack(fill=BOTH, expand=True)

header = Frame(main_frame, bg=COLOR_PRIMARIO, pady=15)
header.pack(fill=X)

Label(header, text="TMDB NEON", font=fuente_titulo,
      bg=COLOR_PRIMARIO, fg=COLOR_SECUNDARIO).pack(side=LEFT, padx=20)

content = Frame(main_frame, bg=COLOR_FONDO)
content.pack(fill=BOTH, expand=True, pady=20)

btn_scraping = crear_boton(content, "🌀 OBTENER DATOS", hacer_scraping, COLOR_ACENTO)
btn_scraping.pack(fill=X, pady=8)

btn_bd = crear_boton(content, "💾 CREAR BASE", crear_bd_y_cargar, "#5E548E")
btn_bd.pack(fill=X, pady=8)

btn_dashboard = crear_boton(content, "📊 VER DASHBOARD", lambda: subprocess.Popen([sys.executable, "tmdb_dashboard.py"]), "#3A86FF")
btn_dashboard.pack(fill=X, pady=8)

btn_ayuda = crear_boton(content, "❔ AYUDA", lambda: webbrowser.open("https://www.themoviedb.org/"), "#8338EC")
btn_ayuda.pack(fill=X, pady=8)

btn_salir = crear_boton(content, "⏻ SALIR", root.destroy, COLOR_TERCIARIO)
btn_salir.pack(fill=X, pady=8)

footer = Frame(main_frame, bg=COLOR_PRIMARIO, pady=10)
footer.pack(fill=X, side=BOTTOM)

label_hora = Label(footer, text="", bg=COLOR_PRIMARIO, fg=COLOR_SECUNDARIO, font=fuente_texto)
label_hora.pack(side=RIGHT, padx=20)

Label(footer, text="NEON EDITION © 2025", bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, font=fuente_texto).pack(side=LEFT, padx=20)

actualizar_hora()
root.eval('tk::PlaceWindow . center')
root.mainloop()
