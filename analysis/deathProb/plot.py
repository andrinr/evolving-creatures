
from itertools import groupby
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter

import matplotlib.pyplot as plt

df_creatures = pd.read_csv("./logs/creatures.csv")
df_general = pd.read_csv("./logs/grid.csv")
df_genes = df_creatures[['nKids','energyChildrenThreshold','speed', 'pfSize']]
fig, ax = plt.subplots()

def update(i):
    ax.clear()
    ax.set_xlim(0,20)
    ax.set_ylim(0,20)    
    ax.set_title('Genome Parameters')
    ax.set_xlabel('energyChildrenThreshold')
    ax.set_ylabel('nKids')
    current = df_creatures[abs(df_creatures['t'] - i) < 10]
    ax.scatter(current['energyChildrenThreshold'], current['nKids'], c=current['age'])

ani = FuncAnimation(fig, func = update, frames = 400, interval =10, repeat = False)

FFwriter = FFMpegWriter(fps=10)
ani.save('./analysis/deathProb/out.mp4', writer=FFwriter)

plt.show()
