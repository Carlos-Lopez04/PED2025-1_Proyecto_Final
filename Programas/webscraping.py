import requests  # Para usar la API de TMDB
import pandas as pd  # Para manejar datos en tablas
import mysql.connector  # Para conectar con MySQL
from tkinter import messagebox  # Para mostrar mensajes

#* Configuración de la API
API_KEY = "6e9456bdd4ec35e91f83f2cf2950e4c2" 
BASE_URL = "https://api.themoviedb.org/3"

#* Obtiene datos de TMDB
def fetch_tmdb_data(endpoint, pages=5):
    all_results = []  # Lista para Guarda todos los datos
    
    # Obtiene datos de cada página
    for page in range(1, pages + 1):
        params = {"api_key": API_KEY, "page": page}
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        
        # Si la respuesta es correcta, Guarda datos
        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get("results", []))
        else:
            messagebox.showerror("Error", f"Error en página {page}: {response.status_code}")
            break
    
    return all_results

#* Obtiene todos los géneros de películas y series
def fetch_genres():
    try:
        # Obtiene géneros de películas y series
        movie_genres_response = requests.get(f"{BASE_URL}/genre/movie/list", params={"api_key": API_KEY})
        tv_genres_response = requests.get(f"{BASE_URL}/genre/tv/list", params={"api_key": API_KEY})

        # Extrae las listas
        movie_genres = movie_genres_response.json().get("genres", []) if movie_genres_response.status_code == 200 else []
        tv_genres = tv_genres_response.json().get("genres", []) if tv_genres_response.status_code == 200 else []

        # Combina y Elimina duplicados
        all_genres = {}
        for genre in movie_genres + tv_genres:
            all_genres[genre['id']] = genre['name']

        return all_genres
    
    except Exception as e:
        messagebox.showerror("Error", f"Error obteniendo géneros: {e}")
        return {}

#* Convierte los datos al DataFrame
def to_dataframe(data, content_type):
    df = pd.DataFrame(data)
    df["type"] = content_type
    
    # Unifica nombres de columnas
    if content_type == "movie":
        df["title"] = df["title"]
        df["release_date"] = df["release_date"]
    else:
        df["title"] = df["name"]  # Series usan "name"
        df["release_date"] = df["first_air_date"]  # Series usan "first_air_date"

    # Saca el año
    df["release_year"] = pd.to_datetime(df["release_date"], errors='coerce').dt.year

    # Retorna solo las columnas necesarias
    return df[["id", "title", "vote_average", "popularity", "release_date", "release_year", "type", "genre_ids"]]

#* Descarga todos los datos y los guarda en archivos CSV
def hacer_scraping():
    try:
        # Obtiene géneros
        genres_dict = fetch_genres()

        # Obtiene datos de diferentes categorías
        popular_movies = fetch_tmdb_data("/movie/popular")
        top_rated_movies = fetch_tmdb_data("/movie/top_rated")
        popular_series = fetch_tmdb_data("/tv/popular")

        # Convierte a tablas
        df_popular_movies = to_dataframe(popular_movies, "movie")
        df_top_rated_movies = to_dataframe(top_rated_movies, "movie")
        df_popular_series = to_dataframe(popular_series, "tv")

        # Guarda géneros como CSV
        genres_df = pd.DataFrame(list(genres_dict.items()), columns=['genre_id', 'genre_name'])
        genres_df.to_csv("genres.csv", index=False)

        # Guarda todos los CSV
        df_popular_movies.to_csv("popular_movies.csv", index=False)
        df_top_rated_movies.to_csv("top_rated_movies.csv", index=False)
        df_popular_series.to_csv("popular_series.csv", index=False)

        messagebox.showinfo("Scraping OK", "Scraping completado y CSV guardados.")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error durante el scraping:\n{e}")
        return False

#* Crea la base de datos MySQL y carga todos los datos
def crear_bd_y_cargar():
    try:
        #Todo Conexión a la base de datos MySQL (cambiar User, Password y Host)
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="141804"
        )
        cursor = conn.cursor()
        
        # Crea base de datos
        cursor.execute("CREATE DATABASE IF NOT EXISTS tmdb_db")
        conn.database = "tmdb_db"

        # Elimina tablas existentes
        cursor.execute("DROP TABLE IF EXISTS content_genres")
        cursor.execute("DROP TABLE IF EXISTS genres")
        cursor.execute("DROP TABLE IF EXISTS movies_popular")
        cursor.execute("DROP TABLE IF EXISTS tv_popular")
        cursor.execute("DROP TABLE IF EXISTS combined_popular")

        # Crea tabla de géneros
        cursor.execute("""
            CREATE TABLE genres (
                genre_id INT PRIMARY KEY,
                genre_name VARCHAR(100) NOT NULL
            )
        """)

        # Crea tabla de películas populares
        cursor.execute("""
            CREATE TABLE movies_popular (
                id INT PRIMARY KEY,
                title VARCHAR(255),
                vote_average FLOAT,
                popularity FLOAT,
                release_date DATE,
                release_year INT,
                type VARCHAR(10)
            )
        """)

        # Crea tabla de series populares
        cursor.execute("""
            CREATE TABLE tv_popular (
                id INT PRIMARY KEY,
                title VARCHAR(255),
                vote_average FLOAT,
                popularity FLOAT,
                release_date DATE,
                release_year INT,
                type VARCHAR(10)
            )
        """)

        # Crea tabla combinada
        cursor.execute("""
            CREATE TABLE combined_popular (
                id INT PRIMARY KEY,
                title VARCHAR(255),
                vote_average FLOAT,
                popularity FLOAT,
                release_date DATE,
                release_year INT,
                type VARCHAR(10)
            )
        """)

        # Crea tabla de relaciones contenido-géneros
        cursor.execute("""
            CREATE TABLE content_genres (
                id INT AUTO_INCREMENT PRIMARY KEY,
                content_id INT,
                genre_id INT,
                content_type VARCHAR(10),
                FOREIGN KEY (genre_id) REFERENCES genres(genre_id),
                UNIQUE KEY unique_content_genre (content_id, genre_id, content_type)
            )
        """)

        # Carga géneros
        try:
            genres_df = pd.read_csv("genres.csv")
            for _, row in genres_df.iterrows():
                cursor.execute("""
                    INSERT IGNORE INTO genres (genre_id, genre_name)
                    VALUES (%s, %s)
                """, (int(row["genre_id"]), row["genre_name"]))
        
        # Géneros por defecto si no existe el archivo
        except FileNotFoundError:
            print("Archivo genres.csv no encontrado, cargando géneros por defecto")
            default_genres = [
                (28, "Action"), (12, "Adventure"), (16, "Animation"), (35, "Comedy"),
                (80, "Crime"), (99, "Documentary"), (18, "Drama"), (10751, "Family"),
                (14, "Fantasy"), (36, "History"), (27, "Horror"), (10402, "Music"),
                (9648, "Mystery"), (10749, "Romance"), (878, "Science Fiction"),
                (10770, "TV Movie"), (53, "Thriller"), (10752, "War"), (37, "Western")
            ]
            for genre_id, genre_name in default_genres:
                cursor.execute("""
                    INSERT IGNORE INTO genres (genre_id, genre_name)
                    VALUES (%s, %s)
                """, (genre_id, genre_name))

        # Carga películas populares
        df_movies_popular = pd.read_csv("popular_movies.csv").dropna(
            subset=["id", "title", "vote_average", "popularity", "release_date", "type"])
        
        for _, row in df_movies_popular.iterrows():
            # Inserta película
            cursor.execute("""
                INSERT IGNORE INTO movies_popular (id, title, vote_average, popularity, release_date, release_year, type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                int(row["id"]),
                row["title"],
                row["vote_average"],
                row["popularity"],
                row["release_date"],
                int(row["release_year"]) if pd.notna(row["release_year"]) else None,
                row["type"]
            ))

            # Inserta géneros de la película
            if pd.notna(row["genre_ids"]) and row["genre_ids"] != "[]":
                try:
                    genre_ids = eval(row["genre_ids"])
                    for genre_id in genre_ids:
                        cursor.execute("""
                            INSERT IGNORE INTO content_genres (content_id, genre_id, content_type)
                            VALUES (%s, %s, %s)
                        """, (int(row["id"]), int(genre_id), "movie"))
                except:
                    pass  # Si hay error, continuar

        # Carga series populares
        df_tv_popular = pd.read_csv("popular_series.csv").dropna(
            subset=["id", "title", "vote_average", "popularity", "release_date", "type"])
        
        for _, row in df_tv_popular.iterrows():
            # Inserta serie
            cursor.execute("""
                INSERT IGNORE INTO tv_popular (id, title, vote_average, popularity, release_date, release_year, type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                int(row["id"]),
                row["title"],
                row["vote_average"],
                row["popularity"],
                row["release_date"],
                int(row["release_year"]) if pd.notna(row["release_year"]) else None,
                row["type"]
            ))

            # Inserta géneros de la serie
            if pd.notna(row["genre_ids"]) and row["genre_ids"] != "[]":
                try:
                    genre_ids = eval(row["genre_ids"])
                    for genre_id in genre_ids:
                        cursor.execute("""
                            INSERT IGNORE INTO content_genres (content_id, genre_id, content_type)
                            VALUES (%s, %s, %s)
                        """, (int(row["id"]), int(genre_id), "tv"))
                except:
                    pass

        # Crea tabla combinada (películas y series)
        df_combined = pd.concat([df_movies_popular, df_tv_popular], ignore_index=True)
        df_combined = df_combined.drop_duplicates(subset="id")
        df_combined = df_combined.sort_values(by="popularity", ascending=False)

        for _, row in df_combined.iterrows():
            cursor.execute("""
                INSERT IGNORE INTO combined_popular (id, title, vote_average, popularity, release_date, release_year, type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                int(row["id"]),
                row["title"],
                row["vote_average"],
                row["popularity"],
                row["release_date"],
                int(row["release_year"]) if pd.notna(row["release_year"]) else None,
                row["type"]
            ))

        # Guarda cambios y cierra
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Base de Datos OK", "Base de datos creada y tablas llenadas correctamente con relaciones.")
        return True
    except Exception as e:
        messagebox.showerror("Error BD", f"Error creando la base de datos:\n{e}")
        return False

if __name__ == "__main__":
    print("Probando funciones de scraping...")
    if hacer_scraping():
        print("Scraping completado con éxito!")
        if crear_bd_y_cargar():
            print("Base de datos creada y cargada correctamente!")
    else:
        print("Error en el scraping")