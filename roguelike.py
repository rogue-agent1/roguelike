#!/usr/bin/env python3
"""Tiny roguelike dungeon crawler."""
import sys, random
random.seed(42); W,H=40,20; HP=20; GOLD=0
def gen_dungeon():
    d=[['#']*W for _ in range(H)]
    rooms=[]
    for _ in range(6):
        rw,rh=random.randint(4,8),random.randint(3,5)
        rx,ry=random.randint(1,W-rw-1),random.randint(1,H-rh-1)
        for y in range(ry,ry+rh):
            for x in range(rx,rx+rw): d[y][x]='.'
        rooms.append((rx+rw//2,ry+rh//2))
    for i in range(len(rooms)-1):
        x1,y1=rooms[i]; x2,y2=rooms[i+1]
        while x1!=x2: d[y1][x1]='.'; x1+=1 if x2>x1 else -1
        while y1!=y2: d[y1][x1]='.'; y1+=1 if y2>y1 else -1
    # Place items
    for _ in range(5):
        r=random.choice(rooms); d[r[1]+random.randint(-1,1)][r[0]+random.randint(-1,1)]='$'
    for _ in range(3):
        r=random.choice(rooms); d[r[1]+random.randint(-1,1)][r[0]+random.randint(-1,1)]='M'
    return d,rooms
d,rooms=gen_dungeon()
px,py=rooms[0]; d[py][px]='@'
ex,ey=rooms[-1]; d[ey][ex]='>'
for row in d: print(''.join(row))
print(f"\n@ = you, $ = gold, M = monster, > = exit")
print(f"HP: {HP}, Rooms: {len(rooms)}")
