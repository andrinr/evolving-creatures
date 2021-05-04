import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from evolution import Evolution

# Parameters
NFRAMES = 1<<10
SUBFRAMES = 1
VDIST = 3
NCREATURES = 10

evolution = Evolution((200,200), VDIST, NCREATURES)

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(1, 2)
axLeft = fig.add_subplot(gs[:,0])
axRight = fig.add_subplot(gs[:,1])

foodPlot = axLeft.imshow(evolution.foodGrid)

def fetchCreaturePositions(evolution):
    creaturePositions = np.zeros((len(evolution.creatureList), 2))
    for i in range(len(evolution.creatureList)):
        creaturePositions[i] = evolution.creatureList[i].pos

    return creaturePositions

creaturePositions = fetchCreaturePositions(evolution)
creaturePlot = axLeft.scatter(creaturePositions[:,0], creaturePositions[:,1])


def update(time):
    global foodPlot, creaturePlot, evolution
    # For efficency do not draw every update
    for i in range(SUBFRAMES):
        evolution.update()

    foodPlot.set_array(evolution.foodGrid)

    creaturePositions = fetchCreaturePositions(evolution)
    creaturePlot.set_offsets(creaturePositions)
    return


animation = FuncAnimation(fig, update, frames=range(NFRAMES), interval=10, repeat=False)

plt.show()