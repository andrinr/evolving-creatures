import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from evolution import Evolution

# Parameters
NFRAMES = 1<<10
SUBFRAMES = 1
NCREATURES = 10
GRIDSIZE = 50

evolution = Evolution(GRIDSIZE, NCREATURES)

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(1, 2)
axLeft = fig.add_subplot(gs[:,0])
axRight = fig.add_subplot(gs[:,1])

def update(time):
    # For efficency do not draw every update
    for i in range(SUBFRAMES):
        evolution.update()

    axLeft.clear()
    axLeft.set_xlim(0,GRIDSIZE)
    axLeft.set_ylim(0,GRIDSIZE)
    evolution.plot(axLeft)
    return

animation = FuncAnimation(fig, update, frames=range(NFRAMES), interval=10, repeat=False)

plt.show()