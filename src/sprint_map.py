import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch

def calculate_velocity(df):
    df = df.sort_values(['player_id_tracking', 'timestamp'])
    df['x_diff'] = df.groupby('player_id_tracking')['x'].diff()
    df['y_diff'] = df.groupby('player_id_tracking')['y'].diff()
    df['time_diff'] = df.groupby('player_id_tracking')['timestamp'].diff().dt.total_seconds()
    df['distance'] = np.sqrt(df['x_diff']**2 + df['y_diff']**2)
    df['velocity'] = df['distance'] / df['time_diff']
    return df

def plot_sprint_map(df, player_id):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = calculate_velocity(df)
    
    player_data = df[df['player_id_tracking'] == player_id]
    
    # Check if player data exists
    if len(player_data) == 0:
        print(f"No data found for player_id: {player_id}")
        return
    
    sprints = player_data[player_data['velocity'] > 7].copy()
    
    sprints['has_ball'] = sprints['ball_carrier'] == True
    
    pitch = Pitch(
        pitch_type="skillcorner",
        line_alpha=0.75,
        pitch_length=105,
        pitch_width=68,
        pitch_color="#001400",
        line_color="white",
        linewidth=1.5,
    )
    fig, ax = pitch.draw(figsize=(12, 8))
    
    # Sprint arrows
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
    
    player_name = player_data['short_name'].iloc[0]
    position = player_data['player_role.acronym'].iloc[0] if 'player_role.acronym' in player_data.columns else ''
    team = player_data['team_name'].iloc[0] if 'team_name' in player_data.columns else ''
    
    ax.set_title(f"{player_name} ({position}) - {team}\nSprint Map (>7 m/s)", color='white', fontsize=16)
    ax.legend(loc='upper right', facecolor='#001400', edgecolor='white', labelcolor='white')
    
    plt.tight_layout()
    plt.savefig(f'sprint_map_{player_name.replace(" ", "_")}.png', dpi=150, facecolor='#1a1a1a')
    plt.show()