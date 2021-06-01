from creature import Creature
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from grid import Grid
from  time import time
import csv
import numpy as np
from matplotlib.cm import RdYlBu_r as cMap
import scipy.stats as st 



GRID_SIZE = 50
CREATURE_RATE = 0.005
INIT_FOOD_RATE = 0.001
GROW_FOOD_RATE = 0.01


class Animation:
    DAYS = 500
    SUBFRAMES = 1
    count = 0
    def __init__(self, grid):
        self.count += 1 
        self.elapsed = []
        self.grid = grid
        print("number of creatures: ", len(self.grid.creatureList))
        self.grid.updateAll()
        self.xStat = [0,1]
        self.yStat = self.grid.histCreatures*2
        
        plt.style.use("dark_background")
        
        # fig = plt.figure(figsize=(16,10), constrained_layout=True)
        figStat = plt.figure(figsize=(16,10))
        self.figStat = figStat
        # fig.tight_layout()
        figStat.tight_layout()

        # gs = fig.add_gridspec(nrows=4, ncols=3)

        # self.axCreatures = fig.add_subplot(gs[:,0:1])
        # self.axCreatures.axis('off')


        # animate random movement without any properties
        # self.linePlot()
        # self.plotHist()
        # self.plotSpeedVsPFsize()
        self.plot3D()

        # self.arrowSpines(self.axStat)0

        # self.axPf = fig.add_subplot(gs[0,2:3])
        # self.imPf = self.axPf.imshow(self.grid.creatureList[0].finalCosts.astype(float), vmin=0, vmax=1.2, cmap='magma')

        # self.axFood = fig.add_subplot(gs[1,2:3])

        # self.axGen1 = fig.add_subplot(gs[2,2:4])
        # self.axGen1.set_title('energyChildrenThreshold (x) vs nChildren (y)')

        # self.axGen2 = fig.add_subplot(gs[3,2:4])
        # self.axGen2.set_title('toEnemies (x) vs genomeThreshold (y)')

        # self.fig = fig



        # with open('log.csv', 'w') as f:
        #     writer = csv.writer(f)
        #     for row in Creature.data:
        #         writer.writerow(row)

    def init(self):
        pass
        
    def update(self, iteration):
        # start = time()
        self.grid.updateAll()
        # self.elapsed.append(time() - start)
        
        
        # animate random movement with speed properties and also speed/PF properties
        self.animateHistSpeed()


        if not iteration % self.SUBFRAMES:
            # start = time()
            self.animateCreatures(self.axAni, iteration)
            # self.animateFood()
            # self.animateGen1()
            # self.animateGen2()
            # self.animatePerceptionField()
            # print('plot performance time for plotting: ', time()-start)
            # print('avg update performance time: ', sum(self.elapsed)/self.SUBFRAMES)
            # print("number of creatures: ", len(self.grid.creatureList))
            # print("current itartion number: ", iteration)
            # self.elapsed.clear()

        return self.axAni,

    def animateCreatures(self, ax, day):
        ax.clear()
        ax.axis('off')
        ax.set_xlim(self.grid.ghostZone-2, self.grid.N + self.grid.ghostZone+2)
        ax.set_ylim(self.grid.ghostZone-2, self.grid.N + self.grid.ghostZone+2)
        ax.set_title('Day {}'.format(day))

        xFood, yFood = np.where(self.grid.foodGrid !=0)
        ax.scatter(xFood, yFood, marker='H', s=100, c='lawngreen')

        # # mark the creature, whose perceptionfield is visualized
        # if len(self.grid.creatureList):
        #     self.grid.creatureList[0].color = 'yellow'
        
        xCreatures, yCreatures, colors, sizes = zip(*[[c.x, c.y, c.color, (22*c.size)**1.2] for c in self.grid.creatureList])
        ax.scatter(xCreatures, yCreatures, s=sizes, c=colors)
        ax.set_title('Day {}'.format(day))

        xEaten, yEaten = np.where(self.grid.eaten != 0)
        ax.scatter(xEaten, yEaten, marker='X', s=180, c='red')

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

# =============================================================================
# 3D plot of speed, perception field size and creature size
# =============================================================================
    def plot3D(self):
        gs = self.figStat.add_gridspec(nrows=12, ncols=12)
        
        self.axCreatures = self.figStat.add_subplot(gs[0:6, 0:6])
        self.axCreatures.axis('off')

        self.ax3D = self.figStat.add_subplot(gs[0:6, 6:12], projection='3d')
        self.axHistSpeed = self.figStat.add_subplot(gs[6:12, 0:4])
        self.axHistSize= self.figStat.add_subplot(gs[6:12, 4:8])
        self.axHistPFsize = self.figStat.add_subplot(gs[6:12,8:12])
        
        self.axHistSpeed.spines['right'].set_visible(False)
        self.axHistSpeed.spines['top'].set_visible(False)
        self.axHistSize.spines['right'].set_visible(False)
        self.axHistSize.spines['top'].set_visible(False)
        self.axHistPFsize.spines['right'].set_visible(False)
        self.axHistPFsize.spines['top'].set_visible(False)

        ani = FuncAnimation(self.figStat, 
                            func = self.update3D,
                            init_func = self.init,
                            frames = self.DAYS+1,
                            interval =10,
                            repeat = True)

        FFwriter = FFMpegWriter(fps=10)
        ani.save('3D_pop'+str(self.count)+'_gfd'+str(self.grid.growFoodDensity)+'.mp4', writer=FFwriter)
        plt.show()


    def update3D(self, i):
        self.grid.updateAll()
        self.animateHist(self.axHistSpeed, 'speed', self.grid.histSpeeds)
        self.animateHist(self.axHistSize, 'size', self.grid.histSizes)
        self.animateHist(self.axHistPFsize, 'pfSize', self.grid.histPFsize)

        ax = self.ax3D
        ax.clear()
        ax.set_title("number of creatures: {}".format(len(self.grid.creatureList)))
        ax.set_xlabel('creature Size')
        ax.set_ylabel('perceptionfield size')
        ax.set_zlabel('speed')

        ax.set_xlim(1,6)
        ax.set_ylim(4, 10)
        ax.set_zlim(1, 8)

        ax.scatter(xs = self.grid.histSizes,
                   ys = self.grid.histPFsize, 
                   zs = self.grid.histSpeeds,
                   s = (np.array(self.grid.histSizes)*22)**1.1,
                   c = self.grid.histColors)

        if not i % self.SUBFRAMES:
            self.animateCreatures(self.axCreatures, i)

# =============================================================================
# speed histogram
# =============================================================================
    def plotHist(self):
        self.axAni = self.figStat.add_subplot(121)
        self.axAni.axis('off')
        self.axStat = self.figStat.add_subplot(122)
        ani = FuncAnimation(self.figStat, 
                            func = self.updateHist, 
                            init_func = self.init, 
                            frames = self.DAYS+1, 
                            interval =10, 
                            repeat = True)

        FFwriter = FFMpegWriter(fps=10)
        ani.save('Speed_vs_PFsize.mp4', writer=FFwriter)
        plt.show()

    def updateHist(self, i):
        self.grid.updateAll()
        self.animateHistSpeed(self.axStat, 'speed', self.grid.histSpeeds, 'Speed & Sense')
        if not i % self.SUBFRAMES:
            self.animateCreatures(self.axAni, i)
        return self.axAni,

    def animateHist(self, ax, gene, values, title=''):
        if self.grid.creatureList[0]:
            minVal, maxVal = self.grid.creatureList[0].genome.bounds[gene]  
            x = np.linspace(1, maxVal, 4*maxVal)
    
            ax.clear()
            ax.set_xlim(minVal-1, maxVal+1)
            ax.set_ylim(0, 1)
            ax.set_xlabel(gene)
            ax.set_title(title)
            # self.addText(4.8,2.7)

            n, bins, patches = ax.hist(values,
                                       range = [1, maxVal],
                                       density = True,
                                       bins = maxVal+1)

            kde = st.gaussian_kde(values).pdf(x)
            ax.plot(x, kde, '-', label='PDF', color='yellow')

            fact = 254/(maxVal+1)
            for i, p in enumerate(patches):
                plt.setp(p, 'facecolor', cMap(round(i * fact)))


# =============================================================================
# Speed vs. Perceptionfield size
# =============================================================================
    def plotSpeedVsPFsize(self):
        self.axStat = self.figStat.add_subplot(122)
        self.axAni = self.figStat.add_subplot(121)
        self.axAni.axis('off')

        ani = FuncAnimation(self.figStat, 
                            func = self.updateSpeedPF, 
                            init_func = self.init, 
                            frames = self.DAYS+1, 
                            interval =10, 
                            repeat = True)

        FFwriter = FFMpegWriter(fps=10)
        ani.save('Speed_vs_PFsize.mp4', writer=FFwriter)
        plt.show()

    def updateSpeedPF(self, iteration):
        self.grid.updateAll()

        self.axStat.clear()
        self.axStat.spines['right'].set_visible(False)
        self.axStat.spines['top'].set_visible(False)
        self.axStat.set_xlabel('Speed')
        self.axStat.set_ylabel('Sense Size')
        self.axStat.set_title('Speed vs Sense Size')
        self.axStat.set_xlim(0, 7)
        self.axStat.set_ylim(4, 10)
        self.addText(5, 9.5)
        self.axStat.scatter(x = self.grid.histSpeeds, 
                            y = self.grid.histPFsize,
                            s = 80,
                            c = self.grid.histColors,
                            edgecolor = self.grid.edgeColors)

        if not iteration % self.SUBFRAMES:
            self.animateCreatures(self.axAni, iteration)
        return self.axAni,


# =============================================================================
# animate random movement without any properties
# =============================================================================
    def linePlot(self):
        self.axAni = self.figStat.add_subplot(121)
        self.axAni.axis('off')
        self.axStat = self.figStat.add_subplot(122)
        self.statGraph, = self.axStat.plot([], [], '-', markersize=20)
        self.axStat.set_xlim(0,self.DAYS)
        self.axStat.set_ylim(0, 600)

        ani = FuncAnimation(self.figStat, 
                            func = self.updateLinePlot, 
                            init_func = self.init, 
                            frames = self.DAYS+1, 
                            interval =10, 
                            repeat = True)

        FFwriter = FFMpegWriter(fps=10)
        ani.save('Speed_vs_PFsize.mp4', writer=FFwriter)
        plt.show()

    def updateLinePlot(self, i):
        self.statGraph.set_data(self.xStat, self.yStat)
        self.grid.updateAll()
        self.xStat.extend([i+1, i+2])
        self.yStat += [self.grid.histCreatures[-1]] * 2

        if not i % self.SUBFRAMES:
            self.animateCreatures(self.axAni, i)
        return self.statGraph,


    def addText(self, x, y):
            self.axStat.text(x, 
                             y, 
                             'Grid Size: {}x{}\nCreature Rate: {}\nInit Food Rate: {}\nGrow Food Rate: {}'.format(self.grid.N,
                                                                                                                  self.grid.N,
                                                                                                                  self.grid.creatureDensity,
                                                                                                                  self.grid.initFoodDensity,
                                                                                                                  self.grid.growFoodDensity),
                             bbox = dict(facecolor='blue', alpha=.5))

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
            # ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
            #         transform=ax.get_yaxis_transform(), clip_on=False)
            # ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
            #         transform=ax.get_xaxis_transform(), clip_on=False)

grid = Grid(GRID_SIZE, CREATURE_RATE, INIT_FOOD_RATE, GROW_FOOD_RATE)
Animation(grid)