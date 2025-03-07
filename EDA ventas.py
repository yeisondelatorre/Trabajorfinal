import streamlit as st
import pandas as pd

# Título del dashboard
st.title("Dashboard de Análisis de Datos")

# Crear una barra lateral o pestañas para seleccionar entre diferentes secciones
option = st.sidebar.radio("Selecciona una opción", ["Introducción", "EDA"])

if option == "Introducción":
    st.subheader("Introducción de la Base de Datos")
    st.markdown("""
    Este dashboard presenta el análisis de datos de [nombre del conjunto de datos]. Los datos fueron capturados a partir de [fuente de los datos], utilizando técnicas de [método de captura de datos], entre [fecha de inicio] y [fecha de fin].

    Los objetivos principales del análisis son:
    - [Objetivo 1]
    - [Objetivo 2]
    - [Objetivo 3]
    """)

    # Agregar una imagen desde GitHub
    st.image("https://github.com/yeisondelatorre/Trabajorfinal/blob/main/ima1.jpeg?raw=true", caption="Descripción de la imagen", use_column_width=True)

elif option == "EDA":
    st.subheader("Análisis Exploratorio de Datos (EDA)")
    st.write("""
    En esta sección realizaremos el análisis exploratorio de datos (EDA) para comprender mejor la base de datos.
    Se pueden incluir gráficas, estadísticas descriptivas y otras herramientas útiles para explorar los datos.
    """)
    
    uploaded_file = st.file_uploader("Cargar archivo CSV", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Primeras filas del dataframe:")
            st.write(df.head())  # Muestra las primeras filas del dataframe

            # Estadísticas descriptivas
            st.write("Estadísticas Descriptivas:")
            st.write(df.describe())
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
