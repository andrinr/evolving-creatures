import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from evolution import Evolution

# Parameters
NFRAMES = 100

evolution = Evolution((200,200))

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(1, 2)
axLeft = fig.add_subplot(gs[:,0])
axRight = fig.add_subplot(gs[:,1])

foodPlot = axLeft.imshow(evolution.foodGrid)

def update(time):
    evolution.update()
    foodPlot.imshow(evolution.foodGrid)
    return


animation = FuncAnimation(fig, update, frames=range(NFRAMES), interval=10, repeat=False)

plt.show()