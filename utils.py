import streamlit as st
from datetime import datetime, timezone
import pandas as pd

def format_match_time(iso_time_string):
    """Convert ISO time string to local time format"""
    try:
        # Parse ISO time
        match_time = datetime.fromisoformat(iso_time_string.replace('Z', '+00:00'))
        # Convert to local time
        local_time = match_time.replace(tzinfo=timezone.utc).astimezone()
        return local_time.strftime('%H:%M')
    except:
        return "TBD"

def format_match_date(iso_time_string):
    """Convert ISO time string to date format"""
    try:
        match_time = datetime.fromisoformat(iso_time_string.replace('Z', '+00:00'))
        local_time = match_time.replace(tzinfo=timezone.utc).astimezone()
        return local_time.strftime('%Y-%m-%d')
    except:
        return "TBD"

def get_match_status_color(status_short):
    """Get color for match status"""
    status_colors = {
        "NS": "#FFA500",  # Not Started - Orange
        "1H": "#FF4B4B",  # First Half - Red
        "HT": "#FF6B6B",  # Half Time - Light Red
        "2H": "#FF4B4B",  # Second Half - Red
        "ET": "#FF1744",  # Extra Time - Dark Red
        "P": "#FF1744",   # Penalty - Dark Red
        "FT": "#00AA55",  # Full Time - Green
        "AET": "#00AA55", # After Extra Time - Green
        "PEN": "#00AA55", # After Penalties - Green
        "PST": "#FFC107", # Postponed - Yellow
        "CANC": "#9E9E9E", # Cancelled - Gray
        "ABD": "#9E9E9E",  # Abandoned - Gray
        "TBD": "#9E9E9E",  # To Be Decided - Gray
    }
    return status_colors.get(status_short, "#9E9E9E")

def display_team_form(form_string):
    """Display team form with colored indicators"""
    if not form_string:
        return ""
    
    form_html = ""
    for result in form_string[-5:]:  # Last 5 results
        if result == "W":
            form_html += '<span style="color: #00AA55; font-weight: bold;">W</span> '
        elif result == "D":
            form_html += '<span style="color: #FFA500; font-weight: bold;">D</span> '
        elif result == "L":
            form_html += '<span style="color: #FF4B4B; font-weight: bold;">L</span> '
    
    return form_html.strip()

def calculate_goal_difference(goals_for, goals_against):
    """Calculate goal difference"""
    gf = goals_for or 0
    ga = goals_against or 0
    diff = gf - ga
    
    if diff > 0:
        return f"+{diff}"
    elif diff < 0:
        return str(diff)
    else:
        return "0"

def format_minutes(minutes):
    """Format minutes played"""
    if not minutes:
        return "0"
    
    if minutes >= 90:
        return f"{minutes}'"
    else:
        return f"{minutes}'"

def get_league_flag_emoji(country):
    """Get flag emoji for country"""
    flag_mapping = {
        "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "Spain": "🇪🇸",
        "Germany": "🇩🇪",
        "Italy": "🇮🇹",
        "France": "🇫🇷",
        "Portugal": "🇵🇹",
        "Netherlands": "🇳🇱",
        "Brazil": "🇧🇷",
        "Argentina": "🇦🇷",
        "World": "🌍",
    }
    return flag_mapping.get(country, "🌍")

def display_loading_spinner(text="Loading..."):
    """Display a loading spinner with custom text"""
    with st.spinner(text):
        pass

def safe_get(dictionary, key, default=None):
    """Safely get a value from a dictionary"""
    return dictionary.get(key, default) if dictionary else default

def format_large_number(number):
    """Format large numbers with K/M suffixes"""
    if number is None:
        return "0"
    
    if number >= 1000000:
        return f"{number / 1000000:.1f}M"
    elif number >= 1000:
        return f"{number / 1000:.1f}K"
    else:
        return str(number)

def validate_api_response(response_data):
    """Validate API response structure"""
    if not response_data:
        return False, "No data received"
    
    if "response" not in response_data:
        return False, "Invalid response format"
    
    if not response_data["response"]:
        return False, "Empty response data"
    
    return True, "Valid response"

def handle_api_error(error_message):
    """Handle and display API errors"""
    st.error(f"API Error: {error_message}")
    st.info("Please check your internet connection and try again.")

def create_metric_card(title, value, subtitle=None, delta=None):
    """Create a custom metric card"""
    with st.container():
        st.metric(
            label=title,
            value=value,
            delta=delta,
            help=subtitle
        )

def filter_matches_by_status(matches, status_list):
    """Filter matches by status"""
    return [
        match for match in matches
        if match.get("fixture", {}).get("status", {}).get("short") in status_list
    ]

def sort_matches_by_time(matches, reverse=False):
    """Sort matches by fixture time"""
    return sorted(
        matches,
        key=lambda x: x.get("fixture", {}).get("date", ""),
        reverse=reverse
    )

def get_time_until_match(iso_time_string):
    """Get time remaining until match starts"""
    try:
        match_time = datetime.fromisoformat(iso_time_string.replace('Z', '+00:00'))
        current_time = datetime.now(timezone.utc)
        
        if match_time > current_time:
            diff = match_time - current_time
            hours = int(diff.total_seconds() // 3600)
            minutes = int((diff.total_seconds() % 3600) // 60)
            
            if hours > 24:
                days = hours // 24
                remaining_hours = hours % 24
                return f"{days}d {remaining_hours}h"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        else:
            return "Started"
    except:
        return "Unknown"
