# handle library selection and recommend new libraries?

import streamlit as st
from streamlit_geolocation import streamlit_geolocation



class LibrarySelector:
    def __init__(self):
        pass

    def render(self):
        # Example list of libraries with their coordinates (latitude, longitude)
        department_libraries_coordinates = {
            "Department of Engineering Library": {
                "min_lat": 52.2010,
                "max_lat": 52.2020,
                "min_lon": 0.1280,
                "max_lon": 0.1290
            },
            "University Library": {
                "min_lat": 52.2013,
                "max_lat": 52.2032,
                "min_lon": 0.1182,
                "max_lon": 0.1215
            },
            "Squire Law Library": {
                "min_lat": 52.2051,
                "max_lat": 52.2065,
                "min_lon": 0.1149,
                "max_lon": 0.1173
            },
            "Seeley Historical Library": {
                "min_lat": 52.2035,
                "max_lat": 52.2055,
                "min_lon": 0.1200,
                "max_lon": 0.1220
            },
            "Moore Library": {
                "min_lat": 52.1973,
                "max_lat": 52.1992,
                "min_lon": 0.1172,
                "max_lon": 0.1192
            },
            "Betty & Gordon Moore Library": {
                "min_lat": 52.2050,
                "max_lat": 52.2070,
                "min_lon": 0.1205,
                "max_lon": 0.1225
            }
        }


        
        library_name = st.selectbox("Select a library:", list(department_libraries_coordinates.keys()))
        st.write(f"You selected: {library_name}")

        location = streamlit_geolocation()
        st.write(location)
        print(location["latitude"]) 

        verif = False
        if department_libraries_coordinates[library_name]["min_lat"] <= location["latitude"] <= department_libraries_coordinates[library_name]["max_lat"] and \
            department_libraries_coordinates[library_name]["min_lon"] <= location["longitude"] <= department_libraries_coordinates[library_name]["max_lon"]:
            verif = True

        st.write(verif)
        # Return the coordinates of the selected library
        return department_libraries_coordinates[library_name]