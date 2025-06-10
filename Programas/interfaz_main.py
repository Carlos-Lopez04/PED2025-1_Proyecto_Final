from tkinter import *  # Para la interfaz gráfica
from tkinter import font, messagebox  # Para manejar fuentes y ventanas emergentes
from time import strftime  # Para obtener la hora actual
import webbrowser  # Para abrir enlaces en el navegador
import subprocess  # Para ejecutar otros programas
import sys  # Para manejar funciones del sistema
from webscraping import hacer_scraping, crear_bd_y_cargar 

# COLORES
COLOR_FONDO = "#0a1a2f"  # Color oscuro para el fondo principal
COLOR_PRIMARIO = "#14213d"  # Color primario para botones y cabecera
COLOR_SECUNDARIO = "#1e3a8a"  # Color secundario para botones
COLOR_TERCIARIO = "#1e40af"  # Color terciario para botones
COLOR_ACENTO = "#1e3a8a"  # Color de resalte para bordes
COLOR_PELIGRO = "#7f1d1d"  # Color rojo para botones de advertencia (ej. Salir)
COLOR_TEXTO = "#e2e8f0"  # Color de texto normal
COLOR_TEXTO_CLARO = "#ffffff"  # Color de texto blanco
COLOR_BORDE = "#1e293b"  # Color para bordes de frames

#* FUNCIÓN PARA CREAR BOTONES CON EFECTO HOVER
def crear_boton(parent, text, command, color, hover_color):
    # Configuración básica del botón (texto, color, fuente, etc.)
    btn = Button(parent,
                text=text,
                command=command,  # Función que se ejecuta al hacer clic
                bg=color,  # Color de fondo
                fg=COLOR_TEXTO_CLARO,  # Color del texto (blanco)
                activebackground=hover_color,  # Color al hacer clic
                activeforeground=COLOR_TEXTO_CLARO,  # Color del texto al hacer clic
                font=fuente_botones,  # Fuente definida más adelante
                borderwidth=0,  # Sin borde
                padx=20,  # Espaciado horizontal
                pady=10,  # Espaciado vertical
                relief=FLAT)  # Estilo plano (sin relieve)

    # Función para cambiar el color cuando el mouse entra en el botón
    def on_enter(e):
        e.widget['bg'] = hover_color  # Cambia al color de hover

    # Función para restaurar el color cuando el mouse sale del botón
    def on_leave(e):
        e.widget['bg'] = color  # Vuelve al color original

    # Asigna las funciones a los eventos del mouse
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return btn  # Devuelve el botón configurado

# FUNCIONES PRINCIPALES
# Abre un dashboard ejecutando un script externo (dashboards.py)
def abrir_dashboard():
    try:
        # Ejecuta el script dashboards.py en un proceso separado
        subprocess.Popen([sys.executable, "dashboards.py"])
    except Exception as e:
        # Muestra un mensaje de error si falla
        messagebox.showerror("Error", f"No se pudo abrir el dashboard:\n{e}")

# Abre el sitio web de TMDB en el navegador predeterminado
def abrir_ayuda():
    webbrowser.open("https://www.themoviedb.org/")
    
# Actualiza la hora en la barra de estado cada segundo
def actualizar_hora():
    hora_actual = strftime('%H:%M:%S')  # Obtiene la hora actual
    label_hora.config(text=f"🕒 {hora_actual}")  # Actualiza el texto del label
    label_hora.after(1000, actualizar_hora)  # Programa la próxima actualización en 1 segundo

#* CONFIGURACIÓN DE LA VENTANA PRINCIPAL
root = Tk()  # Crea la ventana principal
root.title("TMDB Data Manager - Interactive Edition")  # Título de la ventana
root.geometry("650x550")  # Tamaño inicial (ancho x alto)
root.resizable(True, True)  # Permite redimensionar la ventana
root.configure(bg=COLOR_FONDO)  # Color de fondo

# DEFINICIÓN DE FUENTES
try:
    # Intenta usar fuentes específicas (Helvetica y Arial)
    fuente_titulo = font.Font(family="Helvetica", size=20, weight="bold")
    fuente_subtitulo = font.Font(family="Helvetica", size=12, slant="italic")
    fuente_botones = font.Font(family="Arial", size=12, weight="bold")
    fuente_texto = font.Font(family="Arial", size=10)
except:
    # Si falla, usa fuentes genéricas con los mismos estilos
    fuente_titulo = font.Font(size=20, weight="bold")
    fuente_subtitulo = font.Font(size=12, slant="italic")
    fuente_botones = font.Font(size=12, weight="bold")
    fuente_texto = font.Font(size=10)

#* ESTRUCTURA PRINCIPAL
# Frame principal que contiene todo el contenido
main_frame = Frame(root, bg=COLOR_FONDO, padx=30, pady=20)
main_frame.pack(fill=BOTH, expand=True)

# Encabezado
header_frame = Frame(main_frame, bg=COLOR_PRIMARIO, height=100,
                    highlightbackground=COLOR_ACENTO, highlightthickness=3)
header_frame.pack(fill=X, pady=(0, 20))

# Título principal
label_title = Label(header_frame,
                    text="TMDB Data Manager",
                    font=fuente_titulo,
                    bg=COLOR_PRIMARIO,
                    fg=COLOR_TEXTO_CLARO,
                    padx=20)
label_title.pack(side=LEFT, fill=Y)

#* Subtítulo
label_subtitle = Label(header_frame,
                    text="Interactive Professional Edition",
                    font=fuente_subtitulo,
                    bg=COLOR_PRIMARIO,
                    fg="#e9ecef",
                    padx=20)
label_subtitle.pack(side=LEFT, fill=Y)

#* BOTONES DEL CONTENIDO PRINCIPAL
content_frame = Frame(main_frame,
                    bg="#0a1a2f",
                    highlightbackground=COLOR_BORDE,
                    highlightthickness=1,
                    padx=30,
                    pady=30,
                    relief=RAISED)
content_frame.pack(fill=BOTH, expand=True)

# Botón para hacer web scraping 
btn_scraping = crear_boton(content_frame,
                        "📊 Obtener Datos de TMDB",
                        hacer_scraping,
                        COLOR_SECUNDARIO,
                        "#172554")
btn_scraping.pack(fill=X, pady=10, ipady=5)

# Botón para crear la base de datos
btn_bd = crear_boton(content_frame,
                    "💾 Crear Base de Datos",
                    crear_bd_y_cargar,
                    COLOR_TERCIARIO,
                    "#1a365d")
btn_bd.pack(fill=X, pady=10, ipady=5)

# Botón para abrir el dashboard interactivo
btn_dashboard = crear_boton(
    content_frame,
    "📈 Ver Dashboard Interactivo",
    abrir_dashboard,
    "#4c1d95",  # Color morado
    "#5b21b6"   # Color hover
)
btn_dashboard.pack(fill=X, pady=10, ipady=5)

# Botón de ayuda (abre el sitio web de TMDB)
btn_ayuda = crear_boton(content_frame,
                    "❓ Ayuda y Documentación",
                    abrir_ayuda,
                    COLOR_PRIMARIO,
                    "#0f172a")
btn_ayuda.pack(fill=X, pady=10, ipady=5)

# Botón para salir de la aplicación
btn_salir = crear_boton(content_frame,
                    "🚪 Salir de la Aplicación",
                    root.destroy,  # Cierra la ventana principal
                    COLOR_PELIGRO,
                    "#63171b")
btn_salir.pack(fill=X, pady=10, ipady=5)

#* BARRA DE ESTADO (INFERIOR)
status_frame = Frame(main_frame, bg=COLOR_PRIMARIO, height=40)
status_frame.pack(fill=X, side=BOTTOM)

#* Label que muestra la hora actual (se actualiza cada segundo)
label_hora = Label(status_frame,
                text="🕒 ",
                bg=COLOR_PRIMARIO,
                fg=COLOR_TEXTO_CLARO,
                font=fuente_texto)
label_hora.pack(side=RIGHT, padx=20)
actualizar_hora()  # Inicia la actualización de la hora

#* Label con información de copyright/versión
label_version = Label(status_frame,
                    text="UABC/FCA-LIN © 2025",
                    bg=COLOR_PRIMARIO,
                    fg="#e9ecef",
                    font=fuente_texto)
label_version.pack(side=LEFT, padx=20)


root.eval('tk::PlaceWindow . center')  # Centra la ventana en la pantalla
root.mainloop()  # Inicia el bucle principal de la interfaz