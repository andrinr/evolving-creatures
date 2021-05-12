import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from grid import Grid
import time
# Parameters
NFRAMES = 1000
SUBFRAMES = 50
GRIDSIZE = 100

grid = Grid(GRIDSIZE, 0.001, 0.03, 0.0002)

print("number of creatures: ", len(grid.creatureList))

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(4, 3)
axLeft = fig.add_subplot(gs[:,0:2])
axPf = fig.add_subplot(gs[0,2])
axFood = fig.add_subplot(gs[1,2:3])

iteration = 0
def update(f):
    global iteration
    # For efficency do not plot every update
    elapsed = 0
    for i in range(SUBFRAMES):
        iteration += 1
        start = time.perf_counter()
        grid.updateAll()
        end = time.perf_counter()
        elapsed += end - start
    
    print('avg update performance time: ', elapsed/SUBFRAMES)

    start = time.perf_counter()
    axLeft.clear()
    axPf.clear()
    axFood.clear()
    axLeft.set_xlim(Grid.ghostZone-1,GRIDSIZE+Grid.ghostZone)
    axLeft.set_ylim(GRIDSIZE+Grid.ghostZone,Grid.ghostZone-1)
    grid.plotAll(axLeft, axPf, axFood)
    end = time.perf_counter()
    elapsed = end - start

    print('plot performance time: ', elapsed)

    print("current itartion number: ", iteration)
    return

animation = FuncAnimation(fig, update, frames=range(NFRAMES), interval=300, repeat=False)

plt.show()



