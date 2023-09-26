#!/usr/bin/python3
## Filter games in a given PGN file by players' Elo.

import chess.pgn
import sys

fn = sys.argv[1]
pgn = open(fn)

while True:
    offset = pgn.tell()

    headers = chess.pgn.read_headers(pgn)
    if headers is None:
        break
    welo = int(headers['WhiteElo'])
    belo = int(headers['BlackElo'])
    here = pgn.tell()
    if welo < 1100 and belo < 1100:
        pgn.seek(offset)
        game = chess.pgn.read_game(pgn)
        print(game, end="\n\n")
        pgn.seek(here)

pgn.close()
