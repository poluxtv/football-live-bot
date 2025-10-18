import streamlit as st
import pandas as pd
from datetime import datetime
from api_service import api_service, POPULAR_LEAGUES

def show_live_scores():
    st.header("🔴 Live Match Scores")
    
    # League selection
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_leagues = st.multiselect(
            "Select Leagues (leave empty for all):",
            options=list(POPULAR_LEAGUES.keys()),
            default=["Premier League", "Champions League"]
        )
    
    with col2:
        st.markdown("### Live Matches")
        if st.button("🔄 Refresh Now"):
            st.rerun()
    
    # Get league IDs
    league_ids = None
    if selected_leagues:
        league_ids = [POPULAR_LEAGUES[league]["id"] for league in selected_leagues]
    
    # Fetch live matches
    with st.spinner("Loading live matches..."):
        data = api_service.get_live_matches(league_ids)
    
    if not data or not data.get("response"):
        st.info("No live matches at the moment.")
        return
    
    matches = data["response"]
    
    if not matches:
        st.info("No live matches for selected leagues.")
        return
    
    # Display live matches
    st.markdown("### 🔴 Currently Live")
    
    for match in matches:
        fixture = match["fixture"]
        teams = match["teams"]
        goals = match["goals"]
        league_info = match["league"]
        
        # Create match container
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
            
            with col1:
                st.write(f"**{teams['home']['name']}**")
            
            with col2:
                home_score = goals['home'] if goals['home'] is not None else 0
                st.markdown(f"<h3 style='text-align: center;'>{home_score}</h3>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("<h3 style='text-align: center;'>-</h3>", unsafe_allow_html=True)
                # Show match time
                elapsed = fixture.get("status", {}).get("elapsed", "")
                if elapsed:
                    st.markdown(f"<p style='text-align: center; color: #FF4B4B;'>{elapsed}'</p>", unsafe_allow_html=True)
            
            with col4:
                away_score = goals['away'] if goals['away'] is not None else 0
                st.markdown(f"<h3 style='text-align: center;'>{away_score}</h3>", unsafe_allow_html=True)
            
            with col5:
                st.write(f"**{teams['away']['name']}**")
            
            # League and status info
            st.caption(f"{league_info['name']} • {fixture['status']['long']}")
            st.divider()
    
    # Recent finished matches (last 2 hours)
    st.markdown("### ⏱️ Recently Finished")
    
    with st.spinner("Loading recent matches..."):
        today_data = api_service.get_todays_matches(league_ids)
    
    if today_data and today_data.get("response"):
        recent_matches = []
        current_time = datetime.now()
        
        for match in today_data["response"]:
            fixture = match["fixture"]
            match_time = datetime.fromisoformat(fixture["date"].replace('Z', '+00:00'))
            
            # Check if match is finished and within last 2 hours
            if (fixture["status"]["short"] == "FT" and 
                (current_time - match_time).total_seconds() < 7200):  # 2 hours
                recent_matches.append(match)
        
        if recent_matches:
            for match in recent_matches[:5]:  # Show only last 5
                fixture = match["fixture"]
                teams = match["teams"]
                goals = match["goals"]
                league_info = match["league"]
                
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
                    
                    with col1:
                        st.write(teams['home']['name'])
                    
                    with col2:
                        st.markdown(f"<p style='text-align: center;'>{goals['home']}</p>", unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown("<p style='text-align: center;'>-</p>", unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown(f"<p style='text-align: center;'>{goals['away']}</p>", unsafe_allow_html=True)
                    
                    with col5:
                        st.write(teams['away']['name'])
                    
                    st.caption(f"{league_info['name']} • Full Time")
                    st.divider()
        else:
            st.info("No recently finished matches.")
    
    # Auto-refresh indicator
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em; margin-top: 2rem;'>
        🔄 Live scores update automatically every 30 seconds
    </div>
    """, unsafe_allow_html=True)
