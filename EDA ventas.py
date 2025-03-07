import streamlit as st
import plotly.express as px
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

# Agregar una imagen
st.image("/content/ima1.jpeg", caption="Descripción de la imagen", use_column_width=True)
