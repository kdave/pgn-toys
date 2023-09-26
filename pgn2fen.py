#!/usr/bin/python3
## Print FEN of each move (PGN game).

import chess.pgn

f = open("lichess.pgn", 'r')
game = chess.pgn.read_game(f)
board = chess.Board()
for h in game.headers.items():
    print(f'[{h[0]} "{h[1]}"]')

print('')

for mv in game.mainline_moves():
    board.push(mv)
    print(board.fen())
