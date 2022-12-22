import numpy as np
from itertools import accumulate, islice

with open('input.txt') as f:
    trees = np.genfromtxt(f, dtype=int, delimiter=1)

def outside(treeline):
    def visibile(state, tree):
        _, highest = state
        if tree > highest:
            return True, tree
        return False, highest
    visibilities = accumulate(treeline, visibile, initial=(False,-1))
    return np.fromiter((v for v,_ in islice(visibilities,1,None)),bool)

print(np.sum(np.any(
    np.array([
        np.apply_along_axis(outside,0,trees),
        np.apply_along_axis(outside,1,trees),
        np.flipud(np.apply_along_axis(outside,0,np.flipud(trees))),
        np.fliplr(np.apply_along_axis(outside,1,np.fliplr(trees)))
    ]),
    axis=0
)))

def visibility(treeline):
    def visible(state, tree):
        _, distances = state
        distance = distances[tree]
        distances[:tree+1] = 1
        distances[tree+1:] += 1
        return distance, distances
    visibilities = accumulate(treeline, visible, initial=(0, np.zeros(10,int)))
    return np.fromiter((d for d,_ in islice(visibilities,1,None)),int)

print(np.max(np.prod(
    np.array([
        np.apply_along_axis(visibility,0,trees),
        np.apply_along_axis(visibility,1,trees),
        np.flipud(np.apply_along_axis(visibility,0,np.flipud(trees))),
        np.fliplr(np.apply_along_axis(visibility,1,np.fliplr(trees)))
    ]),
    axis=0
)))
