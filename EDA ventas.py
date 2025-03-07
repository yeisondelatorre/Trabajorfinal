import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # Necesario para poder mostrar los gráficos en Streamlit
import numpy as np


# Título del dashboard
st.title("Segmentación de clientes - Hábitos de compra")

# Crear una barra lateral o pestañas para seleccionar entre diferentes secciones
option = st.sidebar.radio("Selecciona una opción", ["Introducción", "EDA"])

if option == "Introducción":
    st.subheader("Introducción")
    st.markdown("""
    El conjunto de datos en cuestión proviene de una cadena de suministro de productos para el hogar en el municipio de Magangué, Bolívar,
    y contiene información detallada sobre las ventas de diversos productos como víveres y artículos de aseo. Cada registro incluye datos sobre
    el producto vendido, la fecha de la transacción, el tipo de producto, y cuál ha sido el producto más vendido en un periodo determinado.
    El objetivo principal de este análisis es segmentar a los clientes en diferentes grupos según sus hábitos de compra, lo que permitirá ofrecer
    un sistema de recomendación de productos basado en su historial de compras. A través del uso de modelos de clasificación de machine learning (ML),
    se buscará identificar patrones y comportamientos recurrentes en las compras de los clientes, con el fin de mejorar la personalización
    de las ofertas y optimizar las estrategias comerciales. Este enfoque no solo ayudará a entender mejor las preferencias del cliente, sino que también 
    contribuirá a aumentar la eficiencia y la satisfacción del cliente mediante la propuesta de productos adecuados y oportunos.
    Los datos sobre las ventas de productos fueron capturan a través de sistemas de punto de venta (POS), los cuales registran cada transacción
    realizada en el comercio. Estos sistemas permiten almacenar información clave, como el tipo de producto, la cantidad,
    el precio, y la fecha y hora de la venta, así como el método de pago utilizado.
    
    - **Objetivo General**: Desarrollar un modelo de segmentación de clientes basado en los hábitos de compra
    a partir de los datos de ventas de una cadena de suministro de productos para el hogar en Magangué, Bolívar, con
    el fin de implementar un sistema de recomendación de productos y optimizar las estrategias comerciales mediante 
    el uso de modelos de clasificación de machine learning.

    - ***Objetivos específicos***:
        - Realizar un análisis exploratorio de datos (EDA)
        - Segmentar a los clientes
        - Desarrollar y entrenar modelos de clasificación de machine learning
        - Proponer un sistema de recomendación de productos
        - Evaluar el rendimiento de los modelos de clasificación y recomendación
    """)
    # Imagen desde GitHub
    st.image("https://github.com/yeisondelatorre/Trabajorfinal/blob/main/ima1.jpeg?raw=true", caption="Descripción de la imagen", use_container_width=True)

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
