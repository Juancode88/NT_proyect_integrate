import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import json

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 1")

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

# Configuración inicial
st.title("Desarrollo y Avance Actividad 1 - Creación de DataFrames")

# Descripción del contexto
st.write("""
Esta aplicación muestra cómo crear DataFrames de Pandas desde diferentes fuentes de datos 
y visualizarlos en una interfaz de Streamlit.
""")

# 1. DataFrame desde diccionario
st.subheader("1. DataFrame de Libros")
libros_dict = {
    "título": ["Cien años de soledad", "1984", "El Principito"],
    "autor": ["Gabriel García Márquez", "George Orwell", "Antoine de Saint-Exupéry"],
    "año de publicación": [1967, 1949, 1943],
    "género": ["Realismo mágico", "Distopía", "Fábula"]
}
df_libros = pd.DataFrame(libros_dict)
st.dataframe(df_libros)

# 2. DataFrame desde lista de diccionarios
st.subheader("2. Información de Ciudades")
ciudades_lista = [
    {"nombre": "Buenos Aires", "población": 2891000, "país": "Argentina"},
    {"nombre": "Madrid", "población": 3223000, "país": "España"},
    {"nombre": "Lima", "población": 9752000, "país": "Perú"}
]
df_ciudades = pd.DataFrame(ciudades_lista)
st.dataframe(df_ciudades)

# 3. DataFrame desde lista de listas
st.subheader("3. Productos en Inventario")
productos = [
    ["Laptop", 1200, 15],
    ["Teléfono", 800, 30],
    ["Tablet", 400, 20]
]
df_productos = pd.DataFrame(productos, columns=["producto", "precio", "stock"])
st.dataframe(df_productos)

# 4. DataFrame desde Series
st.subheader("4. Datos de Personas")
nombres = pd.Series(["Ana", "Carlos", "María", "Juan"])
edades = pd.Series([25, 32, 28, 40])
ciudades = pd.Series(["Madrid", "Barcelona", "Valencia", "Sevilla"])
df_personas = pd.DataFrame({"nombre": nombres, "edad": edades, "ciudad": ciudades})
st.dataframe(df_personas)

# 5. DataFrame desde CSV local
st.subheader("5. Datos desde CSV")
# Crear archivo CSV temporal
csv_data = """id,nombre,valor
1,Producto A,100
2,Producto B,200
3,Producto C,150"""
with open("data.csv", "w") as f:
    f.write(csv_data)

df_csv = pd.read_csv("data.csv")
st.dataframe(df_csv)

# 6. DataFrame desde Excel local
st.subheader("6. Datos desde Excel")
df = pd.read_excel('static/alternos/primer_excels.xlsx', engine='openpyxl')

# Mostrar en Streamlit
st.dataframe(df)

# 7. DataFrame desde JSON
st.subheader("7. Datos de Usuarios desde JSON")
# Crear archivo JSON temporal
json_data = [
    {"nombre": "usuario1", "correo": "usuario1@example.com"},
    {"nombre": "usuario2", "correo": "usuario2@example.com"},
    {"nombre": "usuario3", "correo": "usuario3@example.com"}
]
with open("data.json", "w") as f:
    json.dump(json_data, f)

df_json = pd.read_json("data.json")
st.dataframe(df_json)

# 8. DataFrame desde URL
st.subheader("8. Datos desde URL")
try:
    url = "https://raw.githubusercontent.com/plotly/datasets/master/iris-data.csv"
    df_url = pd.read_csv(url)
    st.dataframe(df_url.head())  # Mostrar solo las primeras filas
except:
    st.warning("No se pudo cargar el archivo desde la URL")

# 9. DataFrame desde SQLite
st.subheader("9. Datos desde SQLite")
# Crear base de datos temporal
conn = sqlite3.connect("estudiantes.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS estudiantes (nombre TEXT, calificación INTEGER)")
cursor.execute("INSERT INTO estudiantes VALUES ('Ana', 85), ('Luis', 92), ('Sofía', 78)")
conn.commit()

df_sql = pd.read_sql("SELECT * FROM estudiantes", conn)
st.dataframe(df_sql)
conn.close()

# 10. DataFrame desde NumPy array
st.subheader("10. Datos desde NumPy")
np_array = np.array([
    [1, "A", 10.5],
    [2, "B", 20.3],
    [3, "C", 15.7]
])
df_numpy = pd.DataFrame(np_array, columns=["ID", "Categoría", "Valor"])
st.dataframe(df_numpy)

# Nota al pie
st.markdown("---")           
st.caption("Aplicación creada para mostrar diferentes formas de crear DataFrames en Pandas y visualizarlos en Streamlit")