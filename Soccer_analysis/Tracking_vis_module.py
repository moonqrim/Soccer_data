import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mplsoccer import Pitch
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

df = pd.read_csv('tracking_data(5min)_sep.csv')

def by_frame(data,
             figax=None):
    data = data # type : series
    idx_ = int(data['id']-250)
    time = (data['id']-250) * 0.04

    # draw pitch(fig)
    pitch = Pitch(pitch_type='uefa', pitch_length=105, pitch_width=68,
              axis=False, label=False, corner_arcs=True,
              pitch_color='white', line_color='black', linewidth=0.5)

    if figax is None:
        fig, ax = pitch.draw()
    else:
        fig, ax = figax

    objects = [] # ax's list
    for team, color in zip(['H', 'A'], ['r', 'b']): # draw players
        x_cols = [k for k in data.keys() if k.startswith(team) and k.endswith('_x')]
        y_cols = [k for k in data.keys() if k.startswith(team) and k.endswith('_y')]
        obj = ax.scatter(data[x_cols], data[y_cols], s=20, c=color, alpha=0.6) # ax1 :players
        objects.append(obj)

    # draw ball / ax2 : ball
    obj = ax.scatter(data['ball_x'], data['ball_y'], s=10, color='black')
    objects.append(obj)

    frame_text = f'Frame Number : {idx_}'
    time_text = f"{int(time // 60):02d}:{time % 60:05.2f}"

    objects.append(ax.text(0, 0, frame_text, fontsize=6)) # frame number
    objects.append(ax.text(45, 0, 'FIRST_HALF', fontsize=6)) # first_half
    objects.append(ax.text(55, 0, time_text, fontsize=8)) # time

    return fig, ax, objects

def tracking_vis_by_frame(
        frames,    # data
        fps=25,    # default 25
        figax=None,
        file_name='Italy_Czech2'  # default
):

    metadata = dict(title='Tracking Data', comment='Bepro tracking data clip')
    writer = animation.FFMpegWriter(fps=fps, metadata=metadata)

    if not os.path.exists('task2'):
        os.makedirs('task2')
    file = f'task2/{file_name}.mp4'

    pitch = Pitch(pitch_type='uefa', pitch_length=105, pitch_width=68,
              axis=False, label=False,corner_arcs=True,
              pitch_color='white', line_color='black', linewidth=0.5)

    if figax is None:
        fig, ax = pitch.draw()
    else:
        fig, ax = figax
    ax.invert_yaxis()

    with writer.saving(fig, file, dpi=100):
        for i in frames.index:
            frame_data = frames.loc[i]
            # 프레임 별로 받아오기
            fig, ax, objects = by_frame(frame_data, (fig, ax))
            writer.grab_frame()

            for obj in objects:
                obj.remove() # objects 초기화
    plt.clf()
    plt.close(fig)
