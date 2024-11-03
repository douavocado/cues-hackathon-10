import streamlit as st

from components.library_selector import LibrarySelector
from components.library_coordinates import department_libraries_coordinates
from components.checkin_handler import CheckInHandler
from logic.classes import Environment, Library, HumanPlayer, BotPlayer

import numpy as np
import random
import threading

st.set_option('client.showErrorDetails', False)


def main():
    pages = {"Home" : [st.Page(r"pages\track_time.py", title="Track Time"), st.Page(r"pages\my_records.py", title="My Records"),st.Page(r"pages\store.py", title="Store")]}
    pg = st.navigation(pages)
    pg.run()


if __name__ == "__main__":
    main()
