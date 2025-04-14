import pandas as pd
import requests
import os
from io import StringIO
from dotenv import load_dotenv
from pathlib import Path
import sqlite3

# Obtener la ruta absoluta del directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta absoluta al archivo .env
env_path = Path(script_dir) / '.env'

# Verifica si el archivo .env existe
print(f"Ruta del archivo .env: {env_path}")
if os.path.exists(env_path):
    print("El archivo .env existe.")
else:
    print("¡Error! El archivo .env NO existe en la ruta especificada.")
    exit()

# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path=env_path)

# Obtener las URLs de las variables de entorno
url_movies = os.getenv('DATABASE_URL_1')
url_credits = os.getenv('DATABASE_URL_2')

# Depuración: Imprimir los valores después de load_dotenv()
print(f"Después de load_dotenv():")
print(f"DATABASE_URL_1: {url_movies}")
print(f"DATABASE_URL_2: {url_credits}")

# Verificar si las URLs se cargaron correctamente
if url_movies is None or url_credits is None:
    print("Error: No se pudieron cargar las URLs desde el archivo .env.")
    print(f"DATABASE_URL_1: {url_movies}")
    print(f"DATABASE_URL_2: {url_credits}")
    exit()  # Salir del script si las URLs no se cargaron

# Función para cargar un DataFrame desde una URL
def cargar_dataframe_desde_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Lanza un error para códigos de estado HTTP malos (4xx o 5xx)
    csv_data = StringIO(response.text)
    return pd.read_csv(csv_data)

try:
    # Cargar los DataFrames
    df_movies = cargar_dataframe_desde_url(url_movies)
    df_credits = cargar_dataframe_desde_url(url_credits)

    print("DataFrames cargados exitosamente.")

    # Crear una conexión a la base de datos SQLite
    conn = sqlite3.connect('movies_database.db')

    # Guardar los DataFrames en tablas SQL
    df_movies.to_sql('movies', conn, if_exists='replace', index=False)
    df_credits.to_sql('credits', conn, if_exists='replace', index=False)

    # Ejecutar una consulta SQL para unir las tablas
    query = """
    SELECT m.movie_id, m.title, m.overview, m.genres, m.keywords, c.cast, c.crew
    FROM movies m
    JOIN credits c ON m.title = c.title;
    """

    df_combined = pd.read_sql_query(query, conn)

    # Cerrar la conexión a la base de datos
    conn.close()

    print("Base de datos creada y tablas unidas exitosamente.")

    # Seleccionar las columnas deseadas
    df_cleaned = df_combined[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

    print("Tabla combinada limpiada.")
    print(df_cleaned.head())
except Exception as e:
    print(f"Ocurrió un error: {e}")
    