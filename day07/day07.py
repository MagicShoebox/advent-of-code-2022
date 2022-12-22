from dataclasses import dataclass

@dataclass
class File:
    name: str
    size: int

@dataclass
class Directory:
    name: str
    size: int
    files: dict[str, File]
    dirs: dict[str, 'Directory']

with open('input.txt') as f:
    lines = [line.rstrip() for line in f]

workdir = [Directory(name='/', size=0, files={}, dirs={})]

for line in lines:
    match line.split():
        case ['$', 'cd', '/']:
            workdir = workdir[:1]
        case ['$', 'cd', '..']:
            workdir.pop()
        case ['$', 'cd', dir]:
            workdir.append(workdir[-1].dirs[dir])
        case ['$', 'ls']:
            pass
        case ['dir', name]:
            workdir[-1].dirs[name]=Directory(name=name, size=0, files={}, dirs={})
        case [size, name]:
            workdir[-1].files[name]=File(name=name, size=int(size))

stack = [(0, workdir[0])]
workdir = []
while stack:
    depth, current = stack.pop()
    workdir = workdir[:depth]
    workdir.append(current)
    size = sum(file.size for file in current.files.values())
    for dir in workdir:
        dir.size += size
    stack.extend((depth+1, dir) for dir in current.dirs.values())

total = 0
minimum = 30000000 - (70000000 - workdir[0].size)
to_delete = workdir[0]
stack = [workdir[0]]
while stack:
    current = stack.pop()
    stack.extend(current.dirs.values())
    if current.size <= 100000:
        total += current.size
    if minimum <= current.size < to_delete.size:
        to_delete = current

print(total)
print(to_delete.size)
