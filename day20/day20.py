from dataclasses import dataclass

@dataclass
class Node:
    value: int
    pred: 'Node'
    succ: 'Node'

with open('input.txt') as f:
    lines = (line.rstrip() for line in f)
    nodes = [Node(int(line), None, None) for line in lines]

def order_nodes():
    nodes[-1].succ = nodes[0]
    nodes[0].pred = nodes[-1]
    for x,y in zip(nodes, nodes[1:]):
        x.succ = y
        y.pred = x

def advance(target, i):
    if i <= len(nodes) // 2:
        for _ in range(i):
            target = target.succ
    else:
        for _ in range(len(nodes) - i):
            target = target.pred
    return target

def rearrange(n):
    zero_node = None
    for _ in range(n):
        for node in nodes:
            steps = node.value % (len(nodes) - 1)
            if steps == 0:
                if node.value == 0:
                    zero_node = node
                continue
            target = advance(node, steps)
            
            node.pred.succ = node.succ
            node.succ.pred = node.pred

            target.succ.pred = node
            node.succ = target.succ
            target.succ = node
            node.pred = target
    return zero_node

def coordinates(zero_node):
    return sum(advance(zero_node, i).value for i in [1000,2000,3000])

order_nodes()
print(coordinates(rearrange(1)))
order_nodes()
for node in nodes:
    node.value *= 811589153
print(coordinates(rearrange(10)))
