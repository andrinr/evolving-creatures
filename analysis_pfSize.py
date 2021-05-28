from itertools import groupby
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
import main
import matplotlib.pyplot as plt
import yaml

yamlFile = "./input/birthDeath.yaml"

df_all = pd.DataFrame()

SIMULATE = False

for i in range(3):
    csvFile = './logs/bd' + str(i) + '.csv'
    rate = round(i * 0.004 + 0.0015, 6)

    if SIMULATE:
        params = {}
        with open(yamlFile) as fp:
            params = yaml.load(fp, Loader=yaml.FullLoader)

        params['GROW_FOOD_RATE'] = rate

        params['CSV_NAME_CREATURES'] = csvFile

        with open(yamlFile, 'w') as fp:
            documents = yaml.dump(params, fp)

        main.start(yamlFile)

    df = pd.read_csv(csvFile)

    df['GROW_FOOD_RATE'] = rate

    df_all = pd.concat([df_all, df])

plt.close()

# We use a subseclection where only creatures which have died at later stages are plotted
# This is to avoid outliers from early stages of the simulation where the entire paramter space is filled
g = sns.boxplot(
    data=df_all[df_all['t'] > 300],
    x="GROW_FOOD_RATE", y="pfSize", hue="GROW_FOOD_RATE",
    palette="tab10",
)


plt.show()