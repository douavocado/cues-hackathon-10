import streamlit as st
from components.library_selector import LibrarySelector
from components.checkin_handler import render as checkin_handler


def main():
    # Set the title of the app
    st.title("Cambridge Library Monopoly")
    st.header("Select a Library and Check In/Out")


    # Render the library selector component
    library_selector = LibrarySelector()
    library_coords = library_selector.render()  # This should return the coordinates of the selected library


    if library_coords:
        # If a library is selected, render the check-in/out handler
        checkin_handler(library_coords)


if __name__ == "__main__":
    main()