import numpy as np

with open('input.txt') as f:
    moves = list(next(f).rstrip())

shapes = [
    np.array([
     [1, 1, 1, 1]
    ]),
    np.array([
     [0, 1, 0],
     [1, 1, 1],
     [0, 1, 0]
    ]),
    np.array([
     [0, 0, 1],
     [0, 0, 1],
     [1, 1, 1]
    ]),
    np.array([
     [1],
     [1],
     [1],
     [1]
    ]),
    np.array([
     [1, 1],
     [1, 1]
    ])
]

FLOOR = 5000
WIDTH = 7

grid = np.zeros([FLOOR, WIDTH], dtype=int)
grid[FLOOR - 1] = [1]*WIDTH
max_row = FLOOR - 1

def window(shape, pos):
    h,w = shape.shape
    x,y = pos
    return slice(y+1-h, y+1), slice(x, x+w)

def collision(shape, pos):
    return np.any(grid[window(shape, pos)] + shape == 2)

def drop_rock(max_row, rock, m):
    shape = shapes[rock % len(shapes)]
    pos = (2, max_row - 4)
    i = m

    while True:
        match moves[i % len(moves)]:
            case '<':
                next_pos = (pos[0]-1, pos[1])
            case '>':
                next_pos = (pos[0]+1, pos[1])
        i += 1

        if next_pos[0] >= 0 and next_pos[0] + shape.shape[1] <= WIDTH and not collision(shape, next_pos):
            pos = next_pos

        next_pos = (pos[0], pos[1]+1)

        if collision(shape, next_pos):
            grid[window(shape, pos)] += shape
            return min(max_row, pos[1] - shape.shape[0] + 1), i - m

        pos = next_pos

def visualize(max_row):
    print()
    for row in grid[max_row:]:
        print(''.join('#' if x else '.' for x in row))

rock = 0
move = 0
period_start = None
while rock < 2022:
    max_row, m = drop_rock(max_row, rock, move)
    rock += 1
    move += m
    if period_start is None and np.all(grid[max_row] == 1):
        period_start = rock, max_row, move

print((FLOOR - 1) - max_row)

while move != period_start[2]:
    max_row, m = drop_rock(max_row, rock, move)
    rock += 1
    move = (move + m) % len(moves)

period_end = rock
remaining_rocks = 10**12 - rock
rocks_per_period = rock - period_start[0]
periods = remaining_rocks // rocks_per_period
rows_per_period = period_start[1] - max_row
pseudo_rows = periods * rows_per_period

while rock - period_end < remaining_rocks % rocks_per_period:
    max_row, m = drop_rock(max_row, rock, move)
    rock += 1
    move += m

print((FLOOR - 1) - max_row + pseudo_rows)
