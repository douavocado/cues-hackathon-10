# display user’s data (check ins, outs, and points)

import streamlit as st
from components.checkin_summary import render as checkin_summary

def render():
    st.header("My Library Records")
    checkin_summary.render()  # Render the check-in summary component
