import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch

def plot_player_heatmap(df, player_id):
    player_data = df[df['player_id_tracking'] == player_id]
    
    # Check if player data exists
    if len(player_data) == 0:
        print(f"No data found for player_id: {player_id}")
        return
    
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
    
    # Heatmap
    heatmap, xedges, yedges = np.histogram2d(
        player_data['x'], player_data['y'],
        bins=[30, 20],
        range=[[-52.5, 52.5], [-34, 34]]
    )
    
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    im = ax.imshow(heatmap.T, extent=extent, origin='lower', cmap='hot', alpha=0.6)
    
    plt.colorbar(im, ax=ax, label='Time spent')
    
    player_name = player_data['short_name'].iloc[0]
    position = player_data['player_role.acronym'].iloc[0] if 'player_role.acronym' in player_data.columns else ''
    team = player_data['team_name'].iloc[0] if 'team_name' in player_data.columns else ''
    
    ax.set_title(f"{player_name} ({position}) - {team}\nHeat Map", color='white', fontsize=16)
    
    plt.tight_layout()
    plt.savefig(f'heatmap_{player_name.replace(" ", "_")}.png', dpi=150, facecolor='#1a1a1a')
    plt.show()
