with open('input.txt') as f:
    motions = [(x[0], int(x[1])) for x in (line.split() for line in f)]

def unit(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0

def tail_positions(rope):
    for dir,dist in motions:
        for _ in range(dist):
            match dir:
                case 'L':
                    rope[0][0] -= 1
                case 'R':
                    rope[0][0] += 1
                case 'U':
                    rope[0][1] -= 1
                case 'D':
                    rope[0][1] += 1
            for head, tail in zip(rope, rope[1:]):
                if abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1:
                    tail[0] += unit(head[0] - tail[0])
                    tail[1] += unit(head[1] - tail[1])
            yield tuple(rope[-1])

print(len(set(tail_positions([[0,0] for _ in range(2)]))))
print(len(set(tail_positions([[0,0] for _ in range(10)]))))
