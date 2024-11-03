import streamlit as st

from components.library_selector import LibrarySelector
from components.library_coordinates import department_libraries_coordinates
from components.checkin_handler import CheckInHandler
from logic.classes import Environment, Library, HumanPlayer, BotPlayer

import numpy as np
import random
import threading
import time

st.set_option('client.showErrorDetails', False)

def initEnv():
    prop_adaptive = 0.3
    total_players = 20

    libraries = []
    for lib_name, lib_coords in department_libraries_coordinates.items():
        lat = (lib_coords['min_lat'] + lib_coords['max_lat']) / 2
        lon = (lib_coords['min_lon'] + lib_coords['max_lon']) / 2
        libraries.append(Library(lib_name, (lat, lon)))

    # create human and test players
    players = [HumanPlayer(0, (0,0))]
    for id_ in range(1, total_players):
        if np.random.random() < prop_adaptive:
            players.append(BotPlayer(id_, base_location=(random.randint(0,20), random.randint(0,20)), adaptive= True, keenness=random.randint(1,10), stay_keenness=random.randint(1,10)))
        else:
            players.append(BotPlayer(id_, base_location=(random.randint(0,20), random.randint(0,20)), adaptive= False, keenness=random.randint(1,10), stay_keenness=random.randint(1,10)))
        
    # create environment
    env = Environment(destinations=libraries, players=players)
    return env


def main():
    st.logo("images\CUExLong.png", size="large")
    pages = {"Home" : [st.Page(r"pages\track_time.py", title="Track Time"), st.Page(r"pages\my_records.py", title="My Records"),st.Page(r"pages\store.py", title="Store")]}
    pg = st.navigation(pages)
    pg.run()
    

if __name__ == "__main__":
    main()
