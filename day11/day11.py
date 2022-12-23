import re
from dataclasses import dataclass
from itertools import takewhile, islice
from typing import Callable
from operator import attrgetter
from math import prod

@dataclass
class Monkey:
    id: int
    inspected: int
    items: list[int]
    operation: Callable[[int], int]
    test: Callable[[int], bool]
    modulus: int
    true_dest: 'Monkey'
    false_dest: 'Monkey'

def monkey(block) -> Monkey:
    def op(expression) -> Callable[[int],int]:
        match expression.split():
            case ['old', '*', 'old']:
                return lambda old: old * old
            case ['old', '*', x]:
                return lambda old: old * int(x)
            case ['old', '+', x]:
                return lambda old: old + int(x)
            case _:
                raise ValueError('Unrecognized')
    def test(expression) -> Callable[[int], bool]:
        match expression.split():
            case ['divisible', 'by', b]:
                return lambda a: a % int(b) == 0
            case _:
                raise ValueError('Unrecognized')

    return Monkey(
        id=int(re.match(r'Monkey (\d):', block[0]).group(1)),
        inspected=0,
        items=[int(x) for x in block[1].split(':')[1].split(',')],
        operation=op(block[2].split('=')[1]),
        test=test(block[3].split(':')[1]),
        modulus=int(block[3].split('by')[1]),
        true_dest=int(re.match(r'\s*throw to monkey (\d)', block[4].split(':')[1]).group(1)),
        false_dest=int(re.match(r'\s*throw to monkey (\d)', block[5].split(':')[1]).group(1))
    )

with open('input.txt') as f:
    lines = (line.rstrip() for line in f)
    blocks = [[line, *takewhile(bool, lines)] for line in lines]
    monkeys1 = [monkey(block) for block in blocks]
    monkeys2 = [monkey(block) for block in blocks]

M = prod(m.modulus for m in monkeys1)

def simulation(monkeys, divisor, rounds):
    for _ in range(rounds):
        for monkey in monkeys:
            while monkey.items:
                monkey.inspected += 1
                item = monkey.items.pop()
                item = monkey.operation(item) % M
                item //= divisor
                if monkey.test(item):
                    monkeys[monkey.true_dest].items.append(item)
                else:
                    monkeys[monkey.false_dest].items.append(item)

    return (m.inspected for m in sorted(monkeys, key=attrgetter('inspected'), reverse=True))

print(prod(islice(simulation(monkeys1,3,20),0,2)))
print(prod(islice(simulation(monkeys2,1,10000),0,2)))
