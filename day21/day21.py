import re
from dataclasses import dataclass

@dataclass
class Node:
    op: str
    left: str
    right: str
    dependent: bool

@dataclass
class Input:
    pass

def parse_line(line):
    int_pattern = re.compile(r'-?\d+')
    match line.split(': '):
        case [monkey, x] if int_pattern.match(x):
            return monkey, int(x)
        case [monkey, node]:
            left, op, right = node.split()
            return monkey, Node(op, left, right, False)

with open('input.txt') as f:
    lines = (line.rstrip() for line in f)
    tuples = (parse_line(line) for line in lines)
    monkeys = {k:v for k,v in tuples}

def do_op(op, left, right):
    match op:
        case '+':
            return left + right
        case '*':
            return left * right
        case '-':
            return left - right
        case '/':
            return left // right

def simplify(root):
    stack = [root]
    while stack:
        node = monkeys[stack[-1]]
        match monkeys[node.left], monkeys[node.right]:
            case int(x), int(y):
                monkeys[stack[-1]] = do_op(node.op, x, y)
                stack.pop()
            case Node() as left, _ if not left.dependent:
                stack.append(node.left)
            case _, Node() as right if not right.dependent:
                stack.append(node.right)
            case _:
                node.dependent = True
                stack.pop()
    return monkeys[root]

def solve_for_input(root):
    match monkeys[root.left], monkeys[root.right]:
        case (n, int(v)) | (int(v), n):
            node, value = n, v
    while isinstance(node, Node):
        node.dependent = False
        match node.op, monkeys[node.left], monkeys[node.right]:
            case ('+', _, int(v)) | ('+', int(v), _):
                value -= v
            case ('*', _, int(v)) | ('*', int(v), _):
                value //= v
            case ('-', _, int(v)):
                value += v
            case ('-', int(v), _):
                value = v - value
            case ('/', _, int(v)):
                value *= v
            case ('/', int(v), _):
                value = v // value
        match monkeys[node.left], monkeys[node.right]:
            case (n, int()) | (int(), n):
                node = n
    return value

part1_humn = monkeys['humn']
monkeys['humn'] = Input()
part2 = solve_for_input(simplify('root'))
monkeys['humn'] = part1_humn
print(simplify('root'))
print(part2)
