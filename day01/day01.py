from itertools import takewhile

with open('input.txt') as f:
    lines = (line.rstrip() for line in f)
    elves = [[line, *takewhile(bool, lines)] for line in lines]

calories = [sum(map(int, elf)) for elf in elves]
print(max(calories))
print(sum(sorted(calories, reverse=True)[:3]))
