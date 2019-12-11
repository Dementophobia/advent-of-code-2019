from aoc import read_file, timer
from collections import defaultdict

class Painter:
    def __init__(self, prog):
        self.prog     = prog
        self.ip       = 0
        self.output   = 0
        self.rel_base = 0
        self.halt     = False

def split_instruction(instruction):
    instruction = f"{instruction:05}"
    return instruction[3:], instruction[0:3]

def get_values(input, pos, op, modes, painter):
    mode_a, mode_b, mode_c = modes
    values = []
    offset = 0
    
    if op in ["01", "02", "04", "05", "06", "07", "08", "09"]:
        if mode_c == "0":
            values.append(input[input[pos+1]])
        elif mode_c == "1":
            values.append(input[pos+1])
        elif mode_c == "2":
            values.append(input[input[pos+1]+painter.rel_base])

        if op in ["01", "02", "05", "06", "07", "08"]:
            if mode_b == "0":
                values.append(input[input[pos+2]])
            elif mode_b == "1":
                values.append(input[pos+2])
            elif mode_b == "2":
                values.append(input[input[pos+2]+painter.rel_base])

            if op in []:
                if mode_a == "0":
                    values.append(input[input[pos+3]])
                elif mode_a == "1":
                    values.append(input[pos+3])
                elif mode_a == "2":
                    values.append(input[input[pos+3]+painter.rel_base])

    if op in ["01", "02", "07", "08"]:
        if mode_a == "2":
            offset = painter.rel_base
    
    if op in ["03"]:
        if mode_c == "2":
            offset = painter.rel_base

    return values, offset
  
def run_booster(input, painter):
    while painter.prog[painter.ip] != 99:
        op, modes = split_instruction(painter.prog[painter.ip])
        values, offset = get_values(painter.prog, painter.ip, op, modes, painter)
        
        if op == "01": # Addition
            painter.prog[painter.prog[painter.ip+3] + offset] = values[0] + values[1]
            painter.ip += 4
    
        if op == "02": # Multiplication
            painter.prog[painter.prog[painter.ip+3] + offset] = values[0] * values[1]
            painter.ip += 4
        
        if op == "03": # Read and Store input
            painter.prog[painter.prog[painter.ip+1] + offset] = input
            painter.ip += 2

        if op == "04": # Print Output
            painter.output = values[0]
            #print(painter.output)
            painter.ip += 2
            return painter

        if op == "05": # Jump-if-True
            if values[0]:
                painter.ip = values[1]
            else:
                painter.ip += 3

        if op == "06": # Jump-if-False
            if not values[0]:
                painter.ip = values[1]
            else:
                painter.ip += 3
        
        if op == "07": # Less than
            if values[0] < values[1]:
                painter.prog[painter.prog[painter.ip+3] + offset] = 1
            else:
                painter.prog[painter.prog[painter.ip+3] + offset] = 0
            painter.ip += 4

        if op == "08": # Equals
            if values[0] == values[1]:
                painter.prog[painter.prog[painter.ip+3] + offset] = 1
            else:
                painter.prog[painter.prog[painter.ip+3] + offset] = 0
            painter.ip += 4

        if op == "09": # Adjust Relative Base
            painter.rel_base += values[0]
            painter.ip += 2
    
    painter.halt = True
    return painter

def create_program(input):
    prog = defaultdict(int)
    
    for i in range(len(input)):
        prog[i] = int(input[i])
    
    return prog

def turn_and_move(pos, dir, turn):
    if turn == 0:
        dir = (dir - 1) % 4
    else:
        dir = (dir + 1) % 4
        
    if dir == 0: # up
        pos = (pos[0], pos[1] + 1)
    elif dir == 1: # right
        pos = (pos[0]+1, pos[1])
    elif dir == 2: # down
        pos = (pos[0], pos[1] - 1)
    elif dir == 3: # left
        pos = (pos[0] - 1, pos[1])
    
    return pos, dir

@timer
def solve():
    input = read_file("11")[0].split(",")
    prog = create_program(input)
    
    panel = defaultdict(int)
    painted = defaultdict(int)
    painter = Painter(prog)
    
    dir = 0
    pos = (0, 0)

    while not painter.halt:
        painter = run_booster(panel[pos], painter)
        color = painter.output
        painter = run_booster(panel[pos], painter)
        turn = painter.output
        
        painted[pos] = 1
        panel[pos] = color
        
        pos, dir = turn_and_move(pos, dir, turn)

    return len(painted)

result = solve()
print(f"Solution: {result}")