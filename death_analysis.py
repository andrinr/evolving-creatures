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

SIMULATE = True

for i in range(3):
    csvFile = './logs/bd' + str(i) + '.csv'
    rate = round(i * 0.01 + 0.0001, 6)

    if SIMULATE:
        data = {}
        with open(yamlFile) as fp:
            data = yaml.load(fp, Loader=yaml.FullLoader)

        data['GROW_FOOD_RATE'] = rate

        data['CSV_NAME_CREATURES'] = csvFile

        with open(yamlFile, 'w') as fp:
            documents = yaml.dump(data, fp)

        main.start(yamlFile)

    df = pd.read_csv(csvFile)

    df['foodRate'] = rate

    df_all = pd.concat([df_all, df])

plt.close()


g = sns.jointplot(
    data=df_all[df_all['t'] > 150],
    x="nKids", y="energyChildrenThreshold", hue="foodRate",
    kind="kde", palette="tab10"
)
plt.show()