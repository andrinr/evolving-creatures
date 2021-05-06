import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from creature import Creature
# Parameters
NFRAMES = 1<<10
SUBFRAMES = 1
GRIDSIZE = 50

Creature.initAll(GRIDSIZE, 0.1, 0.2)

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(1, 2)
axLeft = fig.add_subplot(gs[:,0])
axRight = fig.add_subplot(gs[:,1])

def update(time):
    # For efficency do not draw every update
    for i in range(SUBFRAMES):
        Creature.updateAll()

    axLeft.clear()
    axLeft.set_xlim(0,GRIDSIZE)
    axLeft.set_ylim(0,GRIDSIZE)
    
    Creature.plotAll(axLeft)
    return

animation = FuncAnimation(fig, update, frames=range(NFRAMES), interval=300, repeat=False)

plt.show()



