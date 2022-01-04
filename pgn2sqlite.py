#!/usr/bin/python3

import chess
import chess.pgn
import sqlite3
import sys
import mmap
import re
import time
import os

# Config
fn = "lichess.pgn"
filesize = os.path.getsize(fn)
dbn = fn + ".sqlite"
commit = 10000

cols = {
    'num': 'int',
    'offset': 'int',
    'wname': 'text',
    'bname': 'text',
    'welo': 'int',
    'belo': 'int',
    'result': 'text',
    'tc': 'text',
    'plies': 'int',
    'eco': 'text',
    'ref': 'text'
}
insertmarks = "?, " * (len(cols) - 1) + "?"

# Open PGN
f = open(fn, "r")
mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
mm.madvise(mmap.MADV_SEQUENTIAL)
games = f

# Set up DB
dbconn = sqlite3.connect(dbn)
db = dbconn.cursor()

db.execute("DROP TABLE IF EXISTS pgn")
db.execute("CREATE TABLE pgn (" + ", ".join([ f"{x[0]} {x[1]}" for x in cols.items()]) + ")")
#sys.exit()

# Main loop
mcache = []
mcached = 0
ccount = commit
index = 1
ts = time.time()
while True:
    headeroff = games.tell()
    game = chess.pgn.read_game(games)
    if not game:
        break
    plies = game.end().ply()
    #ref = re.search(r"lichess.org/(.*)$", game.headers["Site"])[1]
    ref = game.headers["Site"]
    mcache.append(
        (
            index,
            headeroff,
            game.headers["White"],
            game.headers["Black"],
            game.headers["WhiteElo"],
            game.headers["BlackElo"],
            game.headers["Result"],
            game.headers["TimeControl"],
            plies,
            game.headers["ECO"],
            ref
        )
    )
    mcached += 1
    if ccount <= 0:
        db.executemany("INSERT INTO pgn VALUES (" + insertmarks + ")", mcache)
        dbconn.commit()
        ccount = commit
        mcache = []
        mcached = 0
    else:
        ccount -= 1
    now = time.time()
    if now - ts > 1:
        ts = now
        print(f"Processed {index} games (cached {mcached}), {100.0*headeroff/filesize:.2f}%")
    index += 1

# Final flush of cached items
db.executemany("INSERT INTO pgn VALUES (" + insertmarks + ")", mcache)
dbconn.commit()
