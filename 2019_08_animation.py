from aoc import read_file, timer
from collections import defaultdict
from os import path
from PIL import Image, ImageDraw

def extract_layers(raw, size):
    layers = defaultdict(list)
    layer = -1

    for i in range(len(raw)):
        if not i % size:
            layer += 1
        layers[layer].append(raw[i])

    return layers

def print_image(layers):
    scale = 20
    for layer in range(100):
        img = Image.new('RGBA', (25*scale, 6*scale), (255, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        for y in range(6):
            for x in range(25):
                pos = x + y * 25
                if layers[layer][pos] == 0:
                    draw.ellipse((x*scale, y*scale, x*scale+scale-1, y*scale+scale-1), fill=(255, 255, 255))
                elif layers[layer][pos] == 1:
                    draw.ellipse((x*scale, y*scale, x*scale+scale-1, y*scale+scale-1), fill=(0, 0, 0))
        file_path = path.join('images', f"BIOS{100-layer:03}.png")
        img.save(file_path, 'PNG')

@timer
def solve():
    input   = read_file("08")
    input   = [int(x) for x in input[0]]

    size    = 25 * 6
    layers  = extract_layers(input, size)
    
    print_image(layers)

solve()