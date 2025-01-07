
import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from geopy.distance import geodesic

# Function to load data from disability centers
def load_centros(filepath):
    try:
        return pd.read_csv(filepath, sep=';', encoding='utf-8')
    except pd.errors.ParserError as e:
        print(f"Error reading the file {filepath}: {e}")
        return pd.read_csv(filepath, sep=';', encoding='utf-8', error_bad_lines=False)

# Function to split the 'geo_point_2d' column into 'x' and 'y'
def split_geo_point(df):
    if 'geo_point_2d' not in df.columns:
        raise KeyError("The 'geo_point_2d' column is not present in the DataFrame")
    df[['y', 'x']] = df['geo_point_2d'].str.split(',', expand=True).astype(float)
    return df

# Load data for disability centers
centros_fisica = load_centros('discapacitat-fisica-discapacidad-fisica.csv')
centros_fisica = split_geo_point(centros_fisica)

centros_sensorial = load_centros('discapacitat-sensorial-discapacidad-sensorial.csv')
centros_sensorial = split_geo_point(centros_sensorial)

centros_intelectual = load_centros('discapacitat-intellectual-discapacidad-intelectual.csv')
centros_intelectual = split_geo_point(centros_intelectual)

# Load data for reduced mobility parkings
parkings_mr = load_centros('aparcaments-persones-mobilitat-reduida-aparcamientos-personas-movilidad-reducida.csv')
parkings_mr = split_geo_point(parkings_mr)

# Streamlit page configuration
st.set_page_config(page_title="Disability Centers and Parkings", layout="wide")

# App title
st.title("Disability Centers and Reduced Mobility Parkings")

# App description
st.markdown("""
This application helps you find disability centers and nearby reduced mobility parkings.
You can search for a specific center and view nearby parkings and estimated routes.
""")

# Sidebar: Search type selection
search_type = "Specific Center"

# Sidebar: Disability type selector
disability_type = st.sidebar.selectbox("Select the type of disability", ["physical", "sensory", "intellectual"])

# Filter data based on disability type
if disability_type == "physical":
    centers = centros_fisica
elif disability_type == "sensory":
    centers = centros_sensorial
else:
    centers = centros_intelectual

# Search radius
search_radius = st.sidebar.slider("Search radius (meters)", min_value=50, max_value=2000, step=50, value=500)

# Function to find nearby parkings
def find_nearby_parkings(centers, parkings, radius, selected_center_coords):
    nearby_parkings = []
    for _, parking in parkings.iterrows():
        parking_coords = tuple(map(float, parking['geo_point_2d'].split(',')))
        distance = geodesic(selected_center_coords, parking_coords).meters
        if distance <= radius:
            nearby_parkings.append(parking)

    if nearby_parkings:
        return pd.DataFrame(nearby_parkings).drop_duplicates()
    else:
        return pd.DataFrame(columns=['Nombre Places / Número Plazas', 'geo_point_2d'])  # Return an empty DataFrame if no parkings are found

# Show results for specific center
selected_center_name = st.sidebar.selectbox("Select the center", centers['equipamien'].unique())
selected_center_coords = centers.loc[centers['equipamien'] == selected_center_name, ['y', 'x']].iloc[0]
nearby_parkings = find_nearby_parkings(centers, parkings_mr, search_radius, selected_center_coords)

# Create the map
m = folium.Map(location=[selected_center_coords.iloc[0], selected_center_coords.iloc[1]], zoom_start=14)

# Add the selected center to the map
folium.Marker(
    location=selected_center_coords,
    popup=f"{selected_center_name}",
    icon=folium.Icon(color='blue', icon='info-sign', prefix='fa')
).add_to(m)

# Add parkings to the map
parkings_cluster = MarkerCluster(name="Reduced Mobility Parkings").add_to(m)
for _, parking in nearby_parkings.iterrows():
    folium.Marker(
        location=tuple(map(float, parking['geo_point_2d'].split(','))),
        popup=f"Parking - {parking['Nombre Places / Número Plazas']}",
        icon=folium.Icon(color='green', icon='car', prefix='fa')
    ).add_to(parkings_cluster)

# Display the map in Streamlit
folium_static(m)

# Display data in table
st.subheader("Nearby Parkings")
if not nearby_parkings.empty:
    st.dataframe(nearby_parkings[['Nombre Places / Número Plazas', 'geo_point_2d']])
else:
    st.info("No nearby parkings found.")