import streamlit as st
import pandas as pd

# Título del dashboard
st.title("Dashboard de Análisis de Datos")

# Apartado de introducción
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

#### pestaña para el eda

# Crear una barra lateral o pestañas para seleccionar entre diferentes secciones
option = st.sidebar.radio("Selecciona una opción", ["Introducción", "EDA"])

if option == "Introducción":
    st.subheader("Introducción de la Base de Datos")
    st.markdown("""
    Aquí se describe cómo se recogieron los datos, la fuente de la base de datos y otros detalles relevantes.
    """)

elif option == "EDA":
    st.subheader("Análisis Exploratorio de Datos (EDA)")
    st.write("""
    En esta sección realizaremos el análisis exploratorio de datos (EDA) para comprender mejor la base de datos.
    Se pueden incluir gráficas, estadísticas descriptivas y otras herramientas útiles para explorar los datos.
    """)
    # Aquí es donde agregarías tu código para realizar el EDA más adelante.
