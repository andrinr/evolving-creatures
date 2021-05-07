import numpy as np

# Symmetric rounding of 2D vector where < 0 is floor and > 0 is ceil
def sRound(v):
    pos = v.astype(float)
    np.ceil(v, where= v>0, out=pos)
    np.floor(v, where= v<0, out=pos)
    return pos.astype(int)

def normalize(v):
    norm = np.linalg.norm(v)
    return v/norm if norm else v

def closestPoint(arr, pos):
    dist = (arr[:, 0] - pos[0])**2 + (arr[:, 1] - pos[1])**2
    return arr[dist.argmin()]