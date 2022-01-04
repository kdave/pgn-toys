#!/usr/bin/python3

import chess.pgn
import sys

count = 100000

fn = sys.argv[1]
f = open(fn, 'r')
while count > 0:
    game = chess.pgn.read_game(f)
    print(game, end='\n\n')
    count -= 1
