from itertools import groupby
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter

import matplotlib.pyplot as plt

df_creatures = pd.read_csv("./logs/creatures.csv")
df_general = pd.read_csv("./logs/grid.csv")
df_genes = df_creatures[['nKids','energyChildrenThreshold','speed', 'pfSize']]

# GRID PLOT

#grid = sns.PairGrid(df_genes)
#grid.map_diag(sns.histplot)
#grid.map_upper(sns.scatterplot)
#grid.map_lower(sns.kdeplot, fill=True)
    
# LINE PLOT NUMBER OF CHILDREN

# Summarize time ranges#
# df_creatures['t'] = df_creatures['t'].div(100).round(0)

#grouped = df_creatures.groupby('t').median()

#sns.boxplot(x='t', y='nChildren', data=df_creatures)
#sns.boxplot(x='t', y='toEnemies', data=df_creatures)

#sns.displot(data=df_creatures, x='t',kind="kde",multiple="fill", hue='cause', clip=(0, 1000))
#print(df_creatures)
#plt.figure()
# Plot nCreatures against nFoods
#sns.lineplot(x='t', y='vals',  hue='cols', data=df_general)
#df_general = df_general.melt('t', var_name='cols',  value_name='vals')

#plt.figure()

fig, ax = plt.subplots()

def update(i):
    ax.clear()
    ax.set_xlim(0,5)
    ax.set_ylim(0,5)    
    current = df_creatures[abs(df_creatures['t'] - i) < 10]
    ax.scatter(current['energyChildrenThreshold'], current['nKids'], c=current['age'])

ani = FuncAnimation(fig, func = update, frames = 1000, interval =10, repeat = False)

#FFwriter = FFMpegWriter(fps=10)
#ani.save('energyVSkids.mp4', writer=FFwriter)

plt.show()
