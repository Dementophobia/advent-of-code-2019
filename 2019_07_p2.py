from aoc import read_file, timer
from itertools import permutations

class Amp:
    def __init__(self, prog):
        self.prog           = prog[:]
        self.ip             = 0
        self.output         = 0
        self.input_counter  = 0
        self.halt           = False

def split_instruction(instruction):
    instruction = f"{instruction:05}"
    return instruction[3:], instruction[0:3]

def get_values(input, pos, op, modes):
    mode_a, mode_b, mode_c = modes
    values = []
    
    if op in ["01", "02", "04", "05", "06", "07", "08"]:
        if mode_c == "0":
            values.append(input[input[pos+1]])
        else:
            values.append(input[pos+1])

        if op in ["01", "02", "05", "06", "07", "08"]:
            if mode_b == "0":
                values.append(input[input[pos+2]])
            else:
                values.append(input[pos+2])

            if op in []:
                if mode_a == "0":
                    values.append(input[input[pos+3]])
                else:
                    values.append(input[pos+3])

    return values
  
def run_amp(phase, input, amp):
    while amp.prog[amp.ip] != 99:
        op, modes = split_instruction(amp.prog[amp.ip])
        values = get_values(amp.prog, amp.ip, op, modes)
        
        if op == "01": # Addition
            amp.prog[amp.prog[amp.ip+3]] = values[0] + values[1]
            amp.ip += 4
    
        if op == "02": # Multiplication
            amp.prog[amp.prog[amp.ip+3]] = values[0] * values[1]
            amp.ip += 4
        
        if op == "03": # Read and Store input
            if not amp.input_counter:
                amp.prog[amp.prog[amp.ip+1]] = phase
            else:
                amp.prog[amp.prog[amp.ip+1]] = input
            
            amp.input_counter += 1
            amp.ip += 2

        if op == "04": # Print Output
            amp.output = values[0]
            amp.ip += 2
            return amp

        if op == "05": # Jump-if-True
            if values[0]:
                amp.ip = values[1]
            else:
                amp.ip += 3

        if op == "06": # Jump-if-False
            if not values[0]:
                amp.ip = values[1]
            else:
                amp.ip += 3
        
        if op == "07": # Less than
            if values[0] < values[1]:
                amp.prog[amp.prog[amp.ip+3]] = 1
            else:
                amp.prog[amp.prog[amp.ip+3]] = 0
            amp.ip += 4

        if op == "08": # Equals
            if values[0] == values[1]:
                amp.prog[amp.prog[amp.ip+3]] = 1
            else:
                amp.prog[amp.prog[amp.ip+3]] = 0
            amp.ip += 4
    
    amp.halt = True
    return amp

@timer
def solve():
    prog = read_file("07")[0].split(",")
    prog = [int(x) for x in prog]
    max_thrust = 0

    for phases in permutations(range(5, 10), 5):
        amps = [Amp(prog) for i in range(5)]
        active = 0

        while not amps[4].halt:
            amps[active] = run_amp(phases[active], amps[active-1].output, amps[active])
            active       = (active + 1) % 5
    
        max_thrust = max(max_thrust, amps[4].output)
    return max_thrust

result = solve()
print(f"Solution: {result}")
       
