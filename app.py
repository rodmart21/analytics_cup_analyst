import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# Page config
st.set_page_config(page_title="Player Movement Analysis", layout="wide")

# Title
st.title("⚽ Player Movement Intelligence Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/synced_enriched_tracking_and_events_10min.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = load_data()

# Calculate velocity
@st.cache_data
def calculate_velocity(df):
    df = df.sort_values(['player_id_tracking', 'timestamp'])
    df['x_diff'] = df.groupby('player_id_tracking')['x'].diff()
    df['y_diff'] = df.groupby('player_id_tracking')['y'].diff()
    df['time_diff'] = df.groupby('player_id_tracking')['timestamp'].diff().dt.total_seconds()
    df['distance'] = np.sqrt(df['x_diff']**2 + df['y_diff']**2)
    df['velocity'] = df['distance'] / df['time_diff']
    return df

df = calculate_velocity(df)

# Sidebar - Player selection
st.sidebar.header("Select Player")

player_list = df[['player_id_tracking', 'short_name', 'number', 'team_name', 'player_role.acronym']].drop_duplicates()
player_list['display_name'] = player_list['short_name'] + ' (#' + player_list['number'].astype(str) + ') - ' + player_list['player_role.acronym']

selected_player = st.sidebar.selectbox(
    "Choose a player:",
    player_list['player_id_tracking'].values,
    format_func=lambda x: player_list[player_list['player_id_tracking'] == x]['display_name'].values[0]
)

# Get player data
player_data = df[df['player_id_tracking'] == selected_player]
player_name = player_data['short_name'].iloc[0]
position = player_data['player_role.acronym'].iloc[0]
team = player_data['team_name'].iloc[0]
number = player_data['number'].iloc[0]

# Header
st.header(f"{player_name} (#{number}) - {position} | {team}")

# Movement Stats
st.subheader("📊 Movement Statistics")

col1, col2, col3, col4 = st.columns(4)

total_distance = player_data['distance'].sum()
sprint_distance = player_data[player_data['velocity'] > 7]['distance'].sum()
top_speed = player_data['velocity'].max()
num_sprints = ((player_data['velocity'] > 7) & (player_data['velocity'].shift(1) <= 7)).sum()

col1.metric("Total Distance", f"{total_distance:.0f} m")
col2.metric("Sprint Distance", f"{sprint_distance:.0f} m")
col3.metric("Top Speed", f"{top_speed:.1f} m/s")
col4.metric("Number of Sprints", f"{num_sprints}")

# Visualizations
tab1, tab2 = st.tabs(["🔥 Heat Map", "⚡ Sprint Map"])

with tab1:
    st.subheader("Player Heat Map")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    pitch = Pitch(
        pitch_type="skillcorner",
        line_alpha=0.75,
        pitch_length=105,
        pitch_width=68,
        pitch_color="#001400",
        line_color="white",
        linewidth=1.5,
    )
    pitch.draw(ax=ax)
    
    heatmap, xedges, yedges = np.histogram2d(
        player_data['x'], player_data['y'],
        bins=[30, 20],
        range=[[-52.5, 52.5], [-34, 34]]
    )
    
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    im = ax.imshow(heatmap.T, extent=extent, origin='lower', cmap='hot', alpha=0.6)
    
    plt.colorbar(im, ax=ax, label='Time spent')
    ax.set_title(f"{player_name} Heat Map", color='white', fontsize=16)
    
    st.pyplot(fig)

with tab2:
    st.subheader("Sprint Map (>7 m/s)")
    
    sprints = player_data[player_data['velocity'] > 7].copy()
    sprints['has_ball'] = sprints['ball_carrier'] == True
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    pitch = Pitch(
        pitch_type="skillcorner",
        line_alpha=0.75,
        pitch_length=105,
        pitch_width=68,
        pitch_color="#001400",
        line_color="white",
        linewidth=1.5,
    )
    pitch.draw(ax=ax)
    
    with_ball = sprints[sprints['has_ball']]
    without_ball = sprints[~sprints['has_ball']]
    
    if len(with_ball) > 0:
        ax.quiver(with_ball['x'], with_ball['y'], 
                 with_ball['x_diff'], with_ball['y_diff'],
                 color='#32FE6B', alpha=0.7, width=0.003, scale=50, label='With ball')
    
    if len(without_ball) > 0:
        ax.quiver(without_ball['x'], without_ball['y'],
                 without_ball['x_diff'], without_ball['y_diff'],
                 color='#E5BA21', alpha=0.7, width=0.003, scale=50, label='Without ball')
    
    ax.set_title(f"{player_name} Sprint Map", color='white', fontsize=16)
    ax.legend(loc='upper right', facecolor='#001400', edgecolor='white', labelcolor='white')
    
    st.pyplot(fig)