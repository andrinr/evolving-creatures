import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from grid import Grid
# Parameters
NFRAMES = 100
SUBFRAMES = 10
GRIDSIZE = 100

grid = Grid(GRIDSIZE, 0.001, 0.1)

print("number of creatures: ", len(grid.creatureList))

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(1, 3)
axLeft = fig.add_subplot(gs[:,0:2])
axRight = fig.add_subplot(gs[:,2])

iteration = 0
def update(time):
    axLeft.clear()
    axLeft.set_xlim(Grid.ghostZone-1,GRIDSIZE+Grid.ghostZone)
    axLeft.set_ylim(GRIDSIZE+Grid.ghostZone,Grid.ghostZone-1)
    grid.plotAll(axLeft)

    global iteration
    # For efficency do not plot every update
    for i in range(SUBFRAMES):
        iteration += 1
        grid.updateAll()

    print("current itartion number: ", iteration)
    return

animation = FuncAnimation(fig, update, frames=range(NFRAMES), interval=100, repeat=False)

plt.show()



