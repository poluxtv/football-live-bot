import streamlit as st
import time
from datetime import datetime
import live_scores
import match_schedule
import league_standings
import player_stats

# Page configuration
st.set_page_config(
    page_title="Football Live Bot",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00AA55;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #00AA55, #0088CC);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .live-indicator {
        color: #FF4B4B;
        font-weight: bold;
        animation: blink 1s infinite;
    }
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">⚽ Football Live Bot</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("⚽ Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🔴 Live Scores", "📅 Today's Matches", "🏆 League Standings", "👤 Player Statistics"]
    )
    
    # Add refresh button in sidebar
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    # Display current time
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")
    
    # Auto-refresh for live scores
    if page == "🔴 Live Scores":
        # Add auto-refresh toggle
        auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=True)
        if auto_refresh:
            # Create placeholder for countdown
            countdown_placeholder = st.sidebar.empty()
            
            # Auto-refresh countdown
            if 'last_refresh' not in st.session_state:
                st.session_state.last_refresh = time.time()
            
            time_since_refresh = time.time() - st.session_state.last_refresh
            if time_since_refresh >= 30:
                st.session_state.last_refresh = time.time()
                st.rerun()
            else:
                countdown = 30 - int(time_since_refresh)
                countdown_placeholder.markdown(f"**Next refresh in:** {countdown}s")
    
    # Route to different pages
    if page == "🔴 Live Scores":
        live_scores.show_live_scores()
    elif page == "📅 Today's Matches":
        match_schedule.show_match_schedule()
    elif page == "🏆 League Standings":
        league_standings.show_league_standings()
    elif page == "👤 Player Statistics":
        player_stats.show_player_statistics()

if __name__ == "__main__":
    main()
