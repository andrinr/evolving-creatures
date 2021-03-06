from creature import Creature
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from grid import Grid
from  time import daylight, time
import csv
import numpy as np
from matplotlib.cm import RdYlBu_r as cMap
import scipy.stats as st 
import yaml

PARAMETERS = {}

class Animation:
    def __init__(self):
        self.elapsed = []
        self.GRIDSIZE = PARAMETERS['GRID_SIZE']
        self.grid = Grid(self.GRIDSIZE)
        print("number of creatures: ", len(self.grid.creatureList))
        self.grid.updateAll(0)

        if PARAMETERS['VIDEO'] or PARAMETERS['PLOT']:
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

            self.axStat = figStat.add_subplot(122)
            self.axStat.spines['right'].set_visible(False)
            self.axStat.spines['top'].set_visible(False)
            self.axStat.set_xlim(1, 6)
            self.axStat.set_ylim(0, 100)

        # self.arrowSpines(self.axStat)0


        # animate random movement without any properties
        # self.statGraph, = plt.plot([], [], 'o', markersize=20, color)

        # self.axPf = fig.add_subplot(gs[0,2:3])
        # self.imPf = self.axPf.imshow(self.grid.creatureList[0].finalCosts.astype(float), vmin=0, vmax=1.2, cmap='magma')

        # self.axFood = fig.add_subplot(gs[1,2:3])

        # self.axGen1 = fig.add_subplot(gs[2,2:4])
        # self.axGen1.set_title('energyChildrenThreshold (x) vs nChildren (y)')

        # self.axGen2 = fig.add_subplot(gs[3,2:4])
        # self.axGen2.set_title('toEnemies (x) vs genomeThreshold (y)')

        # self.fig = fig

        if PARAMETERS['VIDEO'] or PARAMETERS['PLOT']: 
            self.ani = FuncAnimation(figStat, 
                                 func = self.update, 
                                 init_func = self.init, 
                                 frames = PARAMETERS['DAYS']+1, 
                                 interval =10, 
                                 repeat = False)

        if PARAMETERS['VIDEO']:
            FFwriter = FFMpegWriter(fps=10)
            self.ani.save(PARAMETERS['VIDEO_NAME'], writer=FFwriter)

        if PARAMETERS['PLOT'] or PARAMETERS['VIDEO']:
            plt.show()
        
        if PARAMETERS['CSV'] and not (PARAMETERS['VIDEO'] or PARAMETERS['PLOT']):
            for i in range(PARAMETERS['DAYS']+1):
                print(round(i/PARAMETERS['DAYS']*100, 1), 'percent done')
                self.update(i)

        if PARAMETERS['CSV']:
            with open(PARAMETERS['CSV_NAME_CREATURES'], 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['nKids', 'energyChildrenThreshold', 'speed', 'pfSize', 'cause', 't', 'age'])
                for row in Creature.log:
                    writer.writerow(row)

            with open(PARAMETERS['CSV_NAME_GENERAL'], 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['t', 'nCreatures', 'nFood'])
                for i in range(len(self.grid.histCreatures)):
                    writer.writerow([i, self.grid.histCreatures[i], self.grid.histFood[i]])

    def init(self):
        pass

    def update(self, iteration):
        # start = time()
        self.grid.updateAll(iteration)
        # self.elapsed.append(time() - start)
        
        # animate random movement without any properties
        # self.animateLinePlot(iteration)
        
        if (PARAMETERS['VIDEO'] or PARAMETERS['PLOT']):
            # animate random movement with speed properties and also speed/PF properties
            self.animateHistSpeed()

            # animate random mov. with speed vs. perceptual field size
            # self.animateSpeedPF()

            if not iteration % PARAMETERS['SUBFRAMES']:
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
        gz = PARAMETERS['GHOST_ZONE']
        ax.set_xlim(gz-2, PARAMETERS['GRID_SIZE'] + gz+2)
        ax.set_ylim(gz-2, PARAMETERS['GRID_SIZE'] + gz+2)
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
    def animateLinePlot(self, day):
        self.yStat += [self.grid.histCreatures[-1]] * 2
        self.xStat.extend([day+1, day+2])
        self.statGraph.set_data(self.xStat, self.yStat)

    # animate speed
    def animateHistSpeed(self):
        _, maxSpeed = self.grid.creatureList[0].genome.bounds['speed']
        x = np.linspace(1, maxSpeed, 4*maxSpeed)

        self.axStat.clear()
        self.axStat.set_xlim(1, maxSpeed)
        self.axStat.set_ylim(0, 3)
        self.axStat.set_xlabel('Speed')
        self.axStat.set_title('Speed & Sense')
        x, y = 4.8,2.7
        self.axStat.text(x, 
                         y, 
                         'Grid Size: {}x{}\nCreature Rate: {}\nInit Food Rate: {}\nGrow Food Rate: {}'.format(PARAMETERS['GRID_SIZE'],
                                                                                                              PARAMETERS['GRID_SIZE'],
                                                                                                              PARAMETERS['CREATURE_RATE'],
                                                                                                              PARAMETERS['CREATURE_RATE'],
                                                                                                              PARAMETERS['GROW_FOOD_RATE']),
                         bbox = dict(facecolor='blue', alpha=.5))

        n, bins, patches = self.axStat.hist(self.grid.histSpeeds,
                                            range = [1, maxSpeed],
                                            density = True,
                                            bins = maxSpeed*4)

        kde = st.gaussian_kde(self.grid.histSpeeds).pdf(x)
        self.axStat.plot(x, kde, '-', label='PDF', color='yellow')

        for i, p in enumerate(patches):
            plt.setp(p, 'facecolor', cMap(round(i/(maxSpeed*5-1) * 254)))

    def animateSpeedPF(self):
        # self.statGraph.set_data(self.grid.histSpeeds, self.grid.histPFsize)
        self.axStat.clear()
        self.axStat.spines['right'].set_visible(False)
        self.axStat.spines['top'].set_visible(False)
        self.axStat.set_xlim(1, 6)
        self.axStat.set_ylim(4, 10)
        self.axStat.scatter(x = self.grid.histSpeeds, 
                            y = self.grid.histPFsize,
                            s = 80,
                            c = self.grid.histColors)

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

def start(file):
    print("Loading params from: ", file)
    global PARAMETERS
    with open(file) as f:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        PARAMETERS = yaml.load(f, Loader=yaml.FullLoader)
        Creature.PARAMETERS = PARAMETERS
        Grid.PARAMETERS = PARAMETERS
    
    Animation()