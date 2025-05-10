import streamlit as st
import pandas as pd
from io import StringIO

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 2")

st.header("Descripción de la actividad")
st.markdown("""
Esta actividad es una introducción práctica a Python y a las estructuras de datos básicas.
En ella, exploraremos los conceptos fundamentales de Python y aprenderemos a utilizar variables,
tipos de datos, operadores, y las estructuras de datos más utilizadas como listas, tuplas,
diccionarios y conjuntos.
""")

st.header("Objetivos de aprendizaje")

st.markdown("""
- Comprender los tipos de datos básicos en Python
- Aprender a utilizar variables y operadores
- Dominar las estructuras de datos fundamentales
- Aplicar estos conocimientos en ejemplos prácticos
""")

st.header("Solución")

df = pd.read_csv('static/datasets/estudiantes_colombia.csv')

st.header("Vista General")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Primeras 5 filas")
    st.write(df.head())
with col2:
    st.subheader("Últimas 5 filas")
    st.write(df.tail())

# Sección 2: Resumenes
st.header("Resúmenes Estadísticos")
st.subheader("Datos estadísticos básicos")
st.write(df.describe())

st.subheader("Información del dataset")
buffer = StringIO()
df.info(buf=buffer)
st.text(buffer.getvalue())

# Sección 3: Selección columnas
st.header("Selección de Columnas")
columnas = st.multiselect(
    "Selecciona columnas para visualizar:",
    options=df.columns,
    default=["nombre", "edad", "promedio"]
)
if columnas:
    st.write(df[columnas])

# Sección 4: Filtro por promedio
st.header("Filtrar por Promedio")
rango_min = int(df["promedio"].min())
rango_max = int(df["promedio"].max())

filtro = st.slider(
    "Selecciona promedio mínimo:",
    min_value=rango_min,
    max_value=rango_max,
    value=rango_min
)

estudiantes_filtrados = df[df["promedio"] > filtro]
st.write(f"Estudiantes con promedio mayor a {filtro}:")
st.write(estudiantes_filtrados)