import numpy as np
from itertools import cycle, islice, product, starmap

with open('input.txt') as f:
    grove = np.genfromtxt(f, dtype=str, delimiter=1, comments=None)
    
elves = grove == '#'

def crop(arr):
    active = np.nonzero(arr)
    area = zip(np.min(active, 1), 1 + np.max(active, 1))
    return arr[tuple(starmap(slice, area))]

def disperse(elves, round):
    padded = np.pad(elves, 2)
    slices = [slice(None, -4), slice(1, -3), slice(2, -2), slice(3, -1), slice(4, None)]
    neighbors = [padded[p] for i,p in enumerate(product(slices[1:-1], slices[1:-1])) if i != 4]
    updated = elves & (np.sum(neighbors, 0) == 0)
    elves ^= updated
    if not np.any(elves):
        return updated, True
    updated = np.pad(updated, 2)

    NW, N, NE, W, E, SW, S, SE = neighbors
    quadrants = [
        ((slices[1], slices[2]), (slices[0], slices[2]), [NW, N, NE]),
        ((slices[3], slices[2]), (slices[4], slices[2]), [SW, S, SE]),
        ((slices[2], slices[1]), (slices[2], slices[0]), [NW, W, SW]),
        ((slices[2], slices[3]), (slices[2], slices[4]), [NE, E, SE]),
    ]
    r = round % len(quadrants)
    for dest, conf, quad in islice(cycle(quadrants), r , r+len(quadrants)):
        movers = elves & (np.sum(quad, 0) == 0)
        elves ^= movers
        conflict = movers & updated[dest]
        movers ^= conflict
        updated[2:-2,2:-2] |= conflict
        updated[dest] ^= conflict
        updated[conf] |= conflict
        updated[dest] |= movers
    updated[2:-2,2:-2] |= elves
    return crop(updated), False

for r in range(10):
    elves, _ = disperse(elves, r)
print(elves.size - np.count_nonzero(elves))

round = 10
done = False
while not done:
    elves, done = disperse(elves, round)
    round += 1

print(round)
