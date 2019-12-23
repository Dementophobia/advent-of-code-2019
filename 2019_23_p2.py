from aoc import read_file, timer
from collections import defaultdict, deque

class Game:
    def __init__(self, prog):
        self.prog       = prog
        self.ip         = 0
        self.input      = deque()
        self.output     = deque()
        self.rel_base   = 0
        self.halt       = False
        self.is_waiting = False

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
                game.is_waiting = False
            else:
                game.prog[game.prog[game.ip+1] + offset] = -1
                game.is_waiting = True
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

def create_network(input):
    network, network_queue = [], []
    
    for network_address in range(50):
        prog = create_program(input)
        game = Game(prog)
        send_input(game, [network_address])
        network.append(game)
        network_queue.append([])
    
    return network, network_queue

def is_idle(network, network_queue):
    for network_address in range(50):
        if len(network_queue[network_address]) or \
           not network[network_address].is_waiting:
            return False
    return True

def find_double_nat_y(network, network_queue):
    nat, last_nat = [], None

    while True:
        for network_address in range(50):
            run_game(network[network_address])
            if (output := read_output(network[network_address])):
                network_queue[network_address].append(output)
                if len(network_queue[network_address]) == 3:
                    if network_queue[network_address][0] == 255:
                        nat = network_queue[network_address][1:]
                    else:
                        send_input(network[network_queue[network_address][0]], network_queue[network_address][1:])
                    network_queue[network_address] = []

        if is_idle(network, network_queue) and len(nat):
            if nat[1] == last_nat:
                return last_nat
            send_input(network[0], nat)
            last_nat, nat = nat[1], []

@timer
def solve():
    input = read_file("23")[0].split(",")
    network, network_queue = create_network(input)
    return find_double_nat_y(network, network_queue)

result = solve()
print(f"Solution: {result}")