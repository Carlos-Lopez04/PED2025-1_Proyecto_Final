from tkinter import *
from tkinter import font, messagebox
from time import strftime
import webbrowser
import subprocess
import sys
from webscraping import hacer_scraping, crear_bd_y_cargar

# Colores para cada unos de los botones del menu
COLOR_FONDO = "#599dd4"
COLOR_PRIMARIO = "#17476e"
COLOR_SECUNDARIO = "#132073"
COLOR_TERCIARIO = "#5faeee"
COLOR_ACENTO = "#2352b6"
COLOR_TEXTO = "#142e65"
COLOR_HOVER = "#3e6f96"


#Aqui se crea la ventana principal
root = Tk()
root.title("TMDB Manager - Neon Edition")
root.geometry("900x700")
root.configure(bg=COLOR_FONDO)


#Fuentes que se utilizaran para el texto de los botones
try:
    fuente_titulo = font.Font(family="Serif", size=23, weight="bold")
    fuente_botones = font.Font(family="Cursiva", size=16, weight="bold")
    fuente_texto = font.Font(family="Exo 2", size=19)
except:
    fuente_titulo = font.Font(family="Monospace", size=24, weight="bold")
    fuente_botones = font.Font(family="Times", size=18, weight="bold")
    fuente_texto = font.Font(family="Serif", size=20)



def crear_boton(parent, text, command, bg_color):
    btn = Button(parent, text=text, command=command,
                bg=bg_color, fg=COLOR_TEXTO, activebackground=COLOR_HOVER,
                font=fuente_botones, borderwidth=0, padx=45, pady=16)
    btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
    return btn

#Este codigo es para que en el menu se coloque un reloj, que le da un toque distinto a nuestro menu

def actualizar_hora():
    label_hora.config(text=strftime('⏱ %H:%M:%S'))
    label_hora.after(1000, actualizar_hora)

main_frame = Frame(root, bg=COLOR_FONDO, padx=65, pady=45)
main_frame.pack(fill=BOTH, expand=True)

header = Frame(main_frame, bg=COLOR_PRIMARIO, pady=17)
header.pack(fill=X)

Label(header, text="TMDB NEON", font=fuente_titulo,
      bg=COLOR_PRIMARIO, fg=COLOR_SECUNDARIO).pack(side=LEFT, padx=20)

content = Frame(main_frame, bg=COLOR_FONDO)
content.pack(fill=BOTH, expand=True, pady=50)



#Aqui creamos los 5 botones que componen  nuestro menu

btn_scraping = crear_boton(content, "🌀 OBTENER DATOS", hacer_scraping, COLOR_ACENTO)
btn_scraping.pack(fill=X, pady=12)

btn_bd = crear_boton(content, "💾 CREAR BASE", crear_bd_y_cargar, "#1b58bd")
btn_bd.pack(fill=X, pady=12)

btn_dashboard = crear_boton(content, "📊 VER DASHBOARD", lambda: subprocess.Popen([sys.executable, "tmdb_dashboard.py"]), "#0d187a")
btn_dashboard.pack(fill=X, pady=12)

btn_ayuda = crear_boton(content, "❔ AYUDA", lambda: webbrowser.open("https://www.themoviedb.org/"), "#2e3890")
btn_ayuda.pack(fill=X, pady=12)

btn_salir = crear_boton(content, "⏻ SALIR", root.destroy, COLOR_TERCIARIO)
btn_salir.pack(fill=X, pady=12)

footer = Frame(main_frame, bg=COLOR_PRIMARIO, pady=14)
footer.pack(fill=X, side=BOTTOM)

label_hora = Label(footer, text="", bg=COLOR_PRIMARIO, fg=COLOR_SECUNDARIO, font=fuente_texto)
label_hora.pack(side=RIGHT, padx=16)

Label(footer, text="UABC/FCA-LIN © 2025", bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, font=fuente_texto).pack(side=LEFT, padx=30)

actualizar_hora()
root.eval('tk::PlaceWindow . center')
root.mainloop()
