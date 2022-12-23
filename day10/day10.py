with open('input.txt') as f:
    instructions = [line.rstrip() for line in f]

ip = -1
cycle = 0
register = 1
instruction = None
crt = -1
signal_strengths = []
screen_width = 40
screen = [['.' for _ in range(screen_width)] for _ in range(6)]

while ip < len(instructions)-1 or instruction is not None:
    cycle += 1
    if cycle % 40 == 20:
        signal_strengths.append(cycle * register)
    crt += 1
    if abs(register - crt % screen_width) <= 1:
        screen[crt // screen_width][crt % screen_width] = '#'
    match instruction:
        case None:
            ip += 1
            match instructions[ip].split():
                case ['noop']:
                    pass
                case ['addx', v]:
                    instruction = (cycle+1, register + int(v))
        case (done, new_reg):
            if cycle == done:
                register = new_reg
                instruction = None

print(sum(signal_strengths))
for row in screen:
    print(str.join('', row))
