# display user’s data in table form (check ins, outs, data)

import streamlit as st
# from utils.database import load_checkins, get_user_points

def render():
    user_name = st.text_input("Enter your name to see your records:")
    
    if user_name:
        # checkins_df = load_checkins()  # Load user's check-in data
        user_records = checkins_df[checkins_df["Name"].str.contains(user_name, case=False)]

        if not user_records.empty:
            st.dataframe(user_records)
            # points = get_user_points(user_name)  # Fetch user's accumulated points
            st.write(f"You have accumulated **{points}** points!")
        else:
            st.write("No records found for this user.")
    else:
        st.write("Please enter your name to see your records.")
