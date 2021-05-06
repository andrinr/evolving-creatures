import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from grid import Grid
# Parameters
NFRAMES = 1<<10
SUBFRAMES = 1
GRIDSIZE = 10

grid = Grid(GRIDSIZE, 0.1, 0.1)

print("number of creatures: ", len(grid.creatureList))

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(1, 2)
axLeft = fig.add_subplot(gs[:,0])
axRight = fig.add_subplot(gs[:,1])

iteration = 0
def update(time):
    global iteration
    # For efficency do not draw every update
    for i in range(SUBFRAMES):
        iteration += 1
        grid.updateAll()

    axLeft.clear()
    axLeft.set_xlim(0,GRIDSIZE)
    axLeft.set_ylim(0,GRIDSIZE)
    
    grid.plotAll(axLeft)

    print("current itartion number: ", iteration)
    return

animation = FuncAnimation(fig, update, frames=range(NFRAMES), interval=200, repeat=False)

plt.show()



