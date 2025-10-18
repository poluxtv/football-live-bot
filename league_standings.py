import streamlit as st
import pandas as pd
from api_service import api_service, POPULAR_LEAGUES

def show_league_standings():
    st.header("🏆 League Standings")
    
    # League selection
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_league = st.selectbox(
            "Select League:",
            options=list(POPULAR_LEAGUES.keys()),
            index=0
        )
    
    with col2:
        if st.button("🔄 Refresh Standings"):
            st.rerun()
    
    if not selected_league:
        st.warning("Please select a league.")
        return
    
    league_config = POPULAR_LEAGUES[selected_league]
    league_id = league_config["id"]
    season = league_config["season"]
    
    # Fetch standings
    with st.spinner(f"Loading {selected_league} standings..."):
        data = api_service.get_league_standings(league_id, season)
    
    if not data or not data.get("response"):
        st.error("Unable to fetch standings. Please try again later.")
        return
    
    response = data["response"][0]
    league_info = response["league"]
    standings = response["league"]["standings"][0]  # Main standings group
    
    # League info
    st.markdown(f"### {league_info['name']} - Season {season}")
    st.caption(f"Country: {league_info['country']} | Last Updated: {league_info.get('season', '')}")
    st.divider()
    
    # Create standings DataFrame
    standings_data = []
    
    for team_standing in standings:
        team = team_standing["team"]
        stats = team_standing["all"]  # All games (home + away)
        
        standings_data.append({
            "Position": team_standing["rank"],
            "Team": team["name"],
            "Played": stats["played"],
            "Won": stats["win"],
            "Drawn": stats["draw"],
            "Lost": stats["lose"],
            "GF": stats["goals"]["for"],  # Goals For
            "GA": stats["goals"]["against"],  # Goals Against
            "GD": stats["goals"]["for"] - stats["goals"]["against"],  # Goal Difference
            "Points": team_standing["points"],
            "Form": team_standing.get("form", ""),
        })
    
    df = pd.DataFrame(standings_data)
    
    # Display standings table
    st.markdown("### 📊 Current Standings")
    
    # Style the dataframe
    styled_df = df.style.apply(style_standings_row, axis=1)
    
    # Display with custom formatting
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Position": st.column_config.NumberColumn("Pos", width="small"),
            "Team": st.column_config.TextColumn("Team", width="large"),
            "Played": st.column_config.NumberColumn("P", width="small"),
            "Won": st.column_config.NumberColumn("W", width="small"),
            "Drawn": st.column_config.NumberColumn("D", width="small"),
            "Lost": st.column_config.NumberColumn("L", width="small"),
            "GF": st.column_config.NumberColumn("GF", width="small"),
            "GA": st.column_config.NumberColumn("GA", width="small"),
            "GD": st.column_config.NumberColumn("GD", width="small"),
            "Points": st.column_config.NumberColumn("Pts", width="small"),
            "Form": st.column_config.TextColumn("Form", width="medium"),
        }
    )
    
    # Legend
    st.markdown("### 🏅 Legend")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("🟢 **Champions League**")
        st.caption("Top 4 positions")
    
    with col2:
        st.markdown("🟡 **Europa League**")
        st.caption("5th-6th positions")
    
    with col3:
        st.markdown("🟠 **Conference League**")
        st.caption("7th position")
    
    with col4:
        st.markdown("🔴 **Relegation**")
        st.caption("Bottom 3 positions")
    
    # Top performers
    if len(standings_data) > 0:
        st.markdown("### 📈 Season Highlights")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Most points
            top_team = max(standings_data, key=lambda x: x["Points"])
            st.metric("👑 Leader", top_team["Team"], f"{top_team['Points']} pts")
        
        with col2:
            # Most goals scored
            top_scorer = max(standings_data, key=lambda x: x["GF"])
            st.metric("⚽ Best Attack", top_scorer["Team"], f"{top_scorer['GF']} goals")
        
        with col3:
            # Best defense
            best_defense = min(standings_data, key=lambda x: x["GA"])
            st.metric("🛡️ Best Defense", best_defense["Team"], f"{best_defense['GA']} conceded")
        
        with col4:
            # Best goal difference
            best_gd = max(standings_data, key=lambda x: x["GD"])
            st.metric("📊 Best GD", best_gd["Team"], f"+{best_gd['GD']}")

def style_standings_row(row):
    """Style standings table rows based on position"""
    position = row["Position"]
    styles = [""] * len(row)
    
    # Champions League positions (1-4)
    if 1 <= position <= 4:
        styles = ["background-color: #e8f5e8"] * len(row)
    # Europa League positions (5-6)
    elif 5 <= position <= 6:
        styles = ["background-color: #fff9e6"] * len(row)
    # Conference League position (7)
    elif position == 7:
        styles = ["background-color: #fff4e6"] * len(row)
    # Relegation positions (bottom 3)
    elif position >= len(POPULAR_LEAGUES) - 2:  # Approximate last 3 positions
        styles = ["background-color: #ffe6e6"] * len(row)
    
    return styles
