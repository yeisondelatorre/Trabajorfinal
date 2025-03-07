import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # Necesario para poder mostrar los gráficos en Streamlit
import numpy as np


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

            # Asegurar que las columnas clave estén en el tipo correcto
            df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
            df['precio_dig'] = pd.to_numeric(df['precio_dig'], errors='coerce')

            # Crear una nueva columna de ingresos totales por venta
            df['Total_Venta'] = df['cantidad'] * df['precio_dig']

            # Agrupar por producto para calcular total de unidades vendidas y total de ingresos
            top_productos = df.groupby(['codproducto', 'nom_producto']).agg(
                Total_Unidades=('cantidad', 'sum'),
                Total_Ventas=('Total_Venta', 'sum')
            ).reset_index()

            # Ordenar por la cantidad vendida
            top_productos = top_productos.sort_values(by=['Total_Unidades'], ascending=False)

            # Visualizar con un gráfico de barras usando Seaborn
            st.subheader("Gráfico de Top 10 Productos Más Vendidos")
            plt.figure(figsize=(12, 6))
            sns.barplot(data=top_productos.head(10), y='nom_producto', x='Total_Unidades', palette='Blues_d')

            # Etiquetas y título
            plt.xlabel("Total de Unidades Vendidas")
            plt.ylabel("Producto")
            plt.title("Top 10 Productos Más Vendidos por Cantidad")
            plt.gca().invert_yaxis()  # Invertir el eje Y para que el producto más vendido esté arriba

            # Mostrar el gráfico en Streamlit
            st.pyplot(plt)  # Muestra el gráfico usando Streamlit

            # Gráfico de Distribución de Ventas por Tipo de Cliente
            st.subheader("Distribución de Ventas por Tipo de Cliente")
            plt.figure(figsize=(12,6))

            # Agrupar las ventas por tipo de cliente
            ventas_tipo_cliente = df.groupby('nom_tipocliente')['Total_Venta'].sum()

            # Graficar el resultado
            ventas_tipo_cliente.plot(kind='bar', color='purple', alpha=0.7, edgecolor='black')

            # Etiquetas y título del gráfico
            plt.xlabel("Tipo de Cliente", fontsize=12, labelpad=10)
            plt.ylabel("Total de Ventas", fontsize=12, labelpad=10)
            plt.title("Distribución de Ventas por Tipo de Cliente", fontsize=14, pad=15)

            # Ajustes de formato
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.yticks(fontsize=10)
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # Mejorar el ajuste del gráfico
            plt.tight_layout()

            # Mostrar el gráfico en Streamlit
            st.pyplot(plt)  # Muestra el gráfico usando Streamlit

        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
