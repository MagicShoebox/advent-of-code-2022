from itertools import takewhile
from functools import cmp_to_key

with open('input.txt') as f:
    lines = (line.rstrip() for line in f)
    blocks = [[line, *takewhile(bool, lines)] for line in lines]
    pairs = [(block[0], block[1]) for block in blocks]

def parse(line):
    def lex(pos):
        if pos >= len(line):
            return pos, None
        match line[pos]:
            case '[' | ']' | ',':
                pos += 1
                return pos, line[pos-1]
            case _:
                start = pos
                while '0' <= line[pos] <= '9':
                    pos += 1
                return pos, int(line[start:pos])
    def consumeList(pos):
        buffer = []
        pos, token = lex(pos)
        while token != ']':
            match token:
                case '[':
                    pos, val = consumeList(pos)
                    buffer.append(val)
                case int(x):
                    buffer.append(x)
            pos, token = lex(pos)
        return pos, buffer
    pos, token = lex(0)
    return consumeList(pos)[1]

def compare(x, y):
    match (x,y):
        case (int(a), int(b)):
            if a == b:
                return None
            return a < b
        case (int(a), list(b)):
            return compare([a], b)
        case (list(a), int(b)):
            return compare(a, [b])
        case (list(a), list(b)):
            i = 0
            while i < len(a) and i < len(b):
                r = compare(a[i], b[i])
                if r is not None:
                    return r
                i += 1
            if len(a) == len(b):
                return None
            return len(a) < len(b)

packets = [(parse(x), parse(y)) for x,y in pairs]
print(sum(i+1 for i, p in enumerate(packets) if compare(p[0], p[1])))

dividers = [[[2]],[[6]]]
packets = dividers + [packet for pair in packets for packet in pair]

for i in range(1,len(packets)):
    moving = False
    for j in range(i):
        if moving or compare(packets[i], packets[j]):
            moving = True
            packets[i], packets[j] = packets[j], packets[i]

print((packets.index(dividers[0])+1) * (packets.index(dividers[1])+1))
