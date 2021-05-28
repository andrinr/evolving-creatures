import pandas as pd
from pandas.core.frame import DataFrame
import seaborn as sns
from matplotlib.animation import FuncAnimation, FFMpegWriter
import main
import matplotlib.pyplot as plt
import yaml

yamlFile = "./input/kidsAnalysis.yaml"

df_all = DataFrame()

SIMULATE = False

for i in range(3):
    csvFile = './logs/kids' + str(i) + '.csv'
    rate = round(i * 0.03, 6)

    if SIMULATE:
        params = {}
        with open(yamlFile) as fp:
            params = yaml.load(fp, Loader=yaml.FullLoader)

        params['COSTS_PER_MOVE'] = rate

        params['CSV_NAME_CREATURES'] = csvFile

        with open(yamlFile, 'w') as fp:
            documents = yaml.dump(params, fp)

        main.start(yamlFile)

    df = pd.read_csv(csvFile)

    df['COSTS_PER_MOVE'] = rate

    df_all = pd.concat([df_all, df])

plt.close()

g = sns.boxplot(
    data=df_all[df_all['t'] > 800].sample(5000),
    x="COSTS_PER_MOVE", y="nKids",
)

fig, ax = plt.subplots()

g = sns.boxplot(
    data=df_all.sample(5000),
    x="COSTS_PER_MOVE", y="energyChildrenThreshold",
)

plt.show()
