import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
import random

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 3")

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


st.header("Ejercicio 1 - primeros 10 puntos")
st.text("Link de puntos ejecutados en un notebook de google colab")

url = "https://colab.research.google.com/drive/15xJXXwBepvM2_RzdeB2qnrdGWRubsm7O?usp=sharing"
st.markdown(f"Check out this [link]({url})")  

# Configurar Faker para Colombia
fake = Faker('es_CO')

@st.cache_data
def generar_datos():
    # Establecer semillas para reproducibilidad
    np.random.seed(123)
    random.seed(123)
    fake.seed_instance(123)
    
    # Crear datos
    n = 50
    data = {
        'id': range(1, n + 1),
        'nombre_completo': [fake.name() for _ in range(n)],
        'edad': np.random.randint(15, 76, n),
        'region': random.choices(
            ['Caribe', 'Andina', 'Pacífica', 'Orinoquía', 'Amazonía'],
            weights=[0.3, 0.4, 0.15, 0.1, 0.05],
            k=n
        ),
        'municipio': random.choices(
            [
                'Barranquilla', 'Santa Marta', 'Cartagena',  # Caribe
                'Bogotá', 'Medellín', 'Tunja', 'Manizales',  # Andina
                'Cali', 'Quibdó', 'Buenaventura',           # Pacífica
                'Villavicencio', 'Yopal',                    # Orinoquía
                'Leticia', 'Puerto Inírida'                  # Amazonía
            ],
            k=n
        ),
        'ingreso_mensual': np.random.randint(800000, 12000001, n),
        'ocupacion': random.choices(
            [
                'Estudiante', 'Docente', 'Comerciante', 'Agricultor',
                'Ingeniero', 'Médico', 'Desempleado', 'Pensionado',
                'Emprendedor', 'Obrero'
            ],
            k=n
        ),
        'tipo_vivienda': random.choices(
            ['Propia', 'Arrendada', 'Familiar'],
            k=n
        ),
        'fecha_nacimiento': [
            fake.date_of_birth(minimum_age=15, maximum_age=75) for _ in range(n)
        ],
        'acceso_internet': random.choices([True, False], weights=[0.7, 0.3], k=n)
    }

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Introducir valores nulos
    df.loc[3:5, 'ingreso_mensual'] = np.nan
    df.loc[15:17, 'ocupacion'] = np.nan

    # Convertir fecha de nacimiento
    df['fecha_nacimiento'] = pd.to_datetime(df['fecha_nacimiento'])
    
    return df

# Generar datos
df = generar_datos()

# Título de la aplicación
st.title('Aplicación de Filtros Dinámicos')

# Inicializar máscara de filtrado
mask = pd.Series([True] * len(df), index=df.index)

# Barra lateral para filtros
st.sidebar.title('Configuración de Filtros')

# 1. Filtro por rango de edad
if st.sidebar.checkbox('Filtrar por rango de edad'):
    edad_range = st.sidebar.slider(
        'Rango de edad',
        min_value=15,
        max_value=75,
        value=(15, 75)  # Aquí estaba faltando cerrar el paréntesis del slider
    )
    mask &= df['edad'].between(*edad_range) 
# 2. Filtro por municipios
if st.sidebar.checkbox('Filtrar por municipios'):
    municipios = [
        'Barranquilla', 'Santa Marta', 'Cartagena', 'Bogotá',
        'Medellín', 'Tunja', 'Manizales', 'Cali', 'Quibdó',
        'Buenaventura', 'Villavicencio', 'Yopal', 'Leticia',
        'Puerto Inírida'
    ]
    selected_mun = st.sidebar.multiselect('Seleccionar municipios', municipios)
    if selected_mun:
        mask &= df['municipio'].isin(selected_mun)

# 3. Filtro por ingreso mínimo
if st.sidebar.checkbox('Filtrar por ingreso mensual mínimo'):
    min_income = st.sidebar.slider(
        'Ingreso mínimo (COP)',
        800000,
        12000000,
        800000
    )
    mask &= (df['ingreso_mensual'] > min_income)

# 4. Filtro por ocupación
if st.sidebar.checkbox('Filtrar por ocupación'):
    ocupaciones = [
        'Estudiante', 'Docente', 'Comerciante', 'Agricultor',
        'Ingeniero', 'Médico', 'Desempleado', 'Pensionado',
        'Emprendedor', 'Obrero'
    ]
    selected_occ = st.sidebar.multiselect('Seleccionar ocupaciones', ocupaciones)
    if selected_occ:
        mask &= df['ocupacion'].isin(selected_occ)

# 5. Filtro por vivienda no propia
if st.sidebar.checkbox('Filtrar personas sin vivienda propia'):
    mask &= ~(df['tipo_vivienda'] == 'Propia')

# 6. Filtro por nombre
if st.sidebar.checkbox('Filtrar por nombre'):
    nombre_filter = st.sidebar.text_input('Buscar en nombres')
    mask &= df['nombre_completo'].str.contains(nombre_filter, case=False, na=False)

# 7. Filtro por año de nacimiento
if st.sidebar.checkbox('Filtrar por año de nacimiento'):
    años = list(range(1949, 2010))
    selected_year = st.sidebar.selectbox('Seleccionar año', años)
    mask &= (df['fecha_nacimiento'].dt.year == selected_year)

# 8. Filtro por acceso a internet
if st.sidebar.checkbox('Filtrar por acceso a internet'):
    internet = st.sidebar.radio('Acceso a internet', ['Sí', 'No'])
    mask &= (df['acceso_internet'] == (internet == 'Sí'))

# 9. Filtro por ingresos nulos
if st.sidebar.checkbox('Filtrar por ingresos nulos'):
    mask &= df['ingreso_mensual'].isna()
else:
    mask &= df['ingreso_mensual'].notna()

# 10. Filtro por rango de fechas
if st.sidebar.checkbox('Filtrar por rango de fechas de nacimiento'):
    fecha_min = pd.to_datetime('1949-01-01')
    fecha_max = pd.to_datetime('2009-12-31')
    
    start_date = st.sidebar.date_input(
        'Fecha inicial',
        value=fecha_min,
        min_value=fecha_min,
        max_value=fecha_max
    )
    
    end_date = st.sidebar.date_input(
        'Fecha final',
        value=fecha_max,
        min_value=fecha_min,
        max_value=fecha_max
    )
    
    mask &= df['fecha_nacimiento'].between(
        pd.to_datetime(start_date),
        pd.to_datetime(end_date)
    )


# Aplicar todos los filtros
filtered_df = df[mask]


# Mostrar resultados
st.subheader('Datos Filtrados')
st.write(f'Registros encontrados: {len(filtered_df)}')
st.dataframe(filtered_df)

