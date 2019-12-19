from aoc import read_file, timer
from collections import defaultdict, deque
from copy import copy

class Game:
    def __init__(self, prog):
        self.prog     = prog
        self.ip       = 0
        self.input    = deque()
        self.output   = deque()
        self.rel_base = 0
        self.halt     = False

def split_instruction(instruction):
    instruction = f"{instruction:05}"
    return instruction[3:], instruction[0:3]

def get_values(input, pos, op, modes, game):
    mode_a, mode_b, mode_c = modes
    values = []
    offset = 0
    
    if op in ["01", "02", "04", "05", "06", "07", "08", "09"]:
        if mode_c == "0":
            values.append(input[input[pos+1]])
        elif mode_c == "1":
            values.append(input[pos+1])
        elif mode_c == "2":
            values.append(input[input[pos+1]+game.rel_base])

        if op in ["01", "02", "05", "06", "07", "08"]:
            if mode_b == "0":
                values.append(input[input[pos+2]])
            elif mode_b == "1":
                values.append(input[pos+2])
            elif mode_b == "2":
                values.append(input[input[pos+2]+game.rel_base])

            if op in []:
                if mode_a == "0":
                    values.append(input[input[pos+3]])
                elif mode_a == "1":
                    values.append(input[pos+3])
                elif mode_a == "2":
                    values.append(input[input[pos+3]+game.rel_base])

    if op in ["01", "02", "07", "08"]:
        if mode_a == "2":
            offset = game.rel_base
    
    if op in ["03"]:
        if mode_c == "2":
            offset = game.rel_base

    return values, offset

def read_output(game):
    if len(game.output):
        return game.output.popleft()
    return None

def run_game(game, input = []):
    if len(input):
        game.input.extend(input)
    
    while game.prog[game.ip] != 99:
        op, modes = split_instruction(game.prog[game.ip])
        values, offset = get_values(game.prog, game.ip, op, modes, game)
        
        if op == "01": # Addition
            game.prog[game.prog[game.ip+3] + offset] = values[0] + values[1]
            game.ip += 4
    
        if op == "02": # Multiplication
            game.prog[game.prog[game.ip+3] + offset] = values[0] * values[1]
            game.ip += 4
        
        if op == "03": # Read and Store input
            game.prog[game.prog[game.ip+1] + offset] = game.input.popleft()
            game.ip += 2

        if op == "04": # Print Output
            game.output.append(values[0])
            game.ip += 2
            return

        if op == "05": # Jump-if-True
            if values[0]:
                game.ip = values[1]
            else:
                game.ip += 3

        if op == "06": # Jump-if-False
            if not values[0]:
                game.ip = values[1]
            else:
                game.ip += 3
        
        if op == "07": # Less than
            if values[0] < values[1]:
                game.prog[game.prog[game.ip+3] + offset] = 1
            else:
                game.prog[game.prog[game.ip+3] + offset] = 0
            game.ip += 4

        if op == "08": # Equals
            if values[0] == values[1]:
                game.prog[game.prog[game.ip+3] + offset] = 1
            else:
                game.prog[game.prog[game.ip+3] + offset] = 0
            game.ip += 4

        if op == "09": # Adjust Relative Base
            game.rel_base += values[0]
            game.ip += 2
    
    game.halt = True

def create_program(input):
    prog = defaultdict(int)
    
    for i in range(len(input)):
        prog[i] = int(input[i])
    
    return prog

def try_y(prog, y, box_size = 100):
    output = 0
    x = y
    
    while output == 0:
        x += 1
        game = Game(copy(prog))
        run_game(game, [x, y])
        output = read_output(game)
    
    x1 = x
    
    while output == 1:
        x += 1
        game = Game(copy(prog))
        run_game(game, [x, y])
        output = read_output(game)

    x2 = x - 1
    
    if x2 - x1 + 1 < box_size:
        return -1, None
    
    game = Game(copy(prog))
    run_game(game, [x2-(box_size-1), y+box_size-1])
    
    if read_output(game) == 1:
        game = Game(copy(prog))
        run_game(game, [x2-(box_size-1), y+box_size])
        if read_output(game) == 0:
            return 0, (x2-(box_size-1), y)
        return 1, None
    return -1, None

@timer
def solve():
    input  = read_file("19")[0].split(",")
    prog   = create_program(input)
    game   = Game(prog)

    mini, maxi = 50, 1000
    check = 1
    
    while check:
        middle = (maxi + mini) // 2
        check, corner = try_y(prog, middle)
        if check == -1:
            mini = middle
        elif check == 1:
            maxi = middle
    
    while not check:
        middle -= 1
        check, corner = try_y(prog, middle)
        if not check:
            real_corner = corner
    
    return real_corner[0] * 10000 + real_corner[1]

result = solve()
print(f"Solution: {result}")