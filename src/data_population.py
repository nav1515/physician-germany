# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
import geopandas as gpd
from shapely.geometry import Point
import folium

# First some MPG Data Exploration
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

df_raw = load_data(path="../data/plz-5stellig-daten.csv")
df = deepcopy(df_raw)
plz_datentyp = df['plz'].dtype

munich_df = df[df['plz'].between(80000, 81999)]



# Füge eine neue Spalte "Density" hinzu
munich_df['Density'] = munich_df['einwohner'] / munich_df['qkm']

munich_df.to_csv('../data/munich_pop.csv', index=False)
munich_df.head()

# Add title and header
st.title("Population in Munich")

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Dataframe"):
    st.subheader("This is our dataset:")
    st.dataframe(data=munich_df)
    # st.table(munich_df)

#munich_geojson = gpd.read_file("../data/plz-5stellig-daten.geojson")

# Füge die Bevölkerungsdichte zum GeoDataFrame hinzu (ersetze 'Density' durch den richtigen Spaltennamen)
#munich_geojson['Density'] = munich_df['Density']

# Erstelle eine benutzerdefinierte Karte mit Folium und GeoPandas
#munich_map = folium.Map(location=[munich_geojson['Latitude'].mean(), munich_geojson['Longitude'].mean()], zoom_start=11)

# Hinzufügen von GeoJSON-Daten mit Bevölkerungsdichte zur Karte
# folium.Choropleth(
#     geo_data=munich_geojson,
#     name='choropleth',
#     data=munich_geojson,
#     columns=['PLZ', 'Density'],
#     key_on='feature.properties.PLZ',
#     fill_color='YlGnBu',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Population Density'
# ).add_to(munich_map)

# # Streamlit-Anzeige der Karte
# st.subheader("Bevölkerungsdichte in München")
# st.pydeck_chart(munich_map)