from aoc import read_file, timer
from collections import defaultdict
from copy import copy


class Dungeon:
    def __init__(self, layout):
        self.area         = defaultdict(str)
        self.size_x       = len(layout[2])+4
        self.size_y       = len(layout)
        self.portals      = defaultdict(list)
        self.portal_names = defaultdict(str)
        self.paths        = defaultdict(list)
        
        for y in range(self.size_y):
            for x in range(self.size_x):
                if x < len(layout[y]):
                    self.area[(x, y)] = layout[y][x]
        
        self.reduce_dungeon()
        self.find_portals()
        self.find_paths()

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

    def find_portals(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.area[(x, y)].isupper():
                    if self.area[(x+1, y)].isupper():
                        name = self.area[(x, y)] + self.area[(x+1, y)]
                        if not name in [p[0] for p in self.portals]:
                            id = 0
                        else:
                            id = 1
                        if self.area[(x+2, y)] == ".":
                            self.portals[(name, id)].append((x+2, y))
                            self.portal_names[(x+1, y)] = (name, id)
                        elif self.area[(x-1, y)] == ".":
                            self.portals[(name, id)].append((x-1, y))
                            self.portal_names[(x, y)] = (name, id)
                            
                    elif self.area[(x, y+1)].isupper():
                        name = self.area[(x, y)] + self.area[(x, y+1)]
                        if not name in [p[0] for p in self.portals]:
                            id = 0
                        else:
                            id = 1
                        if self.area[(x, y+2)] == ".":
                            self.portals[(name, id)].append((x, y+2))
                            self.portal_names[(x, y+1)] = (name, id)
                        elif self.area[(x, y-1)] == ".":
                            self.portals[(name, id)].append((x, y-1))
                            self.portal_names[(x, y)] = (name, id)
                        
    def find_paths(self):
        for name, positions in self.portals.items():
            for pos in positions:
                next_search = defaultdict(int)
                next_search[pos] = 1

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
                                if self.area[side_pos] != "#" and \
                                 not search[side_pos]:
                                    del search[side_pos]
                                    changes = True
                                    next_search[side_pos] = 1
                                    if self.area[side_pos].isupper():
                                        next_search[side_pos] = -1
                                        if steps > 1:
                                            target_name = self.portal_names[(side_pos)]
                                            self.paths[name].append((target_name, steps-1))

def find_shortest_way(dungeon, path = [("AA", 0)], best_steps = 1e8, steps = 0):
    if path[-1] == ("ZZ", 1):
        return steps

    for next_portal in dungeon.paths[path[-1]]:
        if next_portal[0] in path:
            continue
        
        next_steps = steps + next_portal[1] + 1
        if next_steps >= best_steps:
            continue

        if next_portal[0][1] == 0:
            id = 1
        else:
            id = 0
            
        next_path = path + [next_portal] + [(next_portal[0][0], id)]
        this_steps = find_shortest_way(dungeon, next_path, best_steps, next_steps)

        if this_steps < best_steps:
            best_steps = this_steps
    
    return best_steps

@timer
def solve():
    input = read_file("20", strip = False)
    dungeon = Dungeon(input)
    return find_shortest_way(dungeon) - 1

result = solve()
print(f"Solution: {result}")