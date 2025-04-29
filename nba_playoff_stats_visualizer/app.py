import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from playoff_stats_finder import TeamGameFinder


def app():
    """
    Main application function that renders the NBA Playoff Stats Visualizer.
    """
    # Set page configuration
    st.set_page_config(
        page_title="NBA Playoff Stats Visualizer",
        page_icon="🏀",
        layout="wide"
    )

    # Title and description
    st.title("Enhance Your Sports Betting Stategy - NBA Playoff Statistics Visualizer")

    # Add detailed instructions about the application
    st.markdown("""
    <div style="font-size: 18px;">
    <h3 style="font-size: 28px;">🏀 Real-Time NBA Stats for Smarter Betting Decisions </h3>
    
    <p>This tool provides <strong>real-time NBA statistical data</strong> designed specifically to help sports bettors gain valuable insights on team and player performance throughout the playoffs. All visualizations are based on official NBA data to ensure accuracy. ⚡</p>
    
    <p><strong>How to use this tool:</strong></p>
    <ul>
    <li>🔍 Select a season and team from the sidebar to load their playoff statistics</li>
    <li>📈 Analyze team performance trends and individual player contributions</li>
    <li>🎯 Identify betting opportunities based on historical performance patterns</li>
    <li>💰 Make more informed decisions for player props and team bets</li>
    </ul>
    
    <p><strong>💡 Pro Tip:</strong> All charts are fully interactive! Click on legends to toggle specific data on/off, hover over data points for detailed information, and zoom in on areas of interest by clicking and dragging.</p>
    
    <p><em>🚀 This is the same tool I personally use when placing bets, now released for public use. Enjoy! 🏆</em></p>
    
    <hr>
    
    <p>📣 <strong>We're committed to continuous improvement!</strong> This tool will be actively updated with new features and data. The feedback section will be open soon, allowing you to help shape the future of this betting tool. Your insights matter! 🔄</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for selections
    st.sidebar.header("Selection Options")

    # Season selection - NBA seasons typically span two years
    seasons = [f"{year}-{str(year + 1)[-2:]}" for year in range(2015, 2025)]
    selected_season = st.sidebar.selectbox(
        "Select Season", seasons, index=len(seasons) - 1)

    # Team selection
    team_names = {
        'Atlanta Hawks': 'ATL', 'Brooklyn Nets': 'BKN', 'Boston Celtics': 'BOS',
        'Charlotte Hornets': 'CHA', 'Chicago Bulls': 'CHI', 'Cleveland Cavaliers': 'CLE',
        'Dallas Mavericks': 'DAL', 'Denver Nuggets': 'DEN', 'Detroit Pistons': 'DET',
        'Golden State Warriors': 'GSW', 'Houston Rockets': 'HOU', 'Indiana Pacers': 'IND',
        'LA Clippers': 'LAC', 'Los Angeles Lakers': 'LAL', 'Memphis Grizzlies': 'MEM',
        'Miami Heat': 'MIA', 'Milwaukee Bucks': 'MIL', 'Minnesota Timberwolves': 'MIN',
        'New Orleans Pelicans': 'NOP', 'New York Knicks': 'NYK', 'Oklahoma City Thunder': 'OKC',
        'Orlando Magic': 'ORL', 'Philadelphia 76ers': 'PHI', 'Phoenix Suns': 'PHX',
        'Portland Trail Blazers': 'POR', 'Sacramento Kings': 'SAC', 'San Antonio Spurs': 'SAS',
        'Toronto Raptors': 'TOR', 'Utah Jazz': 'UTA', 'Washington Wizards': 'WAS'
    }
    selected_team_name = st.sidebar.selectbox(
        "Select Team", list(team_names.keys()))
    selected_team = team_names[selected_team_name]

    # Add a feedback section to the sidebar (greyed out - coming soon)
    st.sidebar.markdown("---")  # Add a separator
    st.sidebar.header("Leave Feedback")
    st.sidebar.markdown(
        "<div style='color: gray; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'>"
        "<p style='margin-bottom: 10px;'><b>Feedback Feature - Coming Soon!</b></p>"
        "<p>We're currently working on implementing a feedback system to improve your experience.</p>"
        "</div>",
        unsafe_allow_html=True
    )

    # Add loading indicator
    with st.spinner("Fetching playoff statistics..."):
        try:
            # Get data using the existing TeamGameFinder
            finder = TeamGameFinder()
            team_stats = finder.get_team_games(selected_team, selected_season)

            # If we found data
            if team_stats:
                # Convert player stats to DataFrame for easier manipulation
                all_player_games = []
                for player_name, games in team_stats.items():
                    for game in games:
                        game_data = {
                            'Player': player_name,
                            'Game Date': game.game_date,
                            'Matchup': game.matchup,
                            'Points': game.points,
                            'Rebounds': game.rebounds,
                            'Assists': game.assists,
                            'Threes Made': game.threes_made,
                            'Minutes': game.minutes
                        }
                        all_player_games.append(game_data)

                df = pd.DataFrame(all_player_games)

                # Extract opponent from matchup
                df['Home Team'] = df['Matchup'].apply(
                    lambda x: x.split(' ')[0])
                df['Away Team'] = df['Matchup'].apply(
                    lambda x: x.split(' ')[-1])
                df['Opponent'] = df.apply(
                    lambda row: row['Away Team'] if row['Home Team'] == selected_team else row['Home Team'], axis=1)

                # Convert game date to datetime for sorting
                df['Game Date'] = pd.to_datetime(df['Game Date'])
                df = df.sort_values('Game Date')

                # Group by unique game dates and assign game numbers
                unique_game_dates = df['Game Date'].unique()
                game_date_to_number = {date: i + 1 for i,
                                       date in enumerate(unique_game_dates)}
                df['Game Number'] = df['Game Date'].map(game_date_to_number)

                # Extract numeric minutes - handle potential format issues
                def extract_minutes(min_str):
                    try:
                        if pd.isna(min_str):
                            return 0
                        min_str = str(min_str)
                        if ':' in min_str:
                            mins, secs = min_str.split(':')
                            return float(mins) + float(secs) / 60
                        elif min_str.replace('.', '', 1).isdigit():
                            return float(min_str)
                        else:
                            return 0
                    except:
                        return 0

                df['Minutes Played'] = df['Minutes'].apply(extract_minutes)

                # Display data overview
                st.header(
                    f"{selected_team_name} Playoff Performance ({selected_season})")

                st.subheader("Series Overview")
                series_info = df[['Game Date', 'Matchup', 'Opponent']
                                 ].drop_duplicates().reset_index(drop=True)
                series_info['Game Date'] = series_info['Game Date'].dt.strftime(
                    '%Y-%m-%d')

                # Use Plotly table
                fig = go.Figure(data=[go.Table(
                    header=dict(values=list(series_info.columns),
                                fill_color='paleturquoise',
                                align='left'),
                    cells=dict(values=[series_info[col] for col in series_info.columns],
                               fill_color='lavender',
                               align='left'))
                ])
                fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
                st.plotly_chart(fig)

                col1, col2 = st.columns(2)
                with col1:
                    # Total points by player
                    player_totals = df.groupby('Player').agg({
                        'Points': 'sum',
                        'Rebounds': 'sum',
                        'Assists': 'sum',
                        'Threes Made': 'sum',
                        'Minutes Played': 'sum'
                    }).sort_values('Points', ascending=False)

                    # Total points by player, broken down by game
                    st.subheader("Top Scorers by Game")

                    # Get the top 10 scorers overall
                    top_scorers = player_totals.nlargest(
                        10, 'Points').index.tolist()

                    # Filter for only those top players
                    top_scorers_df = df[df['Player'].isin(top_scorers)]

                    # Create a mapping from game number to game date for better labels
                    game_date_map = df.drop_duplicates(
                        'Game Number')[['Game Number', 'Game Date']]
                    game_date_map['Game Date'] = game_date_map['Game Date'].dt.strftime(
                        '%Y-%m-%d')
                    game_date_map = dict(
                        zip(game_date_map['Game Number'], game_date_map['Game Date']))

                    # Create a pivot table with players as rows and games as columns
                    player_game_points = pd.pivot_table(
                        top_scorers_df,
                        values='Points',
                        index=['Player'],
                        columns=['Game Number'],
                        aggfunc='sum',
                        fill_value=0
                    )

                    # Convert to long format for plotly
                    player_game_points_long = player_game_points.reset_index().melt(
                        id_vars=['Player'],
                        var_name='Game Number',
                        value_name='Points'
                    )

                    # Add game dates for display
                    player_game_points_long['Game Date'] = player_game_points_long['Game Number'].map(
                        game_date_map)

                    # Sort players by total points descending
                    player_order = player_totals.loc[top_scorers].sort_values(
                        'Points', ascending=False).index.tolist()
                    player_game_points_long['Player'] = pd.Categorical(
                        player_game_points_long['Player'],
                        categories=player_order,
                        ordered=True
                    )

                    # Sort by Player (categorical) and Game Number (ascending)
                    # This ensures the latest games (highest game numbers) are at the bottom of each stack
                    player_game_points_long = player_game_points_long.sort_values(
                        ['Player', 'Game Number'], ascending=[True, False])
                    # Create stacked bar chart
                    fig = px.bar(
                        player_game_points_long,
                        x='Player',
                        y='Points',
                        color='Game Date',  # Use Game Date instead of Game Number for legend
                        labels={'Points': 'Points Scored',
                                'Player': 'Player', 'Game Date': 'Game Date'}
                    )

                    # Customize layout
                    fig.update_layout(
                        xaxis_title="Player",
                        yaxis_title="Total Points",
                        legend_title="Game Date",
                        barmode='stack'
                    )

                    st.plotly_chart(fig)

                with col2:
                    st.subheader("Points Distribution by Player")

                    fig = px.pie(df, values='Points', names='Player', hole=0.3,
                                 color_discrete_sequence=px.colors.sequential.Reds[::-1])

                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig)

                # Game-by-Game stat leaders
                st.header("Game-by-Game Statistical Leaders")

                # game_dates = df['Game Date'].unique()
                game_dates = df['Game Date'].dt.strftime(
                    '%Y-%m-%d').unique()
                selected_game = st.selectbox("Select Game Date", game_dates)

                game_df = df[df['Game Date'] == selected_game]

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.subheader("Points Leaders")
                    points_leaders = game_df.sort_values(
                        'Points', ascending=False).head(5)
                    fig = px.bar(points_leaders, x='Player',
                                 y='Points', color='Points',
                                 color_continuous_scale='Reds')
                    st.plotly_chart(fig)

                with col2:
                    st.subheader("Rebounds Leaders")
                    reb_leaders = game_df.sort_values(
                        'Rebounds', ascending=False).head(5)
                    fig = px.bar(reb_leaders, x='Player',
                                 y='Rebounds', color='Rebounds',
                                 color_continuous_scale='Blues')
                    st.plotly_chart(fig)

                with col3:
                    st.subheader("Assists Leaders")
                    ast_leaders = game_df.sort_values(
                        'Assists', ascending=False).head(5)
                    fig = px.bar(ast_leaders, x='Player',
                                 y='Assists', color='Assists',
                                 color_continuous_scale='Greens')
                    st.plotly_chart(fig)

                # Game-by-Game Analysis
                st.header("Game-by-Game Analysis")

                # Add a selector for the statistic to display
                stat_option = st.radio(
                    "Select statistic to analyze:",
                    ["Points", "Rebounds", "Assists", "3-Points", "Points+Rebounds",
                     "Points+Rebounds+Assists (PRA)"],
                    horizontal=True
                )

                # Handle 3-points data
                if stat_option == "3-Points":
                    df['threes_made'] = df['Threes Made']
                    display_stat = 'threes_made'
                    color_scale = 'Oranges'
                    title_prefix = '3-Points'
                elif stat_option == "Points+Rebounds":
                    # Calculate Points+Rebounds
                    df['PR'] = df['Points'] + df['Rebounds']
                    display_stat = 'PR'
                    color_scale = 'Purples'
                    title_prefix = 'Points+Rebounds'
                elif stat_option == "Points+Rebounds+Assists (PRA)":
                    # Calculate PRA
                    df['PRA'] = df['Points'] + df['Rebounds'] + df['Assists']
                    display_stat = 'PRA'
                    color_scale = 'Viridis'
                    title_prefix = 'Points+Rebounds+Assists'
                elif stat_option == "Assists":
                    display_stat = 'Assists'
                    color_scale = 'Greens'
                    title_prefix = 'Assists'
                elif stat_option == "Points":
                    display_stat = 'Points'
                    color_scale = 'Reds'
                    title_prefix = 'Points'
                else:  # Rebounds
                    display_stat = 'Rebounds'
                    color_scale = 'Blues'
                    title_prefix = 'Rebounds'

                # Identify top 10 players by the selected statistic
                if stat_option == "Points+Rebounds+Assists (PRA)":
                    player_stat_totals = df.groupby(
                        'Player')['PRA'].sum().sort_values(ascending=False)
                elif stat_option == "Points+Rebounds":
                    player_stat_totals = df.groupby(
                        'Player')['PR'].sum().sort_values(ascending=False)
                elif stat_option == "3-Points":
                    player_stat_totals = df.groupby(
                        'Player')['threes_made'].sum().sort_values(ascending=False)
                else:
                    player_stat_totals = player_totals[display_stat].sort_values(
                        ascending=False)

                top_players = player_stat_totals.head(10).index.tolist()

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader(f"Top Players' {title_prefix} by Game")
                    top_players_df = df[df['Player'].isin(top_players)]

                    # Determine which hover data to show based on the selected stat
                    if display_stat == 'PRA':
                        hover_data = ['Points', 'Rebounds',
                                      'Assists', 'Minutes']
                    elif display_stat == 'PR':
                        hover_data = ['Points', 'Rebounds', 'Minutes']
                    elif display_stat == 'threes_made':
                        hover_data = ['Points', 'threes_made', 'Minutes']
                    else:
                        hover_data = None

                    fig = px.line(top_players_df, x='Game Date', y=display_stat, color='Player',
                                  markers=True, hover_data=hover_data)
                    fig.update_layout(xaxis_title="Game Date",
                                      yaxis_title=title_prefix)
                    st.plotly_chart(fig)

                with col2:
                    st.subheader(f"Team {title_prefix} by Game")
                    team_game_totals = df.groupby('Game Date').agg({
                        display_stat: 'sum',
                        'Matchup': 'first',
                        'Opponent': 'first'
                    }).reset_index()

                    fig = px.bar(team_game_totals, x='Game Date', y=display_stat,
                                 hover_data=['Matchup'],
                                 color=display_stat,
                                 color_continuous_scale=color_scale,
                                 text=display_stat)
                    fig.update_layout(xaxis_title="Game Date",
                                      yaxis_title=f"Team Total {title_prefix}")
                    st.plotly_chart(fig)

                # Add heatmap for player performance across games - with error handling
                st.subheader("Player Performance Heatmap")

                try:
                    # Get unique players and game dates
                    players = df['Player'].unique()
                    game_dates = sorted(df['Game Date'].unique())

                    # Create a mapping from game date to formatted date string for display
                    date_labels = {date: date.strftime(
                        '%m/%d') for date in game_dates}

                    # Create an empty DataFrame with the correct dimensions
                    heatmap_data = pd.DataFrame(
                        index=players, columns=game_dates)

                    # Fill in the data
                    for player in players:
                        for game_date in game_dates:
                            player_game_data = df[(df['Player'] == player) & (
                                df['Game Date'] == game_date)]
                            if not player_game_data.empty:
                                heatmap_data.at[player,
                                                game_date] = player_game_data['Points'].sum()
                            else:
                                heatmap_data.at[player, game_date] = 0

                    # Fill NaN values with 0
                    heatmap_data = heatmap_data.fillna(0)

                    # Sort players by total points
                    heatmap_data['Total'] = heatmap_data.sum(axis=1)
                    heatmap_data = heatmap_data.sort_values(
                        'Total', ascending=False).drop('Total', axis=1)

                    # Show top 10 players only
                    heatmap_data = heatmap_data.head(10)

                    # Format the dates for display (convert datetime objects to strings)
                    formatted_dates = [date_labels[date]
                                       for date in heatmap_data.columns]

                    # Create heatmap
                    fig = px.imshow(heatmap_data,
                                    labels=dict(x="Game Date",
                                                y="Player", color="Points"),
                                    x=formatted_dates,  # Use formatted dates
                                    y=heatmap_data.index,
                                    color_continuous_scale='YlOrRd',
                                    aspect="auto")

                    fig.update_layout(
                        title="Points by Player Across Games",
                        xaxis_title="Game Date",
                        yaxis_title="Player",
                        height=500
                    )

                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not generate heatmap: {str(e)}")
                    st.info(
                        "This may happen if there are inconsistencies in the game data.")

            else:
                st.warning(
                    f"No playoff data found for {selected_team_name} in the {selected_season} season.")

        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            st.info("Try selecting a different team or season.")

    # Add attribution footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.8em;'>Data provided by NBA API. Application created by Yi-An T.</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    app()
