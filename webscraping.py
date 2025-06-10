import requests
import pandas as pd
import mysql.connector
from tkinter import messagebox

API_KEY = "6e9456bdd4ec35e91f83f2cf2950e4c2"
BASE_URL = "https://api.themoviedb.org/3"


def fetch_tmdb_data(endpoint, pages=5):
    """Obtiene datos de la API de TMDB"""
    all_results = []
    for page in range(1, pages + 1):
        params = {"api_key": API_KEY, "page": page}
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get("results", []))
        else:
            messagebox.showerror("Error", f"Error en página {page}: {response.status_code}")
            break
    return all_results


def fetch_genres():
    """Obtiene los géneros de películas y series de TMDB"""
    try:
        # Géneros de películas
        movie_genres_response = requests.get(f"{BASE_URL}/genre/movie/list", params={"api_key": API_KEY})
        tv_genres_response = requests.get(f"{BASE_URL}/genre/tv/list", params={"api_key": API_KEY})

        movie_genres = movie_genres_response.json().get("genres",
                                                        []) if movie_genres_response.status_code == 200 else []
        tv_genres = tv_genres_response.json().get("genres", []) if tv_genres_response.status_code == 200 else []

        # Combinar géneros y eliminar duplicados
        all_genres = {}
        for genre in movie_genres + tv_genres:
            all_genres[genre['id']] = genre['name']

        return all_genres
    except Exception as e:
        messagebox.showerror("Error", f"Error obteniendo géneros: {e}")
        return {}


def to_dataframe(data, content_type):
    """Convierte los datos a un DataFrame de pandas"""
    df = pd.DataFrame(data)
    df["type"] = content_type
    if content_type == "movie":
        df["title"] = df["title"]
        df["release_date"] = df["release_date"]
    else:
        df["title"] = df["name"]
        df["release_date"] = df["first_air_date"]

    # Extraer año de la fecha de lanzamiento
    df["release_year"] = pd.to_datetime(df["release_date"], errors='coerce').dt.year

    return df[["id", "title", "vote_average", "popularity", "release_date", "release_year", "type", "genre_ids"]]


def hacer_scraping():
    """Realiza el scraping de datos y guarda en archivos CSV"""
    try:
        # Obtener géneros primero
        genres_dict = fetch_genres()

        popular_movies = fetch_tmdb_data("/movie/popular")
        top_rated_movies = fetch_tmdb_data("/movie/top_rated")
        popular_series = fetch_tmdb_data("/tv/popular")

        df_popular_movies = to_dataframe(popular_movies, "movie")
        df_top_rated_movies = to_dataframe(top_rated_movies, "movie")
        df_popular_series = to_dataframe(popular_series, "tv")

        # Guardar géneros
        genres_df = pd.DataFrame(list(genres_dict.items()), columns=['genre_id', 'genre_name'])
        genres_df.to_csv("genres.csv", index=False)

        df_popular_movies.to_csv("popular_movies.csv", index=False)
        df_top_rated_movies.to_csv("top_rated_movies.csv", index=False)
        df_popular_series.to_csv("popular_series.csv", index=False)

        messagebox.showinfo("Scraping OK", "Scraping completado y CSV guardados.")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error durante el scraping:\n{e}")
        return False


def crear_bd_y_cargar():
    """Crea la base de datos y carga los datos"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS tmdb_db")
        conn.database = "tmdb_db"

        # Eliminar tablas existentes
        cursor.execute("DROP TABLE IF EXISTS content_genres")
        cursor.execute("DROP TABLE IF EXISTS genres")
        cursor.execute("DROP TABLE IF EXISTS movies_popular")
        cursor.execute("DROP TABLE IF EXISTS tv_popular")
        cursor.execute("DROP TABLE IF EXISTS combined_popular")

        # Crear tabla de géneros
        cursor.execute("""
            CREATE TABLE genres (
                genre_id INT PRIMARY KEY,
                genre_name VARCHAR(100) NOT NULL
            )
        """)

        # Crear tablas de contenido con año
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

        # Crear tabla de relación content-genres
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

        # Cargar géneros
        try:
            genres_df = pd.read_csv("genres.csv")
            for _, row in genres_df.iterrows():
                cursor.execute("""
                    INSERT IGNORE INTO genres (genre_id, genre_name)
                    VALUES (%s, %s)
                """, (int(row["genre_id"]), row["genre_name"]))
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

        # Cargar películas populares
        df_movies_popular = pd.read_csv("popular_movies.csv").dropna(
            subset=["id", "title", "vote_average", "popularity", "release_date", "type"])
        for _, row in df_movies_popular.iterrows():
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

            # Insertar géneros de la película
            if pd.notna(row["genre_ids"]) and row["genre_ids"] != "[]":
                try:
                    genre_ids = eval(row["genre_ids"])  # Convertir string a lista
                    for genre_id in genre_ids:
                        cursor.execute("""
                            INSERT IGNORE INTO content_genres (content_id, genre_id, content_type)
                            VALUES (%s, %s, %s)
                        """, (int(row["id"]), int(genre_id), "movie"))
                except:
                    pass

        # Cargar series populares
        df_tv_popular = pd.read_csv("popular_series.csv").dropna(
            subset=["id", "title", "vote_average", "popularity", "release_date", "type"])
        for _, row in df_tv_popular.iterrows():
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

            # Insertar géneros de la serie
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

        # Cargar tabla combinada
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

        conn.commit()
        conn.close()
        messagebox.showinfo("Base de Datos OK", "Base de datos creada y tablas llenadas correctamente con relaciones.")
        return True
    except Exception as e:
        messagebox.showerror("Error BD", f"Error creando la base de datos:\n{e}")
        return False


if __name__ == "__main__":
    print("Aqui estan las funciones para scraping de TMDB y el manejo de BD.")
    print("La interfaz gráfica se encuentra en: interfaz.py, al ejecutarla se muestra")
