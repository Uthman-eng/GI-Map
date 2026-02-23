import folium as fm
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd


# my module code
from folium_map import build_folium_map

st.set_page_config(layout="wide")
st.title("GI Borehole Table")


df = pd.read_excel("GI Locations.xlsx", header= 0)
st.write("Note: information is given in easting and northing, things are plotted in Lat and Long",df)
