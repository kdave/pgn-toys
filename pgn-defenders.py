#!/usr/bin/python3
## Find defenders of your piece in a given position (Scandi btw).

import chess
import chess.pgn
import chess.svg

# Scandi: 1. e4 d5 2. exd5 Qxd5
# Defenders of d2 pawn:
# - N b1
# - B c1
# - Q d1
# - K e1

def find_defenders2(board, square):
    piece = board.piece_at(square)
    color = piece.color

    return board.attackers(color, square)

def find_defenders(board, square):
    piece = board.piece_at(square)
    color = piece.color

    print(f"Find defenders of {chess.square_name(square)}")
    d = []
    for sq in chess.SQUARES:
        sqpiece = board.piece_at(sq)
        if not sqpiece or sq == square:
            continue
        if sqpiece.color != color:
            continue
        attacks = board.attacks(sq)
        if square in attacks:
            print(f"Defender {chess.square_name(sq)} {sqpiece} {[chess.square_name(x) for x in list(attacks)]}")
            d.append(sq)

    return d

board = chess.Board()
board.push_san("e4")
board.push_san("d5")
board.push_san("exd5")
board.push_san("Qxd5")

print(board)

defof = chess.D2
d = find_defenders(board, defof)
print("d", d)
d2 = find_defenders(board, defof)
print("d2", d2)

arr = []
for sq in d:
    arr.append(chess.svg.Arrow(sq, defof))

svg = chess.svg.board(board, arrows=arr, size=480)
with open("defenders.svg", "w") as f:
    f.write(svg)
