#!/usr/bin/python3
## Generate SVG image of a given board.

import chess
import chess.svg
import sys

board = chess.Board()
boardsvg = chess.svg.board(board=board)
f = open("BoardVisualisedFromFEN.svg", "w")
f.write(boardsvg)
f.close()
