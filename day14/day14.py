import numpy as np

with open('input.txt') as f:
    lines = (line.rstrip() for line in f)
    paths = (line.split(' -> ') for line in lines)
    rocks = [[[int(x) for x in point.split(',')] for point in path] for path in paths]

# print(min(x[1] for r in rocks for x in r))
# print(max(x[1] for r in rocks for x in r))
# print(min(x[0] for r in rocks for x in r))
# print(max(x[0] for r in rocks for x in r))

grid = np.zeros([200,1000], dtype='str')
grid[:,:] = '.'
grid[0,500] = '+'

for rock in rocks:
    for p1,p2 in zip(rock, rock[1:]):
        xmin, xmax = min(p1[0],p2[0]), max(p1[0], p2[0])
        ymin, ymax = min(p1[1],p2[1]), max(p1[1], p2[1])
        grid[ymin:ymax+1, xmin:xmax+1] = '#'

floor = 2 + max(p[1] for r in rocks for p in r)
grid[floor, :] = '#'

def fill(count, floor):
    while True:
        x,y = None,None
        s = (500,0)
        while s is not None and s[1] < floor - 1:
            x,y = s
            s = next((p for p in [(x,y+1), (x-1,y+1), (x+1,y+1)] if grid[p[::-1]] == '.'), None)
        if s is not None or grid[y,x] == 'o':
            break
        count += 1
        grid[y,x] = 'o'
    return count

count = fill(0, floor)
print(count)

count = fill(count, floor + 1)
print(count)

# for row in grid[:,480:560]:
#     print(str.join('', row))
