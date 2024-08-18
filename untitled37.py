# Initialize Streamlit app
st.set_page_config(layout="wide")

# Dashboard Title
st.title("Football Player Performance Dashboard")

def load_data(data_file):
    """Loads data from an uploaded file, handling potential errors.

    Args:
        data_file: The uploaded file object.

    Returns:
        A pandas DataFrame if successful, otherwise None.
    """
    try:
        df = pd.read_csv(data_file)
        # Check if 'league_id' column exists after loading
        if 'league_id' not in df.columns:
            st.error("Error: 'league_id' column not found in the CSV file.")
            return None
        return df
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file")

if uploaded_file is not None:
    # Load the data
    df = load_data(uploaded_file)

    if df is not None:
        # Sidebar for filters
        st.sidebar.header("Filter Players")
        selected_league = st.sidebar.selectbox("Select League", df['league_name'].unique())
        selected_club = st.sidebar.selectbox("Select Club", df[df['league_name'] == selected_league]['club_name'].unique())
        selected_position = st.sidebar.selectbox("Select Position", df['club_position'].unique())

        # Filter the dataframe based on selections
        filtered_df = df[(df['league_name'] == selected_league) &
                         (df['club_name'] == selected_club) &
                         (df['club_position'] == selected_position)]

        # Display basic player statistics
        st.header(f"Player Statistics for {selected_club} in {selected_league}")
        st.dataframe(filtered_df[['short_name', 'age', 'overall', 'potential', 'value_eur', 'wage_eur', 'height_cm', 'weight_kg']])

        # Player performance overview
        st.subheader("Player Performance Overview")
        metrics = ['overall', 'potential', 'pace', 'shooting', 
                   'passing', 'dribbling', 'defending', 'physic']

        for metric in metrics:
            st.bar_chart(filtered_df[['short_name', metric]].set_index('short_name'))

        # Country-wise analysis
        st.subheader("Country-wise Analysis")
        country_data = df.groupby('nationality_name')[metrics].mean().reset_index()

        # Visualize overall performance by country
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='nationality_name', y='overall', data=country_data, ax=ax)
        ax.set_title("Overall Performance by Country")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        st.pyplot(fig)

        # Individual Player Analysis
        st.subheader("Individual Player Analysis")
        selected_player = st.selectbox("Select Player", filtered_df['short_name'])
        player_data = filtered_df[filtered_df['short_name'] == selected_player].iloc[0]
        st.write(player_data)

        # Detailed Player Metrics
        st.subheader("Detailed Player Metrics")
        metrics_detailed = ['attacking_crossing', 'attacking_finishing', 'attacking_heading_accuracy',
                            'attacking_short_passing', 'attacking_volleys', 'skill_dribbling', 'skill_curve',
                            'skill_fk_accuracy', 'skill_long_passing', 'skill_ball_control', 'movement_acceleration',
                            'movement_sprint_speed', 'movement_agility', 'movement_reactions', 'movement_balance',
                            'power_shot_power', 'power_jumping', 'power_stamina', 'power_strength', 'power_long_shots',
                            'mentality_aggression', 'mentality_interceptions', 'mentality_positioning', 'mentality_vision',
                            'mentality_penalties', 'mentality_composure', 'defending_marking_awareness', 
                            'defending_standing_tackle', 'defending_sliding_tackle']

        st.write(player_data[metrics_detailed])

        # Suggestions for Improvement
        st.subheader("Suggestions for Improvement")
        improvement_areas = ['weak_foot', 'skill_moves', 'international_reputation', 
                             'attacking_crossing', 'mentality_vision']
        st.write(player_data[improvement_areas])

        # Conclusion
        st.markdown("""
        ### Conclusion
        This dashboard provides a comprehensive view of player performance across various metrics. Managers can use it to make data-driven decisions, track player development, and identify areas for improvement.
        """)

else:
    st.info("Please upload a CSV file to proceed.")
