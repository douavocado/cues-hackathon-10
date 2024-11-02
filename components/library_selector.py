# handle library selection and recommend new libraries?

import streamlit as st
from components.library_coordinates import department_libraries_coordinates


class LibrarySelector:
    def __init__(self):
        pass

    def render(self):
        # Example list of libraries with their coordinates (latitude, longitude)
       

        library_name = st.selectbox("Select a library:", list(department_libraries_coordinates.keys()))
        #st.write(f"You selected: {library_name}")

        # Return the coordinates of the selected library
        return library_name