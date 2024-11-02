# verify user's location using GPS
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from components.library_coordinates import department_libraries_coordinates


def verify_location(library_name):
    st.write("Verify location:")
    location = streamlit_geolocation()

    verif = False
    if department_libraries_coordinates[library_name]["min_lat"] <= location["latitude"] <= department_libraries_coordinates[library_name]["max_lat"] and \
        department_libraries_coordinates[library_name]["min_lon"] <= location["longitude"] <= department_libraries_coordinates[library_name]["max_lon"]:
        verif = True

    st.write(verif)
    return verif