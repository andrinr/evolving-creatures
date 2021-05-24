from itertools import groupby
import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt

df_creatures = pd.read_csv("./logs/creature.csv")
df_general = pd.read_csv("./logs/general.csv")
df_genes = df_creatures[['nChildren', 'energyChildrenThreshold', 'toEnemies', 'toFriends', 'genomeThreshold']]

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
fig, ax = plt.subplots()

sns.displot(ax=ax, data=df_creatures, x='t', hue='causeOfDeath',  kind="kde", multiple="fill", clip=(0, 1000))

# Plot nCreatures against nFoods
ax2 = ax.twinx()
df_general = df_general.melt('t', var_name='cols',  value_name='vals')
sns.lineplot(ax=ax, x='t', y='vals',  hue='cols', data=df_general)

plt.show()