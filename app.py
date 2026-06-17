#   IMPORTAR LIBRERIAS
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import geopandas as gpd

#   CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Geomorfositios de Costa Rica",
    #layout='wide'             
)

#   CARGAR DATOS DESDE GITHUB
@st.cache_data
def cargar_datos():
    return pd.read_csv("https://raw.githubusercontent.com/dennisperez10/Tarea2/refs/heads/main/Geomorfositios.csv", sep=';')

geomorfositios = cargar_datos()


#   TITULO DE LA APLICACION
st.title("Análisis de geomorfositios en Costa Rica")

#   TEXTO INTRODUCTORIO
st.write("En Costa Rica el estudio de geomorfositios data del año 2017. En ese entonces no se conocía del tema y prácticamente era desconocido. No obstante, con el transcurso de los años las investigaciones fueron en aumento, realizándose trabajos en áreas silvestres protegidas principalmente.")
st.write("Aunque las investigaciones se han publicado a nivel internacional en revistas indexadas queda el rezago de divulgarlo ampliamente en el país para que la población sepa del contenido de estas investigaciones.")
st.write("A continuación, se plantea un repaso con algunos de los principales datos recopilados sobre geomorfositios en Costa Rica. Estos corresponden a datos reales obtenidos para desarrollar la tesis titulada ***Propuesta de visor cartográfico para la difusión de información de geomorfositios en Costa Rica*** para obtener el grado de Maestría en Sistemas de Información Geográfica y Teledetección.")

#   INVENTARIO
st.subheader("Inventario de geomorfositios")
st.write("Como parte del proceso de investigación se realizó un inventario de geomorfositios a nivel de todo Costa Rica. Se usó como fuentes de información aquellas publicaciones donde se han identificado y evaluado geomorfositios. Se tomó en consideración en la revisión bibliográfica artículos científicos, tesis e informes técnicos institucionales que hayan propuesto geomorfositios.")
st.write("Como resultado se obtuvo que a nivel nacional han sido identificados 65 geomorfositios. En la tabla anterior se muestra un extracto con sus respectivos atributos de información para 5 geomorfositios seleccionados al azar de acuerdo con el código implementado.")
st.write("Cabe destacar que no hay un geomorfositio que sea igual a otro. Podrán compartir características geofísicas o culturales pero no hay dos iguales, tanto a nivel nacional como a nivel internacional.")

# Mostrar una tabla con los datos
#st.dataframe(geomorfositios, use_container_width=True, hide_index=True)

#   GRÁFICO DE GEOMORFOSITIOS POR ASP
# Conteo de geomorfositios por ASP
geomorfositios_suma = geomorfositios.groupby('AreaProtegida').count()

# Suma de geomorfositios por ASP
geomorfositios_suma = geomorfositios.groupby('AreaProtegida').size().reset_index(name='Cantidad')

#Ordenar de mayor a menor
geomorfositios_suma = geomorfositios_suma.sort_values(by='Cantidad', ascending=False)

# Crear gráfico de barras
grafico = px.bar(
    geomorfositios_suma,
    x="AreaProtegida",
    y="Cantidad",
    orientation="v",
    title='Total de Geomorfositios por Área Silvestre Protegida',
    labels={"AreaProtegida": "Área Protegida", "Cantidad": "Cantidad"}
)
st.plotly_chart(grafico, use_container_width=True)

#   DESCRIPCIÓN DEL GRÁFICO DE BARRAS
st.write ("Una característica importante en los estudios sobre geomorfositios realizados en el país es que la mayoría trabajos se realizaron dentro de ***Áreas Silvestres Protegidas***. La razón de esto radica en que la categoría de manejo le da protección al geomorfositio de cualquier impacto causado por el ser humano. Sin embargo, no es necesario que un geomorfositio esté dentro de un Área Protegida")
st.write ("El gráfico anterior muestra que se han identificado geomorfositios en cinco áreas silvestres protegidas, siendo el Parque Nacional Chirripó donde más geomorfositios fueron identificados. En total 39 geomorfositios están dentro de parques nacionales. Sin embargo, esto no es una regla en firme porque hay 26 geomorfositios que fueron identificados y que no están dentro de un área protegida. Esto más bien significa que son formaciones que están en expuestas a ser dañadas por las actividades humanas. ")

#   GRÁFICO DE CLASIFICACIÓN DE GEOMORFOSITIOS
# Conteo de geomorfositios por clasificación
geomorfositios_clase = geomorfositios.groupby('Clasificacion').size().reset_index(name='Cantidad')

# Crear gráfico circular
fig = px.pie(
    geomorfositios_clase,
    names='Clasificacion',
    values='Cantidad',
    title='Distribución de geomorfositios por clasificación',
    labels={'Clasificacion': 'Clasificación', 'Cantidad': 'Cantidad de geomorfositios'}
)

# Atributos globales de la figura
fig.update_layout(
    title=dict(
        text='Distribución de geomorfositios por clasificación',
        x=0.5,
        xanchor='center'
    ),
    legend_title_text='Clasificación'
)

# Atributos de las propiedades visuales
fig.update_traces(textposition='inside', textinfo='percent')

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)

#   DESCRIPCIÓN DEL GRÁFICO CIRCULAR
st.write("Con el inventario de geomorfositios se verifica que cada investigación utilizó una metodología de valoración diseñada por el equipo de trabajo de Reynard et al. (2016), la cual consiste en dos valoraciones distintas con sus respectivos puntos a evaluar sobre valores científicos y valores añadidos. De acuerdo con los valores obtenidos se realizó una clasificación propuesta por Bouzekraoui et al(2017) quien establece tres categorías de valoración (alta, media y baja) de acuerdo el valor dado para sus valores científicos y añadidos.")
st.write("De tal manera, se registra que hay un 44.6% de geomorfositios con categoría alta. Esto significa que son geomorfositios que han obtenido valores altos en sus valores científicos y añadidos. Significando que son geomorfositios representativos por tratarse de lugares siniguales en el país. Mientras que un 33,8% de los geomorfositios entran en la categoría baja, siendo estos sitios poco representativos por existir varios de estos que son similares entre sí. Mientras que un 21,5% de los geomorfositios poseen categoría media, siendo estos geomorfositios que no tienen el mismo nivel de relevancia de los geomorfositios más representativos del área de estudio.")

#   GRÁFICO DE DISPERSIÓN POR VALORES DE GEOMORFOSITIO
# Selección de columnas
geomorfositios_seleccionados = geomorfositios[['Codigo', 'ValoresCientificos', 'ValoresAnadidos']]

# Creación del gráfico de dispersión
fig = px.scatter(
    geomorfositios_seleccionados,
    x='ValoresCientificos',
    y='ValoresAnadidos',
    color='Codigo',    # para colorear los puntos
    text='Codigo',
    title='Relación entre Valor Científico y Valor Añadido',
    labels={
        'Codigo': 'Codigo',
        'ValoresCientificos': 'Valor Científico',
        'ValoresAnadidos': 'Valor Añadido',
    },
    hover_data={
        'Codigo': True,                       # para mostrar la columna NAME
        'ValoresCientificos': ':,.2f',        # formato con dos decimales y separador de miles
        'ValoresAnadidos': ':.2f',            # formato con dos decimales
    }
)

# Atributos globales de la figura
fig.update_layout(
    title=dict(
        text='Relación entre Valor Científico y Valor Añadido de los geomorfositios',
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    ),
    xaxis_tickformat=',',
    yaxis_tickformat=',',
    xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='lightgray')
)

# Atributos de los elementos visuales del gráfico
fig.update_traces(
    textposition='top center',
    textfont=dict(size=6)
)

# Ajuste del eje x para que comience en 0
x_max = geomorfositios_seleccionados['ValoresCientificos'].max() * 1.05  # Añade un 5% de margen superior
fig.update_xaxes(range=[0, x_max])

# Despliegue del gráfico
st.plotly_chart(fig, use_container_width=True)

#   DESCRIPCIÓN DEL GRÁFICO DE DISPERSIÓN
st.write("Por otra parte, el diagrama de dispersión anterior muestra la comparación entre los valores científicos y valores añadidos. Donde entre más alto a la derecha se localiza un punto del gráfico simboliza que es un geomorfositio de gran relevancia. En este caso se observa que hay un gran número de puntos en la esquina inferior izquierda, siendo estos geomorfositios que tienen poca relevancia. No obstante, entre los geomorfositios más relevantes destacan dos en la esquina superior derecha. Estos son los geomorfositios IRAvol001 y PVAvol001, siendo estos los cráteres de los volcanes Irazú y Poás respectivamente.")
st.write("La razón de obtener valores altos podría tratarse por ser de los lugares más visitados a nivel nacional y ser lugares con los que la población se llega a sentir identificada dandoles un valor y sentido de pertenencia. Es probable que hayan otros geomorfositios tengan características similares pero no tienen el mismo nivel de relevancia que estos geomorfositios en concreto.")
st.write("La importancia de un gráfico de dispersión como este permite validar e identificar cuales geomorfositios tienen más relevancia. En el caso de este trabajo da un panorama que permite conocer el estado y representatividad que tienen los geomorfositios a nivel local. Por tal razón, es que se hace evidente la necesidad de que existan herramientas que expongan al público todo lo relacionado con geomorfositios en el país.")


st.subheader("Distribución de geomorfositios por cantón")

#   MAPA
# Cargar los polígonos de cantones
conteo = gpd.read_file(
    "https://raw.githubusercontent.com/dennisperez10/Tarea2/main/geomorfositios_x_canton.gpkg"
)

# Desplegar las primeras filas (sin la columna de geometría)
conteo.drop(columns="geometry").head()

# Remplazar los 0s por valores nulos
import numpy as np

conteo_mapa = conteo.copy()

conteo_mapa["cantidad_geomorfositios"] = (
    conteo_mapa["cantidad_geomorfositios"]
    .replace(0, np.nan)
)

# Crear una versión simplificada para visualización web
conteo_mapa_web = conteo_mapa.copy()

conteo_mapa_web["geometry"] = (
    conteo_mapa_web.geometry.simplify(
        tolerance=0.001,
        preserve_topology=True
    )
)

# Crear un mapa de Costa Rica con el conteo de geomorfositios por cantón
m = folium.Map(location=[9.9, -84.0], zoom_start=8, tiles="CartoDB positron")

# Agregar el mapa de coropletas
choropleth = folium.Choropleth(
    geo_data=conteo_mapa_web,               # capa de geometrías (polígonos de cantones)
    data=conteo_mapa_web,                 # tabla de datos
    columns=["canton", "cantidad_geomorfositios"],  # columnas: clave de unión y valor
    key_on="feature.properties.canton",    # atributo de las geometrías para la unión
    fill_color="Reds",               # paleta de colores
    bins=[1, 2, 4, 10, 30],
    fill_opacity=0.7,
    line_opacity=0.5,
    nan_fill_color="lightgray",        # color para cantones con valores en 0
    #legend_name=""
    )

choropleth.add_to(m)


for key in list(choropleth._children):
    if "color_map" in key:
        del choropleth._children[key]

# Tooltip
folium.GeoJson(
    conteo_mapa_web,
    tooltip=folium.GeoJsonTooltip(
        fields=["canton", "cantidad_geomorfositios"],
        aliases=["Cantón:", "Cantidad de geomorfositios:"]
    ),
    style_function=lambda x: {
        "fillOpacity": 0,
        "color": "transparent",
        "weight": 0
    }
).add_to(m)

# Leyenda

from branca.element import Template, MacroElement

template = """
{% macro html(this, kwargs) %}
<div style="
position: fixed;
bottom: 70px;
left: 20px;
width: 240px;
background-color: rgba(255,255,255,0.95);
border:2px solid #666666;
border-radius: 6px;
padding:12px;
font-size:14px;
font-family: Arial, sans-serif;
color: black;
z-index:9999;
box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
">

<b style="font-size:16px; color:black;">
Cantidad de geomorfositios
</b>

<br><br>

<div>
<i style="background:#fee5d9;
width:18px;height:18px;
display:inline-block;
margin-right:8px;"></i>1 - 2
</div>

<div>
<i style="background:#fcae91;
width:18px;height:18px;
display:inline-block;
margin-right:8px;"></i>2 - 4
</div>

<div>
<i style="background:#fb6a4a;
width:18px;height:18px;
display:inline-block;
margin-right:8px;"></i>4 - 10
</div>

<div>
<i style="background:#cb181d;
width:18px;height:18px;
display:inline-block;
margin-right:8px;"></i>10 - 30
</div>

<div>
<i style="background:lightgray;
border:1px solid black;
width:18px;height:18px;
display:inline-block;
margin-right:8px;"></i>0 geomorfositios
</div>

</div>
{% endmacro %}
"""

macro = MacroElement()
macro._template = Template(template)

m.get_root().add_child(macro)


# Desplegar el mapa
st_folium(
    m,
    width='stretch',
    height=700
)