import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.set_page_config(layout="wide")
st.title("🚀 My Lightweight Geo-App")

# Load sample data
@st.cache_data
def get_data():
    url = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/countries.geojson"
    data = gpd.read_file(url)
    return data

gdf = get_data()

# --- SMART COLUMN PICKER ---
# This looks for the most likely 'name' column in the dataset
possible_name_cols = ['name', 'NAME', 'admin', 'ADMIN', 'label']
name_col = next((col for col in possible_name_cols if col in gdf.columns), gdf.columns[0])
# ---------------------------

# Sidebar UI
st.sidebar.title("Controls")
st.sidebar.info(f"Using column: '{name_col}' for names")

# Create a list of countries for the dropdown
country_list = sorted(gdf[name_col].unique().tolist())
selected_country = st.sidebar.selectbox("Find a Country", country_list)

# Filter data based on selection
filtered_gdf = gdf[gdf[name_col] == selected_country]

# Map Setup
m = leafmap.Map(center=[20, 0], zoom=2)
m.add_gdf(gdf, layer_name="World", style={'fillOpacity': 0.1, 'color': 'gray'})
m.add_gdf(filtered_gdf, layer_name="Selection", style={'color': 'red', 'fillOpacity': 0.5})

# Launch Map
m.to_streamlit(height=600)

st.write(f"Currently inspecting: **{selected_country}**")

# Show raw data for debugging if needed
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader("Raw Data Preview")
    st.write(gdf.head())
