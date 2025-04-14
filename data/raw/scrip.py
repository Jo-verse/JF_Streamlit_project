import os
import requests

# URL del dataset
url = "https://raw.githubusercontent.com/4GeeksAcademy/naive-bayes-project-tutorial/main/playstore_reviews.csv"

# Ruta donde se guardará el archivo
file_path = os.path.join("data", "raw", "Playstore_reviews.csv")

# Crear los directorios si no existen
os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Crea 'data/raw' si no existen

# Descargar el archivo y guardarlo
response = requests.get(url)

if response.status_code == 200:
    with open(file_path, "wb") as file:
        file.write(response.content)
    print(f"✅ Archivo guardado en {file_path}")
else:
    print("❌ Error al descargar el archivo")