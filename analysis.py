import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt

df_creatures = pd.read_csv("log.csv")
df_creatures.info()

grid = sns.PairGrid(df_creatures)
#grid.map(sns.kdeplot)
grid.map_diag(sns.histplot)
grid.map_lower(sns.kdeplot)
grid.map_upper(sns.scatterplot)

plt.show()
