import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from grid import Grid
import time
# Parameters
NFRAMES = 100
SUBFRAMES = 100
GRIDSIZE = 120
PLOT = False

grid = Grid(GRIDSIZE, 0.02, 0.1, 0.0008)

print("number of creatures: ", len(grid.creatureList))

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(4, 3)
axLeft = fig.add_subplot(gs[:,0:2])
axPf = fig.add_subplot(gs[0,2:3])
axFood = fig.add_subplot(gs[1,2:3])
axGen1 = fig.add_subplot(gs[2,2:4])
axGen2 = fig.add_subplot(gs[3,2:4])

iteration = 0
grid.updateAll()

def update(f):
    global iteration

    if PLOT:
        start = time.perf_counter()
        axLeft.clear()
        axPf.clear()
        axFood.clear()
        axGen1.clear()
        axGen2.clear()
        axLeft.set_xlim(0,GRIDSIZE+2*Grid.ghostZone)
        axLeft.set_ylim(GRIDSIZE+2*Grid.ghostZone,0)
        axGen1.set_xlim(0,15)
        axGen1.set_ylim(0,15)
        grid.plotAll(axLeft, axPf, axFood, axGen1, axGen2)
        end = time.perf_counter()
        elapsed = end - start
        print('plot performance time(s): ', elapsed)

    # For efficency do not plot every update
    elapsed = 0
    for i in range(SUBFRAMES):
        iteration += 1
        start = time.perf_counter()
        grid.updateAll()
        end = time.perf_counter()
        elapsed += end - start
    
    print('avg update performance time(s): ', elapsed/SUBFRAMES)

    print("number of creatures: ", len(grid.creatureList))

    print("current itartion number: ", iteration)
    return



if PLOT:
    animation = FuncAnimation(fig, update, frames=range(NFRAMES), interval=10, repeat=False)
    plt.show()
else:
    for i in range(NFRAMES):
        update(i)



