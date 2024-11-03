# display user’s data (check ins, outs, and points)

import streamlit as st
import pandas as pd
import plotly.express as px

def display_player_scores():
    player_scores = st.session_state.env.get_player_scores()
    print("Player Scores:", player_scores)  # Debugging line
    
    if player_scores:
        scores_df = pd.DataFrame(list(player_scores.items()), columns=["Player ID", "Score"])
        print("Scores DataFrame after creation:", scores_df)  # Debugging line

        scores_df["Player ID"] = scores_df["Player ID"].replace({0: "You"})
        scores_df.sort_values(by="Score", ascending=False, inplace=True)
        scores_df['Color'] = scores_df['Player ID'].apply(lambda x: 'red' if x == "You" else 'blue')

        # Store the sorted DataFrame in session state
        st.session_state.scores_df = scores_df
    else:
        st.session_state.scores_df = pd.DataFrame({"Player ID": ["No Players"], "Score": [0], "Color": ["grey"]})

    # Set index for plotting
    scores_df = st.session_state.scores_df
    # scores_df.set_index("Player ID", inplace=True)

    fig = px.bar(scores_df, x=scores_df.index, y='Score', color='Color',
                 color_discrete_map={'red': 'red', 'blue': 'blue', 'grey': 'grey'},
                 title="Player Scores", labels={'Score': 'Score'})

    # Update layout for legend
    fig.update_layout(
        legend_title_text='Player Types',  # Set legend title
        legend=dict(
            itemsizing='constant'  # Maintain consistent item size
        )
    )

    # Add a custom legend item if desired
    fig.for_each_trace(lambda t: t.update(name='You' if t.name == 'red' else 'Others'))  # Set custom names for legend

    st.plotly_chart(fig)

def get_destination_data():
    destinations_dic = st.session_state.env.destination_dic
    data = []
    for dest in destinations_dic.values():
        data.append({"id": dest.id, "latitude": dest.position[0], "longitude": dest.position[1], "score": dest.worth})
    return data

def display_destination_scores_on_map():
    destination_data = get_destination_data()
    df = pd.DataFrame(destination_data)

    df["size"] =  1 - df["score"] / sum(df["score"])  # Scale sizes for visibility
    df["size"] *= 75
    st.map(df, latitude='latitude', longitude='longitude', size='size')


# Plot graphs

st.markdown("<h1 style='text-align: center;'>My Library Records</h1>", unsafe_allow_html=True)

# if st.button("Refresh Data"):
display_player_scores()
st.header("Destination Scores on Map")
display_destination_scores_on_map()

# display_player_scores() 

# # Call the function to display the map

# display_destination_scores_on_map()


# stock market visualisation of values of each library
# plot score per library over time