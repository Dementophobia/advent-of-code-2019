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

@timer
def solve():
    input   = read_file("08")
    input   = [int(x) for x in input[0]]

    size    = 25 * 6
    layers  = extract_layers(input, size)
    
    zero_counts  = [pixels.count(0) for pixels in layers.values()]
    result_layer = zero_counts.index(min(zero_counts))
    
    return layers[result_layer].count(1) * layers[result_layer].count(2)

result = solve()
print(f"Solution: {result}")