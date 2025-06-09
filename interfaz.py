from tkinter import *
from tkinter import font, messagebox
from time import strftime
import webbrowser
import subprocess
import sys
from webscraping import hacer_scraping, crear_bd_y_cargar

# Colores para el fondo de cada uno de los botones que tiene nuestro menu
COLOR_FONDO = "#0a1a2f"
COLOR_PRIMARIO = "#14213d"
COLOR_SECUNDARIO = "#1e3a8a"
COLOR_TERCIARIO = "#1e40af"
COLOR_ACENTO = "#1e3a8a"
COLOR_PELIGRO = "#7f1d1d" 
COLOR_TEXTO = "#e2e8f0"
COLOR_TEXTO_CLARO = "#ffffff"
COLOR_BORDE = "#1e293b"

#Funcion para crear botones
def crear_boton(parent, text, command, color, hover_color):
    """Los botones tendran efecto Hover"""
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

#Abrir el dashboard. Este proceso tardara unos segundos, hasta que en consola se
#muestre una IP, al hacer click en ella se abrira el navegador web preferente de la computadora utilizada
def abrir_dashboard():
    """Ejecuta el dashboard como un proceso separado"""
    try:
        subprocess.Popen([sys.executable, "tmdb_dashboard.py"])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el dashboard:\n{e}")

def abrir_ayuda():
    """Abre el sitio web de TMDB"""
    webbrowser.open("https://www.themoviedb.org/")
    
def actualizar_hora():
    """Actualiza la hora en la barra de estado"""
    hora_actual = strftime('%H:%M:%S')
    label_hora.config(text=f"🕒 {hora_actual}")
    label_hora.after(1000, actualizar_hora)

# Configuración de la ventana principal
root = Tk()
root.title("TMDB Data Manager - Interactive Edition")
root.geometry("650x550")
root.resizable(True, True)
root.configure(bg=COLOR_FONDO)

# Fuentes utilizadas para el texto que contienen nuestros botones
try:
    fuente_titulo = font.Font(family="Helvetica", size=20, weight="bold")
    fuente_subtitulo = font.Font(family="Helvetica", size=12, slant="italic")
    fuente_botones = font.Font(family="Arial", size=12, weight="bold")
    fuente_texto = font.Font(family="Arial", size=10)
except:
    fuente_titulo = font.Font(size=20, weight="bold")
    fuente_subtitulo = font.Font(size=12, slant="italic")
    fuente_botones = font.Font(size=12, weight="bold")
    fuente_texto = font.Font(size=10)

main_frame = Frame(root, bg=COLOR_FONDO, padx=30, pady=20)
main_frame.pack(fill=BOTH, expand=True)

# Encabezado
header_frame = Frame(main_frame, bg=COLOR_PRIMARIO, height=100,
                    highlightbackground=COLOR_ACENTO, highlightthickness=3)
header_frame.pack(fill=X, pady=(0, 20))

label_title = Label(header_frame,
                    text="TMDB Data Manager",
                    font=fuente_titulo,
                    bg=COLOR_PRIMARIO,
                    fg=COLOR_TEXTO_CLARO,
                    padx=20)
label_title.pack(side=LEFT, fill=Y)

label_subtitle = Label(header_frame,
                    text="Interactive Professional Edition",
                    font=fuente_subtitulo,
                    bg=COLOR_PRIMARIO,
                    fg="#e9ecef",
                    padx=20)
label_subtitle.pack(side=LEFT, fill=Y)

# Frame de contenido
content_frame = Frame(main_frame,
                    bg="#0a1a2f",
                    highlightbackground=COLOR_BORDE,
                    highlightthickness=1,
                    padx=30,
                    pady=30,
                    relief=RAISED)
content_frame.pack(fill=BOTH, expand=True)

# Botones funcionales
btn_scraping = crear_boton(content_frame,
                        "📊 Obtener Datos de TMDB",
                        hacer_scraping,
                        COLOR_SECUNDARIO,
                        "#172554")
btn_scraping.pack(fill=X, pady=10, ipady=5)

btn_bd = crear_boton(content_frame,
                    "💾 Crear Base de Datos",
                    crear_bd_y_cargar,
                    COLOR_TERCIARIO,
                    "#1a365d")
btn_bd.pack(fill=X, pady=10, ipady=5)

btn_dashboard = crear_boton(
    content_frame,
    "📈 Ver Dashboard Interactivo",
    abrir_dashboard,
    "#4c1d95",  # Color morado
    "#5b21b6"   # Color hover
)
btn_dashboard.pack(fill=X, pady=10, ipady=5)

btn_ayuda = crear_boton(content_frame,
                    "❓ Ayuda y Documentación",
                    abrir_ayuda,
                    COLOR_PRIMARIO,
                    "#0f172a")
btn_ayuda.pack(fill=X, pady=10, ipady=5)

btn_salir = crear_boton(content_frame,
                    "🚪 Salir de la Aplicación",
                    root.destroy,
                    COLOR_PELIGRO,
                    "#63171b")
btn_salir.pack(fill=X, pady=10, ipady=5)

# Barra de estado
status_frame = Frame(main_frame, bg=COLOR_PRIMARIO, height=40)
status_frame.pack(fill=X, side=BOTTOM)

label_hora = Label(status_frame,
                text="🕒 ",
                bg=COLOR_PRIMARIO,
                fg=COLOR_TEXTO_CLARO,
                font=fuente_texto)
label_hora.pack(side=RIGHT, padx=20)
actualizar_hora()

label_version = Label(status_frame,
                    text="UABC/FCA-LIN © 2025",
                    bg=COLOR_PRIMARIO,
                    fg="#e9ecef",
                    font=fuente_texto)
label_version.pack(side=LEFT, padx=20)

# Centrar la ventana
root.eval('tk::PlaceWindow . center')

root.mainloop()