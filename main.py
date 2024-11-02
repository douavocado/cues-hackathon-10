import streamlit as st
from components.library_selector import LibrarySelector
from components.location_verifier import verify_location
from components.checkin_handler import CheckInHandler
from logic.classes import Environment, Library, BotPlayer

import random

st.set_option('client.showErrorDetails', False)

def getTestEnv():
    # create test libraries
    libraries = [Library(0, position=(random.random(), random.random())),
                Library(1, position=(random.random(), random.random())),
                Library(2, position=(random.random(), random.random())),
                Library(3, position=(random.random(), random.random())),
                Library(4, position=(random.random(), random.random()))
                ]

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
        st.session_state.env = getTestEnv()

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
