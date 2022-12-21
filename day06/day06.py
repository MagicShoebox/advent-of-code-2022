from itertools import dropwhile

with open('input.txt') as f:
    line = next(f).rstrip()

def stripe(iter, n):
    return zip(*(iter[i:] for i in range(n)))

def duplicates(x):
    _, quad = x
    return len(set(quad))!=len(quad)

start_of_packet = next(dropwhile(duplicates, enumerate(stripe(line,4))))
print(start_of_packet[0]+4)
start_of_message = next(dropwhile(duplicates, enumerate(stripe(line,14))))
print(start_of_message[0]+14)
