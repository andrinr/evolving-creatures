from creature import Creature
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from grid import Grid
from  time import time
import csv
import numpy as np
from genome import Genome


class Animation:

    DAYS = 1000
    SUBFRAMES = 10
    GRIDSIZE = 100

    PLOTOUT = False

    def __init__(self):
        self.elapsed = []

        self.grid = Grid(self.GRIDSIZE, 0.003, 0.004, 0.001)
        print("number of creatures: ", len(self.grid.creatureList))
        self.grid.updateAll(0)

        if self.PLOTOUT :
            plt.style.use("dark_background")
            fig = plt.figure(figsize=(16,10), constrained_layout=True)
            fig.tight_layout()
            
            gs = fig.add_gridspec(nrows=4, ncols=3)
            
            self.axLeft = fig.add_subplot(gs[:,0:2])
            self.axLeft.axis('off')

            self.axPf = fig.add_subplot(gs[0,2:3])
            self.imPf = self.axPf.imshow(self.grid.creatureList[0].finalCosts.astype(float), vmin=0, vmax=1.2, cmap='magma')

            self.axFood = fig.add_subplot(gs[1,2:3])

            self.axGen1 = fig.add_subplot(gs[2,2:4])
            self.axGen1.set_title('energyChildrenThreshold (x) vs nChildren (y)')

            self.axGen2 = fig.add_subplot(gs[3,2:4])
            self.axGen2.set_title('toEnemies (x) vs genomeThreshold (y)')

            self.fig = fig

            self.ani = FuncAnimation(self.fig, 
                                    func = self.update, 
                                    init_func = self.init, 
                                    frames = self.DAYS+1, 
                                    interval = 10, 
                                    repeat = False)

            #FFwriter = FFMpegWriter(fps=10)
            #self.ani.save('simpleLife.mp4', writer=FFwriter)
            plt.show()
        else:
            for i in range(self.DAYS):
                self.update(i)

            with open('./logs/creature.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(Genome.properties[:,0].tolist() + ['t', 'age', 'causeOfDeath'])
                for row in Creature.data:
                    writer.writerow(row)

            with open('./logs/general.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['nCreatures', 'nFood', 't'])
                for i in range(len(self.grid.histFood)):
                    writer.writerow([self.grid.histCreatures[i], self.grid.histFood[i], i])

    def init(self):
        pass

    def update(self, iteration):
        start = time()
        self.grid.updateAll(iteration)
        self.elapsed.append(time() - start)
    
        if not iteration % self.SUBFRAMES:
            start = time()
            
            if self.PLOTOUT : self.updateSubPlots(iteration)

            print('plot performance time for plotting: ', time()-start)
            print('avg update performance time: ', sum(self.elapsed)/self.SUBFRAMES)
            print("number of creatures: ", len(self.grid.creatureList))
            print("current itartion number: ", iteration)
            self.elapsed.clear()

        return

    def updateSubPlots(self, day):
        self.axLeft.clear()
        self.axLeft.axis('off')
        self.axLeft.set_xlim(self.grid.ghostZone-2, self.GRIDSIZE + self.grid.ghostZone+2)
        self.axLeft.set_ylim(self.grid.ghostZone-2, self.GRIDSIZE + self.grid.ghostZone+2)
        self.axLeft.set_title('Day {}'.format(day))

        self.axFood.clear()
        self.axFood.plot(range(min(len(self.grid.histFood),1000)), self.grid.histFood[-1000:], c="green")
        self.axFood.plot(range(min(len(self.grid.histCreatures),1000)), self.grid.histCreatures[-1000:], c="red")

        self.axGen1.clear()
        self.axGen1.set_xlim(0,15)
        self.axGen1.set_ylim(0,15)

        self.axGen2.clear()

        # plot food
        xFood, yFood = np.where(self.grid.foodGrid !=0)
        self.axLeft.scatter(xFood, yFood, marker='*', s=80, c='green')

        # plot perceptionfield
        if len(self.grid.creatureList):
            self.imPf.set_data(self.grid.creatureList[0].finalCosts.astype(float))
            self.axPf.set_title("PF ID: " + str(self.grid.creatureList[0]._id))
            self.grid.creatureList[0].color = 'yellow'

        for creature in self.grid.creatureList:
            # plot creatures
            self.axLeft.scatter(creature.x, creature.y, c=creature.color, s=150)
            # plot ??
            self.axGen1.scatter(creature.genome.get('energyChildrenThreshold'), creature.genome.get('nChildren'),s=1, marker=',')    
            # plot ??
            self.axGen2.scatter(creature.genome.get('toEnemies'), creature.genome.get('genomeThreshold'), marker=',')

            #self.axl.annotate(creature.id, (creature.y, creature.x), c='black')



Animation()