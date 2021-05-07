import numpy as np
import matplotlib.pyplot as plt

a = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
])

print(np.argwhere(a)-np.array([1,1]))

plt.imshow(a, origin='upper')

plt.show()