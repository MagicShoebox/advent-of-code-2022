with open('input.txt') as f:
    rucksacks = [line.rstrip() for line in f]

def common(rucksack):
    midpoint = len(rucksack) // 2
    return (set(rucksack[:midpoint]) & set(rucksack[midpoint:])).pop()

def priority(item):
    p = ord(item)
    if p > ord('Z'):
        return p - ord('a') + 1
    return p - ord('A') + 27

print(sum(priority(common(rucksack)) for rucksack in rucksacks))

def badge(rucksacks):
    return set.intersection(*map(set, rucksacks)).pop()

groups = (rucksacks[x*3:x*3+3] for x in range(0,len(rucksacks) // 3))
print(sum(priority(badge(group)) for group in groups))
