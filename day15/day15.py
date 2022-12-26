import re
from itertools import chain

with open('input.txt') as f:
    pattern = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')
    lines = (line.rstrip() for line in f)
    positions = [[int(x) for x in pattern.match(line).group(1,2,3,4)] for line in lines]

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

beacons = set(tuple(p[2:]) for p in positions)
sensors = [(p[:2], distance(p[:2], p[2:])) for p in positions]

def too_close(sensor, point):
    return distance(sensor[0], point) <= sensor[1]

def no_beacon(p):
    return p not in beacons and any(too_close(s, p) for s in sensors)

xmin = min(s[0][0]-s[1] for s in sensors) - 1
xmax = max(s[0][0]+s[1] for s in sensors) + 1
print(sum(1 for x in range(xmin, xmax + 1) if no_beacon((x,2_000_000))))

def circumference(sensor):
    x,y = sensor[0]
    d = sensor[1] + 1
    return chain(
        ((x+d-i, y+i) for i in range(d+1)),
        ((x+d-i, y-i) for i in range(1,d+1)),
        ((x-d+i, y-i) for i in range(d+1)),
        ((x-d+i, y+i) for i in range(1,d))
    )

distress = (
    p[0]*4_000_000+p[1]
    for s in sensors
    for p in circumference(s)
    if 0 <= p[0] <= 4_000_000
    and 0 <= p[1] <= 4_000_000
    and p not in beacons
    and not no_beacon(p))
print(next(distress))
