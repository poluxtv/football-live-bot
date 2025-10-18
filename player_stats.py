import streamlit as st
import pandas as pd
from api_service import api_service, POPULAR_LEAGUES

def show_player_statistics():
    st.header("👤 Player Statistics")
    
    # League selection
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_league = st.selectbox(
            "Select League:",
            options=list(POPULAR_LEAGUES.keys()),
            index=0
        )
    
    with col2:
        if st.button("🔄 Refresh Stats"):
            st.rerun()
    
    if not selected_league:
        st.warning("Please select a league.")
        return
    
    league_config = POPULAR_LEAGUES[selected_league]
    league_id = league_config["id"]
    season = league_config["season"]
    
    # Tabs for different statistics
    tab1, tab2 = st.tabs(["⚽ Top Scorers", "🎯 Top Assists"])
    
    with tab1:
        show_top_scorers(league_id, season, selected_league)
    
    with tab2:
        show_top_assists(league_id, season, selected_league)

def show_top_scorers(league_id, season, league_name):
    """Display top scorers for the selected league"""
    st.markdown(f"### ⚽ Top Scorers - {league_name}")
    
    # Fetch top scorers
    with st.spinner("Loading top scorers..."):
        data = api_service.get_top_scorers(league_id, season)
    
    if not data or not data.get("response"):
        st.error("Unable to fetch top scorers. Please try again later.")
        return
    
    players = data["response"]
    
    if not players:
        st.info("No player statistics available for this league.")
        return
    
    # Create top scorers DataFrame
    scorers_data = []
    
    for player_data in players[:20]:  # Top 20 scorers
        player = player_data["player"]
        statistics = player_data["statistics"][0]  # Take first team stats
        team = statistics["team"]
        goals = statistics["goals"]["total"] or 0
        assists = statistics["goals"]["assists"] or 0
        appearances = statistics["games"]["appearences"] or 0
        minutes = statistics["games"]["minutes"] or 0
        
        # Calculate goals per game
        goals_per_game = round(goals / appearances, 2) if appearances > 0 else 0
        
        scorers_data.append({
            "Rank": len(scorers_data) + 1,
            "Player": player["name"],
            "Team": team["name"],
            "Goals": goals,
            "Assists": assists,
            "Appearances": appearances,
            "Minutes": minutes,
            "Goals/Game": goals_per_game,
            "Age": player.get("age", "N/A"),
            "Position": statistics.get("games", {}).get("position", "N/A")
        })
    
    df = pd.DataFrame(scorers_data)
    
    # Display metrics for top 3
    if len(scorers_data) >= 3:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🥇 Golden Boot Leader")
            top_scorer = scorers_data[0]
            st.metric(
                top_scorer["Player"],
                f"{top_scorer['Goals']} goals",
                f"{top_scorer['Team']}"
            )
            st.caption(f"⚽ {top_scorer['Goals/Game']} goals per game")
        
        with col2:
            st.markdown("### 🥈 Second Place")
            second = scorers_data[1]
            st.metric(
                second["Player"],
                f"{second['Goals']} goals",
                f"{second['Team']}"
            )
            st.caption(f"⚽ {second['Goals/Game']} goals per game")
        
        with col3:
            st.markdown("### 🥉 Third Place")
            third = scorers_data[2]
            st.metric(
                third["Player"],
                f"{third['Goals']} goals",
                f"{third['Team']}"
            )
            st.caption(f"⚽ {third['Goals/Game']} goals per game")
    
    st.divider()
    
    # Display full table
    st.markdown("### 📊 Complete Top Scorers Table")
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Player": st.column_config.TextColumn("Player", width="large"),
            "Team": st.column_config.TextColumn("Team", width="medium"),
            "Goals": st.column_config.NumberColumn("Goals", width="small"),
            "Assists": st.column_config.NumberColumn("Assists", width="small"),
            "Appearances": st.column_config.NumberColumn("Apps", width="small"),
            "Minutes": st.column_config.NumberColumn("Minutes", width="small"),
            "Goals/Game": st.column_config.NumberColumn("G/G", width="small", format="%.2f"),
            "Age": st.column_config.NumberColumn("Age", width="small"),
            "Position": st.column_config.TextColumn("Pos", width="small"),
        }
    )

def show_top_assists(league_id, season, league_name):
    """Display top assists for the selected league"""
    st.markdown(f"### 🎯 Top Assists - {league_name}")
    
    # Fetch top assists
    with st.spinner("Loading top assists..."):
        data = api_service.get_top_assists(league_id, season)
    
    if not data or not data.get("response"):
        st.error("Unable to fetch top assists. Please try again later.")
        return
    
    players = data["response"]
    
    if not players:
        st.info("No assist statistics available for this league.")
        return
    
    # Create top assists DataFrame
    assists_data = []
    
    for player_data in players[:20]:  # Top 20 assist providers
        player = player_data["player"]
        statistics = player_data["statistics"][0]  # Take first team stats
        team = statistics["team"]
        goals = statistics["goals"]["total"] or 0
        assists = statistics["goals"]["assists"] or 0
        appearances = statistics["games"]["appearences"] or 0
        minutes = statistics["games"]["minutes"] or 0
        
        # Calculate assists per game
        assists_per_game = round(assists / appearances, 2) if appearances > 0 else 0
        
        assists_data.append({
            "Rank": len(assists_data) + 1,
            "Player": player["name"],
            "Team": team["name"],
            "Assists": assists,
            "Goals": goals,
            "Appearances": appearances,
            "Minutes": minutes,
            "Assists/Game": assists_per_game,
            "Age": player.get("age", "N/A"),
            "Position": statistics.get("games", {}).get("position", "N/A")
        })
    
    df = pd.DataFrame(assists_data)
    
    # Display metrics for top 3
    if len(assists_data) >= 3:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🥇 Top Playmaker")
            top_assister = assists_data[0]
            st.metric(
                top_assister["Player"],
                f"{top_assister['Assists']} assists",
                f"{top_assister['Team']}"
            )
            st.caption(f"🎯 {top_assister['Assists/Game']} assists per game")
        
        with col2:
            st.markdown("### 🥈 Second Place")
            second = assists_data[1]
            st.metric(
                second["Player"],
                f"{second['Assists']} assists",
                f"{second['Team']}"
            )
            st.caption(f"🎯 {second['Assists/Game']} assists per game")
        
        with col3:
            st.markdown("### 🥉 Third Place")
            third = assists_data[2]
            st.metric(
                third["Player"],
                f"{third['Assists']} assists",
                f"{third['Team']}"
            )
            st.caption(f"🎯 {third['Assists/Game']} assists per game")
    
    st.divider()
    
    # Display full table
    st.markdown("### 📊 Complete Top Assists Table")
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Player": st.column_config.TextColumn("Player", width="large"),
            "Team": st.column_config.TextColumn("Team", width="medium"),
            "Assists": st.column_config.NumberColumn("Assists", width="small"),
            "Goals": st.column_config.NumberColumn("Goals", width="small"),
            "Appearances": st.column_config.NumberColumn("Apps", width="small"),
            "Minutes": st.column_config.NumberColumn("Minutes", width="small"),
            "Assists/Game": st.column_config.NumberColumn("A/G", width="small", format="%.2f"),
            "Age": st.column_config.NumberColumn("Age", width="small"),
            "Position": st.column_config.TextColumn("Pos", width="small"),
        }
    )
    
    # Additional insights
    if len(assists_data) > 0:
        st.markdown("### 💡 Playmaker Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Most creative midfielder/forward
            creative_players = [p for p in assists_data if p["Position"] in ["Midfielder", "Attacker", "Forward"]]
            if creative_players:
                top_creative = max(creative_players, key=lambda x: x["Assists"])
                st.info(f"🎨 Most Creative Player: **{top_creative['Player']}** ({top_creative['Team']}) with {top_creative['Assists']} assists")
        
        with col2:
            # Best assists to goals ratio
            balanced_players = [p for p in assists_data if p["Goals"] > 0]
            if balanced_players:
                best_balanced = max(balanced_players, key=lambda x: x["Assists"] + x["Goals"])
                total_contributions = best_balanced["Assists"] + best_balanced["Goals"]
                st.success(f"⚡ Most Productive: **{best_balanced['Player']}** with {total_contributions} goal contributions")
