from aoc import read_file, timer
from collections import defaultdict, deque

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

def send_input(game, input):
    game.input.extend(input)

def read_output(game):
    if len(game.output):
        return game.output.popleft()
    return None

def run_game(game):
    if game.prog[game.ip] != 99:
        op, modes = split_instruction(game.prog[game.ip])
        values, offset = get_values(game.prog, game.ip, op, modes, game)
        
        if op == "01": # Addition
            game.prog[game.prog[game.ip+3] + offset] = values[0] + values[1]
            game.ip += 4
    
        if op == "02": # Multiplication
            game.prog[game.prog[game.ip+3] + offset] = values[0] * values[1]
            game.ip += 4
        
        if op == "03": # Read and Store input
            if len(game.input):
                game.prog[game.prog[game.ip+1] + offset] = game.input.popleft()
            else:
                game.prog[game.prog[game.ip+1] + offset] = -1
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
    else:
        game.halt = True

def create_program(input):
    prog = defaultdict(int)
    
    for i in range(len(input)):
        prog[i] = int(input[i])
    
    return prog

def read_prompt(game, fin = False):
    output = None
    
    while output != ord("?"):
        while not (output := read_output(game)):
            if game.halt:
                return
            run_game(game)
        
        print(chr(output), end = "")


@timer
def solve():
    input = read_file("25")[0].split(",")
    prog = create_program(input)
    game = Game(prog)

    instructions = []
    instructions.append("south\n")
    instructions.append("take mouse\n")
    instructions.append("north\n")
    instructions.append("west\n")
    instructions.append("north\n")
    instructions.append("north\n")
    instructions.append("")
    instructions.append("west\n")
    instructions.append("take semiconductor\n")
    instructions.append("east\n")
    instructions.append("")
    instructions.append("south\n")
    instructions.append("west\n")
    instructions.append("south\n")
    instructions.append("take hypercube\n")
    instructions.append("north\n")
    instructions.append("east\n")
    instructions.append("south\n")    
    instructions.append("west\n")
    instructions.append("take antenna\n")
    instructions.append("west\n")
    instructions.append("south\n")
    instructions.append("south\n")
    instructions.append("south\n")
    
    for instruction in instructions:
        read_prompt(game)
        send_input(game, [ord(c) for c in instruction])
        print(f"\n\n{instruction}")
    
    read_prompt(game, fin = True)

solve()