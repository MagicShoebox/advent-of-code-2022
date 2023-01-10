with open('input.txt') as f:
    snafus = [line.rstrip() for line in f]

def decimal(s):
    digits = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2
    }
    return sum(digits[d] * 5**i for i,d in enumerate(s[::-1]))

def snafu(d):
    digits = {
        2: '2',
        1: '1',
        0: '0',
        -1: '-',
        -2: '='
    }
    result = ''
    while d > 0:
        r = d % 5
        if r >= 3:
            r -= 5
        d -= r
        d //= 5
        result += digits[r]
    return result[::-1]

print(snafu(sum(decimal(snafu) for snafu in snafus)))
