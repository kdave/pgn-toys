#!/usr/bin/python3
## Print evaluation of each move in a PGN game (default engine settings).

import chess
import chess.pgn

board = chess.Board()
with open("game7.pgn", "r") as f:
    game = chess.pgn.read_game(f)

for mv in game.mainline_moves():
    board.push(mv)
    print(game.eval())
