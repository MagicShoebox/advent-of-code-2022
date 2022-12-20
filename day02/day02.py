from operator import itemgetter

with open('input.txt') as f:
    rounds = [line.rstrip() for line in f]

ROCK = 0
PAPER = 1
SCISSORS = 2
LOSS = 0
DRAW = 1
WIN = 2
outcomes = [[DRAW, LOSS, WIN], [WIN, DRAW, LOSS], [LOSS, WIN, DRAW]]
scores = {ROCK: 1, PAPER: 2, SCISSORS: 3}

def score(p1, p2):
    return scores[p2] + 3 - 3 * (outcomes[p1][p2] - 1)

code = {'A': ROCK, 'B': PAPER, 'C': SCISSORS, 'X': ROCK, 'Y': PAPER, 'Z': SCISSORS}
print(sum(score(code[r[0]], code[r[2]]) for r in rounds))

moves = [[idx for idx,_ in sorted(enumerate(p1), key=itemgetter(1), reverse=True)] for p1 in outcomes]
results = {'X': LOSS, 'Y': DRAW, 'Z': WIN}
print(sum(score(code[r[0]], moves[code[r[0]]][results[r[2]]]) for r in rounds))
