import streamlit as st
from components.library_selector import LibrarySelector
from components.library_coordinates import department_libraries_coordinates
from components.checkin_handler import CheckInHandler
from logic.classes import Environment, Library, BotPlayer


st.set_option('client.showErrorDetails', False)

def initEnv():
    libraries = []
    for lib_name, lib_coords in department_libraries_coordinates.items():
        lat = (lib_coords['min_lat'] + lib_coords['max_lat']) / 2
        lon = (lib_coords['min_lon'] + lib_coords['max_lon']) / 2
        libraries.append(Library(lib_name, (lat, lon)))

    # create test players
    total_players = 1000
    players = []
    for id_ in range(total_players):
        players.append(BotPlayer(id_))
        
    # create environment
    env = Environment(destinations=libraries, players=players)
    return env

def main():
    st.title("Cambridge Exchange")
    st.header("Select a Location and Check In/Out")
    
    if "env" not in st.session_state:
        st.session_state.env = initEnv()

    # Initialize library selector and check-in handler only once
    if "library_selector" not in st.session_state:
        st.session_state.library_selector = LibrarySelector()
    if "checkin_handler" not in st.session_state:
        st.session_state.checkin_handler = CheckInHandler()

    library_name = st.session_state.library_selector.render()
    if library_name:
        st.session_state.checkin_handler.render(library_name)
    

if __name__ == "__main__":
    main()
