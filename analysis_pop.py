from itertools import groupby
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
import main
import matplotlib.pyplot as plt
import yaml

yamlFile = "./input/popAnalysis.yaml"

dfs = []

SIMULATE = True

for i in range(2):
    csvFile = './logs/pop' + str(i) + '.csv'
    rate = round(i * 0.008 + 0.004, 6)

    if SIMULATE:
        params = {}
        with open(yamlFile) as fp:
            params = yaml.load(fp, Loader=yaml.FullLoader)

        params['GROW_FOOD_RATE'] = rate

        params['CSV_NAME_GENERAL'] = csvFile

        with open(yamlFile, 'w') as fp:
            documents = yaml.dump(params, fp)

        main.start(yamlFile)

    df = pd.read_csv(csvFile)

    dfs.append(df)

plt.close()

for df in dfs:
    print(df.head(5))
    df_ = df.melt('t', var_name='type', value_name='vals')

    fig, ax = plt.subplots()

    g = sns.lineplot(
        data=df_,
        x="t", y="vals", hue='type',
        palette="tab10",
    )

plt.show()
