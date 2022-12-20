with open('input.txt') as f:
    lines = (line.rstrip() for line in f)
    pairs = (line.split(',') for line in lines)
    ranges = [[[int(r) for r in elf.split('-')] for elf in pair] for pair in pairs]

for i in range(len(ranges)):
    x,y = ranges[i]
    if x[0] > y[0] or (x[0] == y[0] and x[1] <= y[1]):
        ranges[i] = [y,x]

def fully_overlaps(pair):
    x,y = pair
    return y[0] >= x[0] and y[1] <= x[1]

print(sum(1 for r in ranges if fully_overlaps(r)))

def overlaps(pair):
    x,y = pair
    return x[1] >= y[0]

print(sum(1 for r in ranges if overlaps(r)))
