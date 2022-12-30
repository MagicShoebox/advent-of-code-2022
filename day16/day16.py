import re
import heapq as hq
from itertools import combinations

START = 'AA'

with open('input.txt') as f:
    pattern = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]+)')
    records = (pattern.match(line.rstrip()).group(1,2,3) for line in f)
    network = {valve: (int(rate), tunnels.split(', ')) for valve, rate, tunnels in records}

def shortest_distance(start, end):
    queue = [(0,start)]
    visited = {start: 0}
    while queue:
        _, v = hq.heappop(queue)
        if v == end:
            return visited[v]
        for n in network[v][1]:
            if n not in visited or visited[n] > visited[v] + 1:
                visited[n] = visited[v] + 1
                hq.heappush(queue, (visited[v] + 1, n))

all_nodes = {v:r for v,(r,_) in network.items() if r > 0}
edges = {}
for u,v in combinations(all_nodes.keys() | {START}, 2):
    d = shortest_distance(u, v)
    edges[(u,v)] = d
    edges[(v,u)] = d

def best_score(nodes, max_time):
    def scores(score, time, flow, visited, current):
        if time == max_time or nodes == visited:
            yield score
            return
        for n in nodes - visited:
            t = min(max_time - time, edges[(current, n)] + 1)
            yield from scores(score + flow * t, time + t, flow + all_nodes[n], visited | {n}, n)

    return max(scores(0,0,0,set(),START))

print(best_score(all_nodes.keys(), 30))

def score_split(split):
    nodes1 = set(split)
    nodes2 = all_nodes.keys() - nodes1
    return best_score(nodes1, 26) + best_score(nodes2, 26)

def splits():
    for i in range(1, 1 + len(all_nodes) // 2):
        yield from combinations(all_nodes, i)

print(max(score_split(split) for split in splits()))
