#!/usr/bin/python3

import mmap
import sys

#fn = "lichess_db_standard_rated_2021-10.pgn"
fn = "lichess.pgn"

index = 1
f = open(fn, "r+b")
mm = mmap.mmap(f.fileno(), 0)
while True:
    hoff = mm.tell()
    moff = mm.find(b'\n\n')
    if moff == -1:
        print(f"END, header no game, pos {mm.tell()}")
        sys.exit(0)
    moff += 2
    mm.seek(moff)
    endofgame = mm.find(b'\n\n')
    if endofgame == -1:
        print(f"END, endofgame, pos {mm.tell()}")
        sys.exit(0)
    mm.seek(endofgame + 2)
    print(f"index={index} hoff={hoff} moff={moff}")
    index += 1

mm.close()
