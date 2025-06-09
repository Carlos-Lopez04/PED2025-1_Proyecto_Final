from tkinter import *
from tkinter import ttk, messagebox, font
from time import strftime
import webbrowser
import subprocess
import sys
from scraping_tmdb import hacer_scraping, crear_bd_y_cargar

COLOR_FONDO = "#121212"
COLOR_PRIMARIO = "#1E1E1E"
COLOR_SECUNDARIO = "#BB86FC"
COLOR_TERCIARIO = "#03DAC6"
COLOR_ACENTO = "#3700B3"
COLOR_PELIGRO = "#CF6679"
COLOR_TEXTO = "#E1E1E1"
COLOR_TEXTO_CLARO = "#FFFFFF"
COLOR_BORDE = "#2E2E2E"

def crear_boton(parent, text, command, color, hover_color):
    btn = Button(parent,
                 text=text,
                 command=command,
                 bg=color,
                 fg=COLOR_TEXTO_CLARO,
                 activebackground=hover_color,
                 activeforeground=COLOR_TEXTO_CLARO,
                 font=fuente_botones,
                 borderwidth=0,
                 padx=20,
                 pady=10,
                 relief=FLAT)

    def on_enter(e):
        e.widget['bg'] = hover_color

    def on_leave(e):
        e.widget['bg'] = color

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return btn

def abrir_dashboard():
    try:
        subprocess.Popen([sys.executable, "tmdb_dashboard.py"])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el dashboard:\n{e}")

def abrir_ayuda():
    webbrowser.open("https://www.themoviedb.org/")

def actualizar_hora():
    hora_actual = strftime('%H:%M:%S')
    label_hora.config(text=f"🕒 {hora_actual}")
    label_hora.after(1000, actualizar_hora)

root = Tk()
root.title("TMDB Data Manager - Interactive Edition")
root.geometry("650x550")
root.resizable(True, True)
root.configure(bg=COLOR_FONDO)

try:
    fuente_titulo = font.Font(family="Montserrat", size=20, weight="bold")
    fuente_subtitulo = font.Font(family="Open Sans", size=12, slant="italic")
    fuente_botones = font.Font(family="Roboto", size=12, weight="bold")
    fuente_texto = font.Font(family="Roboto", size=10)
except:
    fuente_titulo = font.Font(family="Helvetica", size=20, weight="bold")
    fuente_subtitulo = font.Font(family="Tahoma", size=12, slant="italic")
    fuente_botones = font.Font(family="Arial", size=12, weight="bold")
    fuente_texto = font.Font(family="Arial", size=10)

main_frame = Frame(root, bg=COLOR_FONDO, padx=30, pady=20)
main_frame.pack(fill=BOTH, expand=True)

header_frame = Frame(main_frame, bg=COLOR_PRIMARIO, height=100,
                     highlightbackground=COLOR_ACENTO, highlightthickness=3)
header_frame.pack(fill=X, pady=(0, 20))

label_title = Label(header_frame,
                    text="TMDB Data Manager",
                    font=fuente_titulo,
                    bg=COLOR_PRIMARIO,
                    fg=COLOR_SECUNDARIO,
                    padx=20)
label_title.pack(side=LEFT, fill=Y)

label_subtitle = Label(header_frame,
                       text="Interactive Professional Edition",
                       font=fuente_subtitulo,
                       bg=COLOR_PRIMARIO,
                       fg=COLOR_TERCIARIO,
                       padx=20)
label_subtitle.pack(side=LEFT, fill=Y)

content_frame = Frame(main_frame,
                      bg=COLOR_FONDO,
                      highlightbackground=COLOR_BORDE,
                      highlightthickness=1,
                      padx=30,
                      pady=30,
                      relief=FLAT)
content_frame.pack(fill=BOTH, expand=True)

btn_scraping = crear_boton(content_frame,
                          "📊 Obtener Datos de TMDB",
                          hacer_scraping,
                          COLOR_ACENTO,
                          "#6200EE")
btn_scraping.pack(fill=X, pady=10, ipady=5)

btn_bd = crear_boton(content_frame,
                    "💾 Crear Base de Datos",
                    crear_bd_y_cargar,
                    COLOR_SECUNDARIO,
                    "#9A67EA")
btn_bd.pack(fill=X, pady=10, ipady=5)

btn_dashboard = crear_boton(content_frame,
                          "📈 Ver Dashboard Interactivo",
                          abrir_dashboard,
                          COLOR_TERCIARIO,
                          "#66FFF9")
btn_dashboard.pack(fill=X, pady=10, ipady=5)

btn_ayuda = crear_boton(content_frame,
                       "❓ Ayuda y Documentación",
                       abrir_ayuda,
                       COLOR_PRIMARIO,
                      "#424242")
btn_ayuda.pack(fill=X, pady=10, ipady=5)

btn_salir = crear_boton(content_frame,
                       "🚪 Salir de la Aplicación",
                       root.destroy,
                       COLOR_PELIGRO,
                      "#FF8A8A")
btn_salir.pack(fill=X, pady=10, ipady=5)

status_frame = Frame(main_frame, bg=COLOR_PRIMARIO, height=40)
status_frame.pack(fill=X, side=BOTTOM)

label_hora = Label(status_frame,
                   text="🕒 ",
                   bg=COLOR_PRIMARIO,
                   fg=COLOR_TERCIARIO,
                   font=fuente_texto)
label_hora.pack(side=RIGHT, padx=20)
actualizar_hora()

label_version = Label(status_frame,
                      text="UABC/FCA-LIN © 2025",
                      bg=COLOR_PRIMARIO,
                      fg=COLOR_TEXTO,
                      font=fuente_texto)
label_version.pack(side=LEFT, padx=20)

root.eval('tk::PlaceWindow . center')

root.mainloop()
