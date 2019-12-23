from aoc import read_file, timer
from collections import defaultdict, deque
from math import sin, cos, radians
from PIL import Image, ImageDraw, ImageFont
from os import path

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

def get_connections(network, network_queue):
    nat, last_nat = [], None
    connections   = []
    steps         = 0
    
    while True:
        for network_address in range(50):
            run_game(network[network_address])
            if (output := read_output(network[network_address])):
                network_queue[network_address].append(output)
                if len(network_queue[network_address]) == 3:
                    if network_queue[network_address][0] == 255:
                        nat = network_queue[network_address][1:]
                        connections.append((steps, network_address, 50))
                    else:
                        send_input(network[network_queue[network_address][0]], network_queue[network_address][1:])
                        connections.append((steps, network_address, network_queue[network_address][0]))
                    network_queue[network_address] = []

        if is_idle(network, network_queue) and len(nat):
            if nat[1] == last_nat:
                return connections, last_nat
            send_input(network[0], nat)
            connections.append((steps, 50, network_address, nat[1]))
            last_nat, nat = nat[1], []
        steps += 1

def address_to_pixel(network_address, radius = 150):
    center_x, center_y = 170, 167
    angle = radians(network_address * 7.05)
    
    return (cos(angle) * radius + center_x, sin(angle) * radius + center_y)

def create_image(heat_nic, heat_cable, packets_sent, last_nat, current_connections, view, result = " None"):
    img = Image.new('RGBA', (600, 335), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for network_address in range(51):
        pos_x, pos_y = address_to_pixel(network_address, 150)
        draw.ellipse((pos_x-5, pos_y-5, pos_x+5, pos_y+5), fill=(heat_nic[network_address], 0, 255-heat_nic[network_address]))
    
    for connection, heat in heat_cable.items():
        source_x, source_y = address_to_pixel(connection[0], 145)
        target_x, target_y = address_to_pixel(connection[1], 145)
        draw.line((source_x, source_y, target_x, target_y), fill = (heat, 0, 255-heat))
    
    for connection in current_connections:
        source_x, source_y = address_to_pixel(connection[0], 145)
        target_x, target_y = address_to_pixel(connection[1], 145)
        draw.line((source_x, source_y, target_x, target_y), fill = (255, 255, 100))
        
        source_x, source_y = address_to_pixel(connection[0], 150)
        target_x, target_y = address_to_pixel(connection[1], 150)
        draw.ellipse((source_x-5, source_y-5, source_x+5, source_y+5), fill=(255, 255, 100))
        draw.ellipse((target_x-5, target_y-5, target_x+5, target_y+5), fill=(255, 255, 100))
    
    draw.rectangle((380, 0, 600, 145),   fill=(0, 0, 0))
    draw.rectangle((380, 200, 600, 335), fill=(0, 0, 0))
    
    fnt = ImageFont.truetype('C:\Windows\Fonts\courbd.ttf', 26)
    if not view:
        draw.text((430, 20), f"Booting", font=fnt, fill=(255, 255, 255))
        draw.text((430, 50), f"Network", font=fnt, fill=(255, 255, 255))
    else:
        draw.text((415, 20), f"Analyzing", font=fnt, fill=(255, 255, 255))
        draw.text((430, 50), f"Network",   font=fnt, fill=(255, 255, 255))
    
    fnt = ImageFont.truetype('C:\Windows\Fonts\courbd.ttf', 16)
    draw.text((395, 200), f"Network Monitoring", font=fnt, fill=(255, 255, 255))
    
    fnt = ImageFont.truetype('C:\Windows\Fonts\courbd.ttf', 14)
    draw.text((390, 110), f"Last NAT Code:", font=fnt, fill=(255, 255, 255))
    draw.text((534, 110), f"{last_nat}",     font=fnt, fill=(255, 255, 255))
    
    draw.text((390, 130), f"Solution:", font=fnt, fill=(255, 255, 255))
    draw.text((534, 130), f"{result}",  font=fnt, fill=(255, 255, 255))
    
    max_heat_nic = max(heat_nic.values()) // 5 + 20
    draw.text((390, 240), f"Max. Nic Heat:",   font=fnt, fill=(255, 255, 255))
    draw.text((540, 240), f"{max_heat_nic}°C", font=fnt, fill=(255, 255-(max_heat_nic-20)*5, 255-(max_heat_nic-20)*5))
    
    max_heat_cable = max(heat_cable.values()) // 3 + 20
    draw.text((390, 260), f"Max. Cable Heat:",   font=fnt, fill=(255, 255, 255))
    draw.text((540, 260), f"{max_heat_cable}°C", font=fnt, fill=(255, 255-(max_heat_cable-20)*5, 255-(max_heat_cable-20)*5))
    
    draw.text((390, 280), f"Packets sent:",     font=fnt, fill=(255, 255, 255))
    draw.text((541, 280), f"{packets_sent:04}", font=fnt, fill=(255, 255, 255))
    
    file_path = path.join('images', f"test{view:03}.png")
    img.save(file_path, 'PNG')

def draw_connections(connections, result):
    heat_nic     = defaultdict(int)
    heat_cable   = defaultdict(int)
    view         = 0
    packets_sent = 0
    last_nat     = " None"
    
    while len(connections):
        step = connections[0][0]
        current_connections = [connection[1:3] for connection in connections if connection[0] == step]
        last = [connection[3] for connection in connections if connection[0] == step and connection[1] == 50]
        if len(last):
            last_nat = str(last[0])

        packets_sent += len(current_connections)
        
        for connection in current_connections:
            heat_nic[connection[0]] += 1
            heat_nic[connection[1]] += 1
            heat_cable[(connection[0], connection[1])] += 1
        
        create_image(heat_nic, heat_cable, packets_sent, last_nat, current_connections, view)
        view += 1
        connections = [connection for connection in connections if connection[0] != step]
    
    create_image(heat_nic, heat_cable, packets_sent, last_nat, [], view, result)

@timer
def solve():
    input = read_file("23")[0].split(",")
    network, network_queue = create_network(input)
    connections, result = get_connections(network, network_queue)
    print("Finished calculating connections, starting to draw")
    draw_connections(connections, result)

result = solve()
print(f"Solution: {result}")