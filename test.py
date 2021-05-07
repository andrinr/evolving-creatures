import numpy as np
import matplotlib.pyplot as plt

a = np.array([
    [0, 1, 0],
    [0, 0, 0],
    [0, 1, 0]
])

print(a[-1,1])
print(np.argwhere(a[0:1,0:1]))

ax = plt.subplot()

ax.set_xlim(-1,3)
ax.set_ylim(3,-1)

ax.scatter([0],[2])
ax.imshow(a, origin='upper')

plt.show()