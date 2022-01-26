#!/usr/bin/python3

import chess.pgn

f = open("lichess.pgn", 'r')
game = chess.pgn.read_game(f)
board = chess.Board()
for h in game.headers.items():
    print(f'[{h[0]} "{h[1]}"]')

print('')

for mv in game.mainline_moves():
    print(f"{int(board.ply()/2) + 1}. {mv.uci()} ({board.san(mv)})")
    board.push(mv)
