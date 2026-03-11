#!/usr/bin/env python3
"""Roguelike dungeon — procedural dungeon with rooms and corridors."""
import sys, random

class Dungeon:
    def __init__(self, w=50, h=25, rooms=8, seed=42):
        random.seed(seed)
        self.w = w; self.h = h
        self.grid = [['#']*w for _ in range(h)]
        self.rooms_list = []
        self._gen_rooms(rooms)
        self._gen_corridors()
        # Place player and stairs
        r = self.rooms_list[0]
        self.px, self.py = r[0]+r[2]//2, r[1]+r[3]//2
        r2 = self.rooms_list[-1]
        self.grid[r2[1]+r2[3]//2][r2[0]+r2[2]//2] = '>'
        # Place items
        for room in self.rooms_list[1:-1]:
            if random.random() < 0.5:
                rx, ry = room[0]+random.randint(1,room[2]-2), room[1]+random.randint(1,room[3]-2)
                self.grid[ry][rx] = random.choice(['$', '!', '?'])
    def _gen_rooms(self, count):
        for _ in range(count * 10):
            if len(self.rooms_list) >= count: break
            rw = random.randint(4, 10); rh = random.randint(3, 6)
            rx = random.randint(1, self.w-rw-1); ry = random.randint(1, self.h-rh-1)
            if any(rx < r[0]+r[2]+1 and rx+rw+1 > r[0] and ry < r[1]+r[3]+1 and ry+rh+1 > r[1] for r in self.rooms_list):
                continue
            self.rooms_list.append((rx, ry, rw, rh))
            for y in range(ry, ry+rh):
                for x in range(rx, rx+rw):
                    self.grid[y][x] = '.'
    def _gen_corridors(self):
        for i in range(len(self.rooms_list)-1):
            r1, r2 = self.rooms_list[i], self.rooms_list[i+1]
            x1, y1 = r1[0]+r1[2]//2, r1[1]+r1[3]//2
            x2, y2 = r2[0]+r2[2]//2, r2[1]+r2[3]//2
            while x1 != x2:
                self.grid[y1][x1] = '.'; x1 += 1 if x2 > x1 else -1
            while y1 != y2:
                self.grid[y1][x1] = '.'; y1 += 1 if y2 > y1 else -1
    def render(self):
        for y in range(self.h):
            row = ""
            for x in range(self.w):
                if x == self.px and y == self.py: row += '@'
                else: row += self.grid[y][x]
            print(row)

if __name__ == "__main__":
    d = Dungeon(seed=int(sys.argv[1]) if len(sys.argv) > 1 else 42)
    d.render()
    print(f"\n@ = you, > = stairs, $ = gold, ! = potion, ? = scroll")
    print(f"{len(d.rooms_list)} rooms generated")
