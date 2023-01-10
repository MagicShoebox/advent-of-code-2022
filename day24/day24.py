import numpy as np
import heapq as hq

with open('input.txt') as f:
    valley = np.genfromtxt(f, dtype=str, delimiter=1, comments=None)[1:-1,1:-1]

size = valley.shape
blizz = [(ix, b) for ix, b in np.ndenumerate(valley) if b in {'>','v','<','^'}]
blizz_cache = {}

def blizzards(t):
    def generate(t):
        for ix, b in blizz:
            y,x = ix
            match b:
                case '>':
                    yield y, (x + t) % size[1]
                case 'v':
                    yield (y + t) % size[0], x
                case '<':
                    yield y, (x - t) % size[1]
                case '^':
                    yield (y - t) % size[0], x
    if t not in blizz_cache:
        blizz_cache[t] = set(generate(t))
    return blizz_cache[t]

def neighbors(state):
    ix, t = state
    bs = blizzards(t+1)
    if ix not in bs:
        yield ix, t+1
    y,x = ix
    # y <= size[0] - 1 to handle end
    if y <= size[0] - 1 and x > 0 and (ixp := (y,x-1)) not in bs:
        yield ixp, t+1
    if (y > 0 or ix==(0,0)) and (ixp := (y-1,x)) not in bs:
        yield ixp, t+1
    # y >= 0 to handle start
    if y >= 0 and x < size[1] - 1 and (ixp := (y,x+1)) not in bs:
        yield ixp, t+1
    if (y < size[0] - 1 or ix==(size[0]-1,size[1]-1)) and (ixp := (y+1,x)) not in bs:
        yield ixp, t+1

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def shortest_path(t, start, end):
    queue = [(0, (start, t))]
    visited = {(start, t): 0}
    while queue:
        _, v = hq.heappop(queue)
        if v[0] == end:
            current = v
            return visited[v]
        for n in neighbors(v):
            if n not in visited or visited[n] > visited[v] + 1:
                visited[n] = visited[v] + 1
                hq.heappush(queue, (visited[v] + 1 + distance(n[0], end), n))

start = (-1,0)
end = (size[0], size[1] - 1)
time = shortest_path(0, start, end)
print(time)
time += shortest_path(time, end, start)
time += shortest_path(time, start, end)
print(time)
