import numpy as np
import re
from itertools import takewhile

BSIZE = 50
BSTART = 0
BEND = BSIZE - 1

with open('input.txt') as f:
    lines = (line.rstrip() for line in f)
    grid_lines = list(takewhile(bool, lines))
    path = re.split(r'(\d+)', next(lines))[1:-1]

grid = np.full((len(grid_lines), max(len(line) for line in grid_lines)), ' ')
for i, line in enumerate(grid_lines):
    grid[i,:len(line)] = list(line)

part1_warp = {
    (0,1,2): (0,2,2),
    (0,1,3): (2,1,3),
    (0,2,0): (0,1,0),
    (0,2,1): (0,2,1),
    (0,2,3): (0,2,3),
    (1,1,0): (1,1,0),
    (1,1,2): (1,1,2),
    (2,0,2): (2,1,2),
    (2,0,3): (3,0,3),
    (2,1,0): (2,0,0),
    (2,1,1): (0,1,1),
    (3,0,0): (3,0,0),
    (3,0,1): (2,0,1),
    (3,0,2): (3,0,2)
}

part2_warp = {
    (0,1,2): (2,0,0),
    (0,1,3): (3,0,0),
    (0,2,0): (2,1,2),
    (0,2,1): (1,1,2),
    (0,2,3): (3,0,3),
    (1,1,0): (0,2,3),
    (1,1,2): (2,0,1),
    (2,0,2): (0,1,0),
    (2,0,3): (1,1,0),
    (2,1,0): (0,2,2),
    (2,1,1): (3,0,2),
    (3,0,0): (2,1,3),
    (3,0,1): (0,2,1),
    (3,0,2): (0,1,1)
}

def neighbor(warp,r,c,f):
    rb, ro = r // BSIZE, r % BSIZE
    cb, co = c // BSIZE, c % BSIZE
    edge = (rb, cb, f)
    match f:
        case 0 if co != BEND or edge not in warp:
            return r,c+1,f
        case 1 if ro != BEND or edge not in warp:
           return r+1,c,f
        case 2 if co != BSTART or edge not in warp:
            return r,c-1,f
        case 3 if ro != BSTART or edge not in warp:
            return r-1,c,f

    rw, cw, fw = warp[edge]
    r, c = rw * BSIZE, cw * BSIZE
    match fw:
        case 0:
            c += BSTART
        case 1:
            r += BSTART
        case 2:
            c += BEND
        case 3:
            r += BEND

    match fw, f:
        case (0,0) | (2,2):
            r += ro
        case (0,2) | (2,0):
            r += BEND - ro
        case (0,1) | (0,3) | (2,1) | (2,3):
            r += co
        case (1,1) | (3,3):
            c += co
        case (1,3) | (3,1):
            c += BEND - co
        case (1,0) | (1,2) | (3,0) | (3,2):
            c += ro
    
    f = fw
    return r,c,f

def walk_path(warp):
    r,c,f = 0, np.nonzero(grid[0] == '.')[0][0], 0
    for step in path:
        match step:
            case 'L':
                f = (f - 1) % 4
            case 'R':
                f = (f + 1) % 4
            case d:
                for _ in range(int(d)):
                    rp,cp,fp = neighbor(warp,r,c,f)
                    if grid[rp,cp] == '#':
                        break
                    r,c,f = rp,cp,fp
    return r,c,f

def final_password(pos):
    r,c,f = pos
    return 1000*(r+1) + 4*(c+1) + f

print(final_password(walk_path(part1_warp)))
print(final_password(walk_path(part2_warp)))
