import streamlit as st
import numpy as np
from faker import Faker
import pandas as pd

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 4")

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
np.random.seed(42)
fake = Faker('es_ES')
Faker.seed(42)

# Título de la aplicación
st.title('🏰 Academia de Magia Digital')
st.markdown("---")  

# Generación de datos
n_estudiantes = 1000

with st.spinner('Generando estudiantes mágicos...'):
    # Generar nombres únicos
    nombres_unicos = set()
    while len(nombres_unicos) < n_estudiantes:
        nombres_unicos.add(f"{fake.first_name()} {fake.last_name()}")
    
    casas = ['Dragonescale', 'Moonlight', 'Thunderclaw', 'Sunflare', 'Nightshade']
    asignaturas = ['Hechizos', 'Pociones', 'Criaturas Mágicas', 'Adivinación', 'Transformaciones']
    mascotas = ['Dragón', 'Lechuza', 'Gato', 'Salamandra', 'Fénix']
    
    nombres_split = [nombre.split() for nombre in list(nombres_unicos)]
    
    data = {
        'Nombre': [n[0] for n in nombres_split],
        'Apellido': [n[1] for n in nombres_split],
        'Casa': np.random.choice(casas, n_estudiantes, p=[0.2, 0.3, 0.15, 0.25, 0.1]),
        'Nivel_Mágico': np.random.randint(30, 100, n_estudiantes),
        'Asignatura_Favorita': np.random.choice(asignaturas, n_estudiantes),
        'Mascota': np.random.choice(mascotas, n_estudiantes, p=[0.1, 0.4, 0.3, 0.1, 0.1]),
        'Año_Ingreso': np.random.randint(2015, 2023, n_estudiantes)
    }
    
    df = pd.DataFrame(data)

# Sección de operaciones
st.header('🔮 Operaciones Mágicas')
st.subheader('1. Élite de Dragonescale')
dragonescale_elite = df.loc[
    (df['Casa'] == 'Dragonescale') & 
    (df['Nivel_Mágico'] > 80) & 
    (df['Mascota'] == 'Dragón'),
    ['Nombre', 'Apellido', 'Nivel_Mágico', 'Año_Ingreso']
]
st.dataframe(dragonescale_elite)

st.subheader('2. Modificación de Niveles Mágicos')
with st.echo():
    df.loc[
        (df['Casa'] == 'Thunderclaw') & 
        (df['Año_Ingreso'] >= 2020), 
        'Nivel_Mágico'
    ] += 15

st.subheader('3. Categoría de Riesgo')
df['Riesgo'] = np.where(df['Nivel_Mágico'] < 50, 'Alto', 'Bajo')
st.metric("Estudiantes en riesgo alto", df[df['Riesgo'] == 'Alto'].shape[0])

st.subheader('4. Intercambio de Mascotas')
cols = st.columns(2)
with cols[0]:
    st.write("Antes del intercambio:")
    st.table(df.iloc[[100, 500]][['Nombre', 'Mascota']])
    
df.iloc[[100, 500], df.columns.get_loc('Mascota')] = df.iloc[[500, 100], df.columns.get_loc('Mascota')].values

with cols[1]:
    st.write("Después del intercambio:")
    st.table(df.iloc[[100, 500]][['Nombre', 'Mascota']])

st.subheader('5. Subset Estratégico')
subset = df.iloc[:int(n_estudiantes*0.1), [0, 2, 5]]
st.dataframe(subset)

st.subheader('6. Mensaje Secreto')
mensaje_secreto = {
    42: 'A', 153: 'L', 267: 'E', 398: 'G', 512: 'R', 
    689: 'I', 777: 'A', 888: 'M', 999: '!'
}

for idx, letra in mensaje_secreto.items():
    if idx < len(df):
        df.iloc[idx, df.columns.get_loc('Nombre')] = letra

st.success("Mensaje oculto insertado correctamente!")

# Análisis
st.header('📊 Análisis Mágico')
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Nivel promedio por casa:**")
    niveles_casa = df.groupby('Casa')['Nivel_Mágico'].mean().round(2)
    st.bar_chart(niveles_casa)

with col2:
    mascota_popular = df[df['Casa']=='Moonlight']['Mascota'].mode()[0]
    st.markdown(f"**Mascota más popular en Moonlight:**")
    st.markdown(f"<h2 style='text-align: center; color: #FF4B4B;'>{mascota_popular}</h2>", 
                unsafe_allow_html=True)

# Mostrar datos completos
st.header('📚 Base de Datos Completa')
st.dataframe(df)

# Guardar datos
if st.button('💾 Guardar Datos'):
    df.to_csv('academia_magia.csv', index=False)
    st.success("Datos guardados como 'academia_magia.csv'")