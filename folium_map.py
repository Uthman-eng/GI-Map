import folium
from folium.plugins import MarkerCluster, Draw, MeasureControl 
import streamlit as st
from streamlit_folium import st_folium


from pyproj import Transformer
import pandas as pd



# easting northing to lat lon conversion - kept simple and not in the class for now
def to_lat_lon(easting, northing):
    t = Transformer.from_crs("epsg:27700", "epsg:4326", always_xy=True)  # <-- always_xy
    lon, lat = t.transform(easting, northing)
    return lat, lon

# class
class Markers():
    def __init__(self, m, ID, easting, northing, colour, comment, coords_are_latlon=False):
        self.m = m
        self.easting = float(easting)
        self.northing = float(northing)
        self.ID = ID
        self.colour = colour
        self.comment = comment
        self.coords_are_latlon = coords_are_latlon  # <-- lets you reuse class for both cases

    def plotting(self, group=None):  # <-- add self, optional are already lat/lon, skip conversion
        if self.coords_are_latlon:
            lat, lon = self.easting, self.northing
        else:
            lat, lon = to_lat_lon(self.easting, self.northing)
            
        marker = folium.Marker(
            location=[lat, lon],
            popup=f"{self.ID} \nComments: {self.comment}",
            icon=folium.Icon(color=self.colour)
        )

        # Add to a FeatureGroup/Cluster if provided, otherwise directly to mapi fe
        if group is None:
            marker.add_to(self.m)
        else:
            marker.add_to(group)


def plot_data(m):
    # Groups 
    BH_group = folium.FeatureGroup("BH")
    TP_group = folium.FeatureGroup("TP")
    WS_group = folium.FeatureGroup("WS")

    # GI Data for BH, TP, WS processing - adding markers to infomration from excel  
    GI_Data = pd.read_excel('input_info/GI_Data.xlsx', header=0)

    BH_data = GI_Data.filter(like="BH")
    TP_data = GI_Data.filter(like="TP")
    WS_data = GI_Data.filter(like="WS")

    # Plotting markers for BH, TP, WS 
    if BH_data.dropna(how="all").empty:
        print("BH is empty (no data)")
    else:
        for r in BH_data.itertuples(index=False):
            Markers(m, r.BH_ID, r.BH_Easting, r.BH_Northing, "red", r.BH_Comments, False).plotting(group=BH_group)
        BH_group.add_to(m)

    if TP_data.dropna(how="all").empty:
        print("TP is empty (no data)")
    else:
        for r in TP_data.itertuples(index=False):
            Markers(m, r.TP_ID, r.TP_Easting, r.TP_Northing, "blue", r.TP_Comments, False).plotting(group=TP_group)
        TP_group.add_to(m)

    if WS_data.dropna(how="all").empty:
        print("WS is empty (no data)")
    else:
        for r in WS_data.itertuples(index=False):
            Markers(m, r.WS_ID, r.WS_Easting, r.WS_Northing, "green", r.WS_Comments, False).plotting(group=WS_group)
        WS_group.add_to(m)

    return m 








def build_folium_map():
    # can also use:  "OpenStreetMap (normal google maps style), "Cartodb Positron (light)", "Stamen Terrain", "Stamen Toner" (black and white), "Cartodb dark_matter" (dark)
    m = folium.Map(location=[53.239, -1.425], tiles="OpenStreetMap", zoom_start=13)

    plot_data(m)

    # drawing ability to draw and export
    Draw(export=False).add_to(m)

    # lat lon popup on click
    m.add_child(folium.LatLngPopup())


    # measurement tool 
    m.add_child(MeasureControl())

    # searcher:
    folium.plugins.Geocoder().add_to(m)


    # IMPORTANT: add LayerControl BEFORE rendering
    folium.LayerControl(collapsed=False).add_to(m)
    # Render ONCE
    c1, c2 = st.columns(2)
    with c1:
        output = st_folium(m, width=100, height=500, key="gi_map")
    with c2:
        st.write(output)   

    return m  

if __name__ == "__main__":
    m = build_folium_map()
    # m.save("map.html") 