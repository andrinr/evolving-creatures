import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from evolution import Evolution

# Parameters
NFRAMES = 100
SUBFRAMES = 100
VDIST = 3

evolution = Evolution((200,200), VDIST)

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(1, 2)
axLeft = fig.add_subplot(gs[:,0])
axRight = fig.add_subplot(gs[:,1])

foodPlot = axLeft.imshow(evolution.foodGrid)

def update(time):
    # For efficency do not draw every update
    for i in range(SUBFRAMES):
        evolution.update()

    foodPlot.set_array(evolution.foodGrid)
    return


animation = FuncAnimation(fig, update, frames=range(NFRAMES), interval=10, repeat=False)

plt.show()