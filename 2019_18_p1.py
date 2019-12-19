from aoc import read_file, timer
from collections import defaultdict
from copy import copy

class Key:
    def __init__(self, dungeon, position, type):
        self.position         = position
        self.type             = type
        self.distance_to_keys = self.get_key_distances(dungeon)
        self.blocked_by_doors = self.get_blocking_doors(dungeon)

    def get_key_distances(self, dungeon):
        next_search = defaultdict(int)
        next_search[self.position] = 1
        keys    = {}
        changes = True
        steps   = 0
        
        while changes or not steps:
            changes = False
            steps  += 1
            search = copy(next_search)
            
            for position, state in search.items():
                if state == -1:
                    del next_search[position]
                if state == 1:
                    next_search[position] = -1
                    for side in [(-1,0), (0,-1), (1,0), (0,1)]:
                        side_pos = (position[0] + side[0], position[1] + side[1])
                        if dungeon.area[side_pos] != "#" and \
                           not search[side_pos]:
                            del search[side_pos]
                            changes = True
                            next_search[side_pos] = 1
                            if dungeon.area[side_pos].islower():
                                keys[dungeon.area[side_pos]] = steps
        return keys

    def get_blocking_doors(self, dungeon):
        if self.type == "@":
            return []

        next_search = defaultdict(list)
        next_search[dungeon.position] = [1]
        
        while True:
            search = copy(next_search)
            
            for position, state in search.items():
                if state[0] == -1:
                    del next_search[position]
                if state[0] == 1:
                    next_search[position] = [-1]
                    for side in [(-1,0), (0,-1), (1,0), (0,1)]:
                        side_pos = (position[0] + side[0], position[1] + side[1])
                        if dungeon.area[side_pos] != "#" and \
                           not search[side_pos]:
                            del search[side_pos]
                            next_search[side_pos] = copy(state)
                            if dungeon.area[side_pos] == self.type:
                                return state[1:]
                            elif dungeon.area[side_pos].isupper():
                                next_search[side_pos].append(dungeon.area[side_pos])

class Dungeon:
    def __init__(self, layout):
        self.area         = defaultdict(str)
        self.size_x       = len(layout[0])
        self.size_y       = len(layout)
        self.position     = (0, 0)
        self.key_pos      = {}
        
        for y in range(self.size_y):
            for x in range(self.size_x):
                self.area[(x, y)] = layout[y][x]
                if self.area[(x, y)].islower():
                    self.key_pos[self.area[(x, y)]] = (x, y)
                elif self.area[(x, y)] == "@":
                    self.position = (x, y)
        
        self.reduce_dungeon()
    
    def is_dead_end(self, pos, keys_allowed = False):
        tile = self.area[pos]
        if tile == "#" or tile == "@" or (not keys_allowed and tile.islower()):
            return False
        
        count = sum(self.area[(pos[0] + side[0], pos[1] + side[1])] != "#" for side in [(-1,0), (0,-1), (1,0), (0,1)])
        
        if count <= 1:
            return True
        return False
    
    def reduce_dungeon(self):
        reduced = True
        while reduced:
            reduced = False
            for y in range(1, self.size_y):
                for x in range(1, self.size_x):
                    if self.is_dead_end((x, y)):
                        self.area[(x, y)] = "#"
                        reduced = True

def create_keys(dungeon):
    keys = {}
    for type, position in dungeon.key_pos.items():
        keys[type] = Key(dungeon, position, type)
        
    keys["@"] = Key(dungeon, dungeon.position, "@")
        
    return keys
 
def get_reachable_keys(keys, keys_taken, doors_opened):
    reachable = set()
    for key in keys.values():
        if len(set(key.blocked_by_doors) & doors_opened) == len(key.blocked_by_doors) and \
           key.type not in keys_taken:
            reachable.add(key)
    return reachable
    
def fetch_keys(keys, keys_taken, doors_opened, current_key = "@", known_best = 1e8, path = 0, known_situations = {}):
    if len(keys_taken) == len(keys):
        return path
    
    best_path = known_best
    reachable_keys = get_reachable_keys(keys, keys_taken, doors_opened)
    reachable_keys = sorted(reachable_keys, key = lambda x: keys[current_key].distance_to_keys[x.type])
        
    for next_key in reachable_keys:
        next_path = path + keys[current_key].distance_to_keys[next_key.type]

        current_situation = tuple(sorted(list(keys_taken)) + [next_key.type])

        if current_situation in known_situations:
            if next_path >= known_situations[current_situation]:
                continue

        known_situations[current_situation] = next_path
        
        if next_path >= best_path:
            continue
        
        next_keys_taken   = keys_taken   | set(next_key.type)
        next_doors_opened = doors_opened | set(next_key.type.upper())
        
        this_path = fetch_keys(keys, next_keys_taken, next_doors_opened, next_key.type, best_path, next_path, known_situations)
        if this_path < best_path:
            best_path = this_path

    return best_path

@timer
def solve():
    input        = read_file("18")
    dungeon      = Dungeon(input)
    keys         = create_keys(dungeon)
    keys_taken   = set(("@"))
    doors_opened = set()
    
    return fetch_keys(keys, keys_taken, doors_opened)

result = solve()
print(f"Solution: {result}")