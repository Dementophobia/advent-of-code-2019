from aoc import read_file, timer
from collections import defaultdict

def extract_layers(raw, size):
    layers = defaultdict(list)
    layer = -1

    for i in range(len(raw)):
        if not i % size:
            layer += 1
        layers[layer].append(raw[i])

    return layers

def print_image(layers):
    for y in range(6):
        for x in range(25):
            pos = x + y * 25
            for lay in range(100):
                if layers[lay][pos] == 2:
                    continue
                if layers[lay][pos] == 1:
                    print("#", end="")
                else:
                    print(" ", end="")
                break
        print()

@timer
def solve():
    input   = read_file("08")
    input   = [int(x) for x in input[0]]

    size    = 25 * 6
    layers  = extract_layers(input, size)
    
    print_image(layers)

solve()