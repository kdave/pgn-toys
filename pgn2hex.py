#!/usr/bin/python3

import chess.pgn
import struct
import sys

f = open("lichess.pgn", 'r')
offset = 0

hdrstart = offset
headers = chess.pgn.read_headers(f)
movestart = f.tell()

game = chess.pgn.read_game(f)
bstr = b''
for mv in game.mainline_moves():
    # a2c4
    a, b, c, d = str(mv)
    # Encode letters to numbers, starting with a=1
    a = ord(a) - ord('a') + 1
    c = ord(c) - ord('a') + 1
    m = f"{a}{b}{c}{d}"
    #print("M", mv, "H", m)
    x = int(m, 16)
    #print(mv, hex(x))
    #print('x', x)
    p = struct.pack('>H', x)
    #print(p)
    sys.stdout.buffer.write(p)
    bstr += p

eog = struct.pack('>H', 0x0a0a)
sys.stdout.buffer.write(eog)

print(bstr)
