import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize Streamlit app
st.set_page_config(layout="wide")

# Provide the URL to your CSV file on GitHub
data_url = "https://github.com/anish045007/RWAP_5/blob/main/output_male_football_player.csv"

# Load your dataset with error handling
try:
    df = pd.read_csv(data_url)
except pd.errors.ParserError as e:
    st.error(f"Error parsing CSV: {e}")
    st.stop()  # Stop the app if there's a parsing error

# Dashboard Title
st.title("Football Player Performance Dashboard")

# Sidebar for filters
st.sidebar.header("Filter Players")
selected_league = st.sidebar.selectbox("Select League", df['league_id'].unique())
selected_club = st.sidebar.selectbox("Select Club", df[df['league_id'] == selected_league]['club_team_id'].unique())
selected_position = st.sidebar.selectbox("Select Position", df['club_position_oe'].unique())

# Filter the dataframe
filtered_df = df[(df['league_id'] == selected_league) &
                 (df['club_team_id'] == selected_club) &
                 (df['club_position_oe'] == selected_position)]

# Display the filtered dataframe
st.header(f"Player Statistics for {selected_club} in {selected_league}")
st.write(filtered_df)

# Player performance overview
st.subheader("Player Performance Overview")
metrics = ['overall_mmnorm', 'potential_mmnorm', 'pace_mmnorm', 'shooting_mmnorm',
          'passing_mmnorm', 'dribbling_mmnorm', 'defending_mmnorm', 'physic_mmnorm']
for metric in metrics:
    st.bar_chart(filtered_df[metric])

# Country-wise analysis
st.subheader("Country-wise Analysis")
country_data = df.groupby('nationality_id')[metrics].mean().reset_index()
st.dataframe(country_data)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='nationality_id', y='overall_mmnorm', data=country_data, ax=ax)
ax.set_title("Overall Performance by Country")
st.pyplot(fig)

# Individual Player Analysis
st.subheader("Individual Player Analysis")
selected_player = st.selectbox("Select Player", filtered_df.index)
player_data = filtered_df.loc[selected_player]
st.write(player_data)

# Suggestions for Improvement
st.subheader("Suggestions for Improvement")
improvement_areas = ['weak_foot', 'skill_moves', 'international_reputation',
                      'attacking_crossing_mmnorm', 'mentality_vision_mmnorm']
st.write(player_data[improvement_areas])

# Conclusion
st.markdown("""
### Conclusion
This dashboard allows managers to gain insights into the performance of players across various metrics. The country-wise analysis helps in comparing players on a global scale, while the individual analysis aids in tracking and improving specific players' skills.
""")
