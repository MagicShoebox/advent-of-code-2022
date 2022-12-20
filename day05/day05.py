import re
from itertools import takewhile

NUM_STACKS = 9

with open('input.txt') as f:
    lines = (line.rstrip() for line in f)
    stack_lines = [[line[1+i*4:2+i*4].strip() for i in range(NUM_STACKS)] for line in takewhile(bool, lines)][:-1]
    instruction_pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')
    instructions = [[int(x) for x in instruction_pattern.match(line).group(1,2,3)] for line in lines]

start_stacks = [list(takewhile(bool, stack)) for stack in zip(*stack_lines[::-1])]

def run_instructions(stacks, reverse):
    for instruction in instructions:
        n, source, destination = instruction
        s,d = source - 1, destination - 1
        if reverse:
            stacks[d].extend(stacks[s][:-n-1:-1])
        else:
            stacks[d].extend(stacks[s][-n:])
        stacks[s] = stacks[s][:-n]
    return stacks

print(str.join('', (str(s[-1]) for s in run_instructions([s.copy() for s in start_stacks], True))))
print(str.join('', (str(s[-1]) for s in run_instructions([s.copy() for s in start_stacks], False))))
