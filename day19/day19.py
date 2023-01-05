import re
from dataclasses import dataclass
import numpy as np
from numpy.typing import ArrayLike
from math import prod

NUM_TYPES = 4

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODES = 3

ACTIVE_BRANCHES = 50

@dataclass
class Blueprint:
    id: int
    costs: ArrayLike

    def from_matches(matches):
        ms = list(matches)
        id = int(ms[0][0])
        costs = np.array([
            [int(ms[1][0]), 0, 0, 0],
            [int(ms[2][0]), 0, 0, 0],
            [int(ms[3][0]), int(ms[3][1]), 0, 0],
            [int(ms[4][0]), 0, int(ms[4][1]), 0],
        ])
        return Blueprint(id, costs)

@dataclass
class State:
    resources: ArrayLike
    robots: ArrayLike

with open('input.txt') as f:
    pattern_strs = [
          r'Blueprint (\d+)',
          r'Each ore robot costs (\d+) ore',
          r'Each clay robot costs (\d+) ore',
          r'Each obsidian robot costs (\d+) ore and (\d+) clay',
          r'Each geode robot costs (\d+) ore and (\d+) obsidian'
    ]
    patterns = [re.compile(s) for s in pattern_strs]
    lines = (line.rstrip() for line in f)
    records = (zip(patterns, re.split(': |\. ', line)) for line in lines)
    matches = ((p.match(s).groups() for p,s in r) for r in records)
    blueprints = [Blueprint.from_matches(m) for m in matches]

# Wrote this when I thought you could build multiple robots at once
# Keeping the code in case it's useful elsewhere
def unused_multibuild_branches(blueprint, state):
    stack = [(state.resources, [])]
    while stack:
        resources, building = stack.pop()
        if len(building) == NUM_TYPES:
            yield resources, building
        else:
            costs = blueprint.costs[len(building)]
            most = np.min(resources[costs != 0] // costs[costs != 0])
            stack.extend((resources - i * costs, building + [i]) for i in range(1+most))

def branches(blueprint, state):
    yield state.resources[:], [0]*NUM_TYPES
    for i in range(NUM_TYPES):
        if np.all(state.resources >= blueprint.costs[i]):
            yield state.resources - blueprint.costs[i], np.identity(NUM_TYPES, dtype=int)[i]

def gte(state, other):
    gt, lt = False, False
    for i in range(NUM_TYPES):
        x = state.resources[i] - other.resources[i]
        y = state.robots[i] - other.robots[i]
        gt |= x > 0 or y > 0
        lt |= x < 0 or y < 0
        if lt and gt:
            return None
    return not lt

def prune(blueprint, layer, max_branches):
    active = []
    for state in layer:
        i = 0
        while i < len(active) and (compare := gte(state, active[i])) is None:
            i += 1
        if i == len(active):
            active.append(state)
        elif compare:
            active[i] = state

    def total_resources(state):
        est = (state.robots.reshape(NUM_TYPES, 1) * blueprint.costs).sum(0)
        est += state.resources
        return tuple(est[::-1])
    return sorted(active, key=total_resources, reverse=True)[:max_branches]

def scores(blueprint, max_time):
    initial = State(np.zeros(NUM_TYPES, dtype=int), np.zeros(NUM_TYPES, dtype=int))
    initial.robots[ORE] = 1
    time = 0
    layer = [initial]
    next_layer = []
    while time < max_time:
        active = prune(blueprint, layer, ACTIVE_BRANCHES)
        next_layer.extend(
            State(
                resources + state.robots,
                state.robots + building
            )
            for state in active
            for resources, building in branches(blueprint, state)
        )
        time += 1
        layer.clear()
        layer, next_layer = next_layer, layer
    yield from (s.resources[GEODES] for s in layer)

print(sum(b.id * max(scores(b, 24)) for b in blueprints))
print(prod(max(scores(b, 32)) for b in blueprints[:3]))
