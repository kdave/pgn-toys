#!/usr/bin/python3
## Print headers of all games in a given PGN file.

import chess.pgn
import sys

fn = sys.argv[1]
pgn = open(fn)

index = 1
while True:
    offset = pgn.tell()

    headers = chess.pgn.read_headers(pgn)
    if headers is None:
        break
    if (index % 10000) == 0:
        print(f"Game {index}")
    print(headers)
    index += 1

print(f"End {index}")
pgn.close()
