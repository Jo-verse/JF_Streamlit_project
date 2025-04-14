import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from pickle import load

# Cargar datos y modelo
data = pd.read_csv("/Users/joanafernandes/Data Science Bootcamp/26) JF_Streamlit_project/data/processed/clean_data.csv")
model = load(open("/Users/joanafernandes/Data Science Bootcamp/26) JF_Streamlit_project/models/knn_neighbors-5_algorithm-brute_metric-cosine.sav", "rb"))

# Vectorización
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(data["tags"])

# Función de recomendación
def recomendar(titulo):
    if titulo not in data["title"].values:
        return []
    idx = data[data["title"] == titulo].index[0]
    distancias, indices = model.kneighbors(tfidf_matrix[idx])
    recomendaciones = [data["title"][i] for i in indices[0] if i != idx]
    return recomendaciones

# Interfaz Streamlit
st.title("🎬 Recomendador de Películas")

pelicula = st.selectbox("Selecciona una película", sorted(data["title"].unique()))

if st.button("Mostrar recomendaciones"):
    resultados = recomendar(pelicula)
    if resultados:
        st.subheader("Películas recomendadas:")
        for r in resultados:
            st.write(f"- {r}")
    else:
        st.write("No se encontraron recomendaciones.")