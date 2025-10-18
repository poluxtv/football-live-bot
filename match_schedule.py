import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from api_service import api_service, POPULAR_LEAGUES

def show_match_schedule():
    st.header("📅 Today's Match Schedule")
    
    # League selection
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_leagues = st.multiselect(
            "Filter by Leagues:",
            options=list(POPULAR_LEAGUES.keys()),
            default=list(POPULAR_LEAGUES.keys())[:3]
        )
    
    with col2:
        if st.button("🔄 Refresh Schedule"):
            st.rerun()
    
    # Get league IDs
    league_ids = None
    if selected_leagues:
        league_ids = [POPULAR_LEAGUES[league]["id"] for league in selected_leagues]
    
    # Fetch today's matches
    with st.spinner("Loading today's matches..."):
        data = api_service.get_todays_matches(league_ids)
    
    if not data or not data.get("response"):
        st.warning("Unable to fetch match schedule. Please try again later.")
        return
    
    matches = data["response"]
    
    if not matches:
        st.info("No matches scheduled for today in selected leagues.")
        return
    
    # Sort matches by time
    matches_sorted = sorted(matches, key=lambda x: x["fixture"]["date"])
    
    # Group matches by status
    upcoming_matches = []
    live_matches = []
    finished_matches = []
    
    for match in matches_sorted:
        status = match["fixture"]["status"]["short"]
        if status in ["NS", "TBD"]:  # Not started
            upcoming_matches.append(match)
        elif status in ["1H", "HT", "2H", "ET", "BT", "P"]:  # Live
            live_matches.append(match)
        elif status in ["FT", "AET", "PEN"]:  # Finished
            finished_matches.append(match)
    
    # Display live matches first
    if live_matches:
        st.markdown("### 🔴 Live Now")
        display_matches(live_matches, show_live=True)
        st.divider()
    
    # Display upcoming matches
    if upcoming_matches:
        st.markdown("### ⏰ Upcoming Today")
        display_matches(upcoming_matches, show_live=False)
        st.divider()
    
    # Display finished matches
    if finished_matches:
        st.markdown("### ✅ Completed Today")
        with st.expander(f"Show completed matches ({len(finished_matches)})"):
            display_matches(finished_matches, show_live=False, show_results=True)

def display_matches(matches, show_live=False, show_results=False):
    """Display matches in a formatted way"""
    for match in matches:
        fixture = match["fixture"]
        teams = match["teams"]
        goals = match["goals"]
        league_info = match["league"]
        
        # Parse match time
        match_time = datetime.fromisoformat(fixture["date"].replace('Z', '+00:00'))
        local_time = match_time.replace(tzinfo=timezone.utc).astimezone()
        
        # Create match container
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])
            
            with col1:
                # Team names and league
                st.markdown(f"**{teams['home']['name']}** vs **{teams['away']['name']}**")
                st.caption(f"📍 {league_info['name']} - {league_info['round']}")
                if fixture.get("venue", {}).get("name"):
                    st.caption(f"🏟️ {fixture['venue']['name']}")
            
            with col2:
                # Time or score
                if show_live:
                    # Show live score and time
                    home_score = goals['home'] if goals['home'] is not None else 0
                    away_score = goals['away'] if goals['away'] is not None else 0
                    st.markdown(f"### {home_score} - {away_score}")
                    
                    elapsed = fixture.get("status", {}).get("elapsed", "")
                    if elapsed:
                        st.markdown(f"<span class='live-indicator'>{elapsed}' LIVE</span>", unsafe_allow_html=True)
                
                elif show_results:
                    # Show final score
                    if goals['home'] is not None and goals['away'] is not None:
                        st.markdown(f"### {goals['home']} - {goals['away']}")
                        st.caption("Full Time")
                    else:
                        st.caption("Score not available")
                
                else:
                    # Show kick-off time
                    st.markdown(f"### {local_time.strftime('%H:%M')}")
                    st.caption(local_time.strftime('%A'))
            
            with col3:
                # Match status
                status_text = fixture["status"]["long"]
                status_short = fixture["status"]["short"]
                
                if status_short in ["1H", "HT", "2H", "ET", "BT", "P"]:
                    st.markdown(f"🔴 **{status_text}**")
                elif status_short in ["FT", "AET", "PEN"]:
                    st.markdown(f"✅ **{status_text}**")
                elif status_short in ["NS", "TBD"]:
                    st.markdown(f"⏰ **{status_text}**")
                else:
                    st.markdown(f"📋 **{status_text}**")
                
                # Show postponed or cancelled status
                if status_short in ["PST", "CANC", "ABD"]:
                    st.error(f"Match {status_text}")
        
        st.divider()

def format_time_until_match(match_time):
    """Format time until match starts"""
    now = datetime.now(timezone.utc)
    match_time_utc = match_time.replace(tzinfo=timezone.utc)
    
    if match_time_utc > now:
        diff = match_time_utc - now
        hours = int(diff.total_seconds() // 3600)
        minutes = int((diff.total_seconds() % 3600) // 60)
        
        if hours > 0:
            return f"Starts in {hours}h {minutes}m"
        else:
            return f"Starts in {minutes}m"
    else:
        return "Started"
