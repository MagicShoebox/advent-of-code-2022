import numpy as np

with open('input.txt') as f:
    lines = (line.rstrip() for line in f)
    cubes = [tuple(int(x) for x in line.split(',')) for line in lines]

origin = np.array(cubes).min(0)
lava_shape = np.array(cubes).max(0) - origin + 1
lava = np.zeros(lava_shape, dtype=int)
for cube in cubes:
    lava[tuple(cube - origin)] = 1

padded = np.pad(lava, 1)

def slicer(dimensions):
    slices = [slice(None, -2), slice(2, None)]
    return [
        tuple(slices[front_back] if axis==face_dim else slice(1, -1) 
        for axis in range(dimensions)
        )
        for face_dim in range(dimensions)
        for front_back in range(2)
    ]

adjacent = np.sum([padded[s] for s in slicer(lava.ndim)], 0)
exposed = np.sum(np.multiply(lava, 2*adjacent.ndim - adjacent))
print(exposed)

stack = [tuple(0 for _ in range(padded.ndim))]
while stack:
    index = stack.pop()
    if all(0 <= i < d for i,d in zip(index, padded.shape)) and padded[index] == 0:
        padded[index] = 1
        stack.extend(
            tuple(index + i*np.identity(lava.ndim, dtype=int)[d])
            for d in range(lava.ndim)
            for i in [-1,1]
        )

bubbles = 1 - padded[tuple(slice(1,-1) for _ in range(padded.ndim))]
print(exposed - np.sum(np.multiply(bubbles, adjacent)))
