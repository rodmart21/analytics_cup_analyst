import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_velocity(df):
    df = df.sort_values(['player_id_tracking', 'timestamp'])
    df['x_diff'] = df.groupby('player_id_tracking')['x'].diff()
    df['y_diff'] = df.groupby('player_id_tracking')['y'].diff()
    df['time_diff'] = df.groupby('player_id_tracking')['timestamp'].diff().dt.total_seconds()
    df['distance'] = np.sqrt(df['x_diff']**2 + df['y_diff']**2)
    df['velocity'] = df['distance'] / df['time_diff']
    return df

def get_movement_stats(df, player_id):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = calculate_velocity(df)
    
    player_data = df[df['player_id_tracking'] == player_id].copy()
    
    total_distance = player_data['distance'].sum()
    sprint_distance = player_data[player_data['velocity'] > 7]['distance'].sum()
    top_speed = player_data['velocity'].max()
    avg_x = player_data['x'].mean()
    avg_y = player_data['y'].mean()
    
    with_ball_distance = player_data[player_data['ball_carrier'] == True]['distance'].sum()
    without_ball_distance = total_distance - with_ball_distance
    
    num_sprints = ((player_data['velocity'] > 7) & (player_data['velocity'].shift(1) <= 7)).sum()
    
    player_name = player_data['short_name'].iloc[0]
    position = player_data['player_role.acronym'].iloc[0]
    team = player_data['team_name'].iloc[0]
    number = player_data['number'].iloc[0]
    
    stats = {
        'Player': f"{player_name} (#{number})",
        'Position': position,
        'Team': team,
        'Total Distance (m)': f"{total_distance:.1f}",
        'Sprint Distance (m)': f"{sprint_distance:.1f}",
        'Distance with Ball (m)': f"{with_ball_distance:.1f}",
        'Distance without Ball (m)': f"{without_ball_distance:.1f}",
        'Top Speed (m/s)': f"{top_speed:.2f}",
        'Number of Sprints': num_sprints,
        'Average Position': f"({avg_x:.1f}, {avg_y:.1f})"
    }
    
    return stats

def print_movement_stats(df, player_id):
    stats = get_movement_stats(df, player_id)
    
    print("\n" + "="*50)
    print(f"   {stats['Player']} - {stats['Position']}")
    print(f"   {stats['Team']}")
    print("="*50)
    print(f"  Total Distance:        {stats['Total Distance (m)']} m")
    print(f"  Sprint Distance:       {stats['Sprint Distance (m)']} m")
    print(f"  Distance with Ball:    {stats['Distance with Ball (m)']} m")
    print(f"  Distance w/o Ball:     {stats['Distance without Ball (m)']} m")
    print(f"  Top Speed:             {stats['Top Speed (m/s)']} m/s")
    print(f"  Number of Sprints:     {stats['Number of Sprints']}")
    print(f"  Average Position:      {stats['Average Position']}")
    print("="*50 + "\n")
    
    return stats
