from creature import Creature
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from grid import Grid
from  time import time
import csv
import numpy as np
from matplotlib.cm import RdYlBu_r as cMap
import scipy.stats as st 



class Animation:

    DAYS = 200
    SUBFRAMES = 1
    GRIDSIZE = 30

    def __init__(self):
        self.elapsed = []

        self.grid = Grid(self.GRIDSIZE, 0.05, 0.5, 0.005)
        print("number of creatures: ", len(self.grid.creatureList))
        self.grid.updateAll()
        self.xStat = [0,1]
        self.yStat = self.grid.histCreatures*2
        
        plt.style.use("dark_background")
        
        # fig = plt.figure(figsize=(16,10), constrained_layout=True)
        figStat = plt.figure(figsize=(16,10))
        
        # fig.tight_layout()
        figStat.tight_layout()

        # gs = fig.add_gridspec(nrows=4, ncols=3)

        # self.axCreatures = fig.add_subplot(gs[:,0:1])
        # self.axCreatures.axis('off')

        self.axAni = figStat.add_subplot(121)
        self.axAni.axis('off')

        # self.axStat = SubplotZero(figStat, 122)
        # figStat.add_subplot(self.axStat)
        self.axStat = figStat.add_subplot(122)
        # self.arrowSpines(self.axStat)


        # animate random movement without any properties
        # self.statGraph, = plt.plot([], [], '-o', markersize=2)

        # self.axPf = fig.add_subplot(gs[0,2:3])
        # self.imPf = self.axPf.imshow(self.grid.creatureList[0].finalCosts.astype(float), vmin=0, vmax=1.2, cmap='magma')

        # self.axFood = fig.add_subplot(gs[1,2:3])

        # self.axGen1 = fig.add_subplot(gs[2,2:4])
        # self.axGen1.set_title('energyChildrenThreshold (x) vs nChildren (y)')

        # self.axGen2 = fig.add_subplot(gs[3,2:4])
        # self.axGen2.set_title('toEnemies (x) vs genomeThreshold (y)')

        # self.fig = fig

        self.ani = FuncAnimation(figStat, 
                                 func = self.update, 
                                 init_func = self.init, 
                                 frames = self.DAYS+1, 
                                 interval =100, 
                                 repeat = True)

        # FFwriter = FFMpegWriter(fps=10)
        # self.ani.save('ani3.mp4', writer=FFwriter)
        plt.show()
            

        # with open('log.csv', 'w') as f:
        #     writer = csv.writer(f)
        #     for row in Creature.data:
        #         writer.writerow(row)

    def init(self):
        pass

    def update(self, iteration):
        start = time()
        self.grid.updateAll()
        self.elapsed.append(time() - start)
        # self.animateStat(iteration)
        self.animateHist()

        if not iteration % self.SUBFRAMES:
            start = time()
            self.animateCreatures(self.axAni, iteration)
            # self.animateFood()
            # self.animateGen1()
            # self.animateGen2()
            # self.animatePerceptionField()
            print('plot performance time for plotting: ', time()-start)
            print('avg update performance time: ', sum(self.elapsed)/self.SUBFRAMES)
            print("number of creatures: ", len(self.grid.creatureList))
            print("current itartion number: ", iteration)
            self.elapsed.clear()

        return

    def animateCreatures(self, ax, day):
        ax.clear()
        ax.axis('off')
        ax.set_xlim(self.grid.ghostZone-2, self.GRIDSIZE + self.grid.ghostZone+2)
        ax.set_ylim(self.grid.ghostZone-2, self.GRIDSIZE + self.grid.ghostZone+2)
        ax.set_title('Day {}'.format(day))

        xFood, yFood = np.where(self.grid.foodGrid !=0)
        ax.scatter(xFood, yFood, marker='*', s=80, c='green')

        # mark the creature, whose perceptionfield is visualized
        if len(self.grid.creatureList):
            self.grid.creatureList[0].color = 'yellow'
        
        xCreatures, yCreatures, colors = zip(*[[c.x, c.y, c.color] for c in self.grid.creatureList])
        ax.scatter(xCreatures, yCreatures, s=160, c=colors)
        ax.set_title('Day {}'.format(day))

    # change this name
    def animateFood(self):
        self.axFood.clear()
        self.axFood.plot(range(min(len(self.grid.histFood),1000)), self.grid.histFood[-1000:], c="green")
        self.axFood.plot(range(min(len(self.grid.histCreatures),1000)), self.grid.histCreatures[-1000:], c="red")

    def animateGen1(self):
        self.axGen1.clear()

        for creature in self.grid.creatureList:
            self.axGen1.scatter(creature.genome.get('energyChildrenThreshold'), creature.genome.get('nChildren'),s=1, marker=',')

    def animateGen2(self):
        self.axGen2.clear()
        for creature in self.grid.creatureList:
            self.axGen2.scatter(creature.genome.get('toEnemies'), creature.genome.get('genomeThreshold'), marker=',')

    def animatePerceptionField(self):
        if len(self.grid.creatureList):
            self.imPf.set_data(self.grid.creatureList[0].finalCosts.astype(float))
            self.axPf.set_title("PF ID: " + str(self.grid.creatureList[0]._id))

    # animate random movement without any properties
    def animateStat1(self, day):
        self.yStat += [self.grid.histCreatures[-1]] * 2
        self.xStat.extend([day+1, day+2])
        self.statGraph.set_data(self.xStat, self.yStat)

    def animateHist(self):
        _, maxSpeed = self.grid.creatureList[0].genome.bounds['speed']
        x = np.linspace(1, maxSpeed, 4*maxSpeed)

        self.axStat.clear()
        self.axStat.set_title('')
        self.axStat.set_xlim(1, maxSpeed)
        self.axStat.set_ylim(0, 3)

        n, bins, patches = self.axStat.hist(self.grid.histSpeeds,
                                            range = [1, maxSpeed],
                                            density = True,
                                            bins = maxSpeed*5)
        
        kde = st.gaussian_kde(self.grid.histSpeeds).pdf(x)
        self.axStat.plot(x, kde, 'r-', label='PDF', color='yellow')

        for i, p in enumerate(patches):
            plt.setp(p, 'facecolor', cMap(round(i/(maxSpeed*5-1) * 254)))

    def animateBarplot(self):
        self.axStat.clear()
        self.axStat.set_xlim(0, 8)
        self.axStat.set_ylim(0, 150)
        distr = np.zeros(6, dtype=int) 
        start, step = 254/12, 254/6
        colors = [cMap(round(start + i * step)) for i in range(6)]
        for creature in self.grid.creatureList:
            distr[round(creature.genome.get('speed'))-1] += 1
        self.axStat.bar(range(1,7), distr, color=colors)
        
        
    def arrowSpines(self, ax):
        rc = {"xtick.direction" : "inout", 
              "ytick.direction" : "inout", 
              "xtick.major.size" : 5, 
              "ytick.major.size" : 5}

        with plt.rc_context(rc):
            ax.spines['left'].set_position('zero')
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_position('zero')
            ax.spines['top'].set_visible(False)

            ax.set_xlabel('Days')
            ax.set_ylabel('Creatures')
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')

            # make arrows
# =============================================================================
#           ARROWS NOT VISIBLE WHY?
# =============================================================================
            ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
                    transform=ax.get_yaxis_transform(), clip_on=False)
            ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
                    transform=ax.get_xaxis_transform(), clip_on=False)


Animation()