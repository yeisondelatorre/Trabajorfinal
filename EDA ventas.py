import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # Necesario para poder mostrar los gráficos en Streamlit
import plotly.express as px
import numpy as np


# Título del dashboard
st.title(" 📈Segmentación de clientes - Hábitos de compra📉 ")

# Crear una barra lateral o pestañas para seleccionar entre diferentes secciones
option = st.sidebar.radio("Selecciona una opción", ["Introducción", "EDA"])

if option == "Introducción":
    st.subheader("Introducción")
    st.markdown("""
    El conjunto de datos en cuestión proviene de una cadena de suministro de productos para los hogares en Colombia,
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

            # Filtro de productos más vendidos
            productos_filtrar = [590101, 590102, 590103, 205003, 200130, 800020, 205601, 540101, 501121, 501120]
            dfinal = df[df['codproducto'].isin(productos_filtrar)]  # Filtrar productos

            # Agrupar por producto para calcular total de unidades vendidas y total de ingresos
            top_productos = df.groupby(['codproducto', 'nom_producto']).agg(
                Total_Unidades=('cantidad', 'sum'),
                Total_Ventas=('Total_Venta', 'sum')
            ).reset_index()

            # Ordenar por la cantidad vendida
            top_productos = top_productos.sort_values(by=['Total_Unidades'], ascending=False)

            # Gráfico de Top 10 Productos Más Vendidos usando Plotly
            st.subheader("Gráfico de Top 10 Productos Más Vendidos")
            fig = px.bar(top_productos.head(10), 
                         x='Total_Unidades', 
                         y='nom_producto', 
                         orientation='h', 
                         title="Top 10 Productos Más Vendidos por Cantidad", 
                         labels={"Total_Unidades": "Total de Unidades Vendidas", "nom_producto": "Producto"}, 
                         color='Total_Unidades',
                         color_continuous_scale='Blues')
            st.plotly_chart(fig)

            # Gráfico de Distribución de Ventas por Tipo de Cliente usando Plotly
            st.subheader("Distribución de Ventas por Tipo de Cliente")
            ventas_tipo_cliente = df.groupby('nom_tipocliente')['Total_Venta'].sum().reset_index()
            fig2 = px.bar(ventas_tipo_cliente, 
                          x='nom_tipocliente', 
                          y='Total_Venta', 
                          title="Distribución de Ventas por Tipo de Cliente", 
                          labels={"nom_tipocliente": "Tipo de Cliente", "Total_Venta": "Total de Ventas"},
                          color='Total_Venta', 
                          color_continuous_scale='Purples')
            st.plotly_chart(fig2)

            # Histograma de los productos vendidos usando Matplotlib
            st.subheader("Histograma de Productos Vendidos")
            plt.figure(figsize=(12, 6))
            dfinal.groupby('nom_producto')['Total_Venta'].sum().plot(kind='bar', color='seagreen', alpha=0.7, edgecolor='black')
            plt.xlabel("Producto", fontsize=12)
            plt.ylabel("Total de Ventas", fontsize=12)
            plt.title("Total de Ventas por Producto", fontsize=14)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()  # Asegura que las etiquetas no se corten
            st.pyplot(plt)  # Mostrar gráfico en Streamlit

        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
