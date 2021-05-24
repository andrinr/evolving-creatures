from itertools import groupby
import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt

df_creatures = pd.read_csv("log.csv")
df_creatures.info()
df_genes = df_creatures[['nChildren', 'energyChildrenThreshold', 'toEnemies', 'toFriends', 'genomeThreshold']]

# GRID PLOT

#grid = sns.PairGrid(df_genes)
#grid.map_diag(sns.histplot)
#grid.map_upper(sns.scatterplot)
#grid.map_lower(sns.kdeplot, fill=True)

# LINE PLOT NUMBER OF CHILDREN
df_creatures['t'] = df_creatures['t'].div(100).round(0)
#grouped = df_creatures.groupby('t').median()

#sns.boxplot(x='t', y='nChildren', data=df_creatures)
sns.boxplot(x='t', y='toEnemies', data=df_creatures)


plt.show()