import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

# Título del dashboard
st.title(" 📈Segmentación de clientes - Hábitos de compra📉 ")

# Crear un contenedor para el archivo y pasarlo a través de todo Streamlit
@st.cache_resource
def cargar_datos(uploaded_file):
    return pd.read_csv(uploaded_file)

# Cargar el archivo una sola vez
uploaded_file = st.sidebar.file_uploader("Cargar archivo CSV", type="csv")

# Crear una barra lateral o pestañas para seleccionar entre diferentes secciones
option = st.sidebar.radio("Selecciona una opción", ["Introducción", "EDA", "Modelado"])

if uploaded_file is not None:
    df = cargar_datos(uploaded_file)  # Cargar el archivo solo una vez

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

        try:
            # Filtrar productos más vendidos
            productos_filtrar = [590101, 590102, 590103, 205003, 200130, 800020, 205601, 540101, 501121, 501120]
            dfinal = df[df['codproducto'].isin(productos_filtrar)]  # Filtrar productos

            # Agrupar por producto para calcular total de unidades vendidas y total de ingresos
            top_productos = df.groupby(['codproducto', 'nom_producto']).agg(
                Total_Unidades=('cantidad', 'sum'),
                Total_Ventas=('Total_Venta', 'sum')
            ).reset_index()

            # Ordenar por la cantidad vendida
            top_productos = top_productos.sort_values(by=['Total_Unidades'], ascending=False)

            # Gráfico de Top 10 Productos Más Vendidos usando Plotly Express
            st.subheader("Gráfico de Top 10 Productos Más Vendidos")
            fig = px.bar(top_productos.head(10), 
                         x='Total_Unidades', 
                         y='nom_producto', 
                         orientation='h', 
                         title="Top 10 Productos Más Vendidos por Cantidad", 
                         labels={"Total_Unidades": "Total de Unidades Vendidas", "nom_producto": "Producto"}, 
                         color='Total_Unidades')
            st.plotly_chart(fig)

            # Gráfico de Distribución de Ventas por Tipo de Cliente usando Plotly Express
            st.subheader("Distribución de Ventas por Tipo de Cliente")
            ventas_tipo_cliente = df.groupby('nom_tipocliente')['Total_Venta'].sum().reset_index()
            fig2 = px.bar(ventas_tipo_cliente, 
                          x='nom_tipocliente', 
                          y='Total_Venta', 
                          title="Distribución de Ventas por Tipo de Cliente", 
                          labels={"nom_tipocliente": "Tipo de Cliente", "Total_Venta": "Total de Ventas"},
                          color='Total_Venta')
            st.plotly_chart(fig2)

            # Histograma de los productos vendidos usando Plotly Express
            st.subheader("Histograma de Productos Vendidos")
            fig3 = px.bar(dfinal.groupby('nom_producto')['Total_Venta'].sum().reset_index(), 
                          x='nom_producto', 
                          y='Total_Venta', 
                          title="Total de Ventas por Producto", 
                          labels={"nom_producto": "Producto", "Total_Venta": "Total de Ventas"},
                          color='Total_Venta')
            st.plotly_chart(fig3)

        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

    elif option == "Modelado":
        st.subheader("Modelado: Clustering de Clientes")
        st.markdown("""
        En esta sección, se realizará un análisis de clustering utilizando el algoritmo **K-Means** para segmentar los clientes según 
        sus hábitos de compra. Utilizaremos las variables de **cantidad** y **precio_dig** para identificar grupos o clusters de clientes 
        similares, lo que nos permitirá obtener una visión más clara sobre el comportamiento de compra.
        """)

        try:
            # Filtro de productos más vendidos
            productos_filtrar = [590101, 590102, 590103, 205003, 200130, 800020, 205601, 540101, 501121, 501120]
            dfinal = df[df['codproducto'].isin(productos_filtrar)]  # Filtrar productos

            # Seleccionar variables relevantes para el clustering
            df_cluster = dfinal[['cantidad', 'precio_dig']]

            # Estandarizar los datos
            scaler = StandardScaler()
            df_cluster_scaled = scaler.fit_transform(df_cluster)

            # Encontrar el número óptimo de clusters con el método del codo
            wcss = []
            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
                kmeans.fit(df_cluster_scaled)
                wcss.append(kmeans.inertia_)

            # Gráfico método del codo usando Plotly
            fig_codo = go.Figure()
            fig_codo.add_trace(go.Scatter(
                x=list(range(1, 11)), 
                y=wcss, 
                mode='lines+markers', 
                name='WCSS'
            ))
            fig_codo.update_layout(
                title='Método del Codo',
                xaxis_title='Número de Clusters',
                yaxis_title='WCSS',
                template='plotly_dark'
            )
            st.plotly_chart(fig_codo)

            # K = 3 o K = 4 para la segmentación
            st.markdown("**Resultado del Clustering con K = 3**:")
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            dfinal['Cluster'] = kmeans.fit_predict(df_cluster_scaled)

            # Visualización de los clusters con la paleta de colores Viridis
            fig_clusters = px.scatter(dfinal, x='cantidad', y='precio_dig', color='Cluster', title="Segmentación de Clientes por Clustering (K=3)",
                                      labels={"cantidad": "Cantidad", "precio_dig": "Precio", "Cluster": "Cluster"},
                                      color_continuous_scale='viridis')
            st.plotly_chart(fig_clusters)

        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")




