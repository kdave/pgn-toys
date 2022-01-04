#!/usr/bin/python3

import chess.pgn

f = open("lichess.pgn", 'r')
game = chess.pgn.read_game(f)
print(game)
endnode = game.end()
print(endnode)
print(endnode.ply())
