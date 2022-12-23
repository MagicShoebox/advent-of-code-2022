import numpy as np
import heapq as hq

with open('input.txt') as f:
    hills = np.genfromtxt(f, dtype=str, delimiter=1)

def get_pos(haystack, needle):
    loc = np.where(haystack == needle)
    return loc[0][0], loc[1][0]

end = get_pos(hills, 'E')

def distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def neighbors(p):
    x,y = p
    return [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]

def inside(p):
    return 0 < p[0] < hills.shape[0] and 0 < p[1] < hills.shape[1]

def height(p):
    match hills[p]:
        case 'S':
            return ord('a')
        case 'E':
            return ord('z')
        case x:
            return ord(x)

def climbable(p, n):
    return height(n) <= height(p) + 1

def path_length(start):
    queue = [(0,start)]
    visited = {start: 0}
    path = {start: None}
    while queue:
        _, p = hq.heappop(queue)
        if p == end:
            break
        for n in (n for n in neighbors(p) if inside(n) and climbable(p, n)):
            if n not in visited or visited[p] + 1 < visited[n]:
                visited[n] = visited[p] + 1
                path[n] = p
                hq.heappush(queue, (visited[p] + distance(n, end), n))

    if end not in path:
        return None
    else:
        length = 0
        current = end
        while path[current] is not None:
            length += 1
            current = path[current]

        return length

print(path_length(get_pos(hills, 'S')))
starts = (length for start in zip(*np.where(hills == 'a')) if (length:=path_length(start)) is not None)
print(min(starts))
