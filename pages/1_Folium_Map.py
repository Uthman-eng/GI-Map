import folium as fm
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd


# my module code
from folium_map import build_folium_map

st.set_page_config(layout="wide")
st.title("GI Map ")


m = build_folium_map()
st.components.v1.html(m.get_root().render(), height=850)
