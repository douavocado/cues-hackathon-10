# verify user's location using GPS
import streamlit as st
from components.library_coordinates import department_libraries_coordinates
from streamlit_js_eval import get_geolocation

def verify_location(library_name):
    location = get_geolocation()
    print(location)

    # FOR TESTING:
    # location['coords']['latitude'] = 52.202
    # location['coords']['longitude'] = 0.119
    
    verif = False
    if location is not None:
        if department_libraries_coordinates[library_name]["min_lat"] <= location['coords']['latitude'] <= department_libraries_coordinates[library_name]["max_lat"] and \
            department_libraries_coordinates[library_name]["min_lon"] <= location['coords']['longitude'] <= department_libraries_coordinates[library_name]["max_lon"]:
            verif = True

    return verif