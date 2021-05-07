import numpy as np

# Symmetric rounding of 2D vector where < 0 is floor and > 0 is ceil
def sRound(v):
    v_ = np.array([0,0])
    if v[0] > 0:
        v_[0] = np.ceil(v[0])
    else:
        v_[0] = np.floor(v[0])
    
    if v[1] > 0:
        v_[1] = np.ceil(v[1])
    else:
        v_[1] = np.floor(v[1]) 

    return v_

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
        return v
    return v / norm

def closestPoint(arr, pos):
    dist = (arr[:, 0] - pos[0])**2 + (arr[:, 1] - pos[1])**2
    return arr[dist.argmin()]