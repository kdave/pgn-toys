#!/usr/bin/python3

import sys
import sqlite3
import os
import time

source = open("index.txt")
commit = 100000
reportafter = 1
maxindex = 88092721

dbconn = sqlite3.connect('index.txt.sqlite', isolation_level='DEFERRED')
db = dbconn.cursor()
db.execute('''PRAGMA synchronous = OFF''')
db.execute('''PRAGMA journal_mode = OFF''')
db.execute('''PRAGMA temp_store = memory''')

db.execute("drop table if exists tab")
db.execute("create table tab(idx INT, off INT)")
index = 1

names = ('index', 'offset', 'hash')
ccount = commit
mcache = []
print("Commit after:", commit)
ts = time.time()
while True:
    line = source.readline()
    sp = line.split(" ")
    # len("index=")
    if sp[0] == '':
        break
    index = int(sp[0][6:])
    # len("hoff=")
    offset = int(sp[1][5:])
    mcache.append((index, offset))
    if ccount <= 0:
        now = time.time()
        if now - ts > reportafter:
            print(f"Progress, index {index}, offset {offset}, {100.0*index/88092721:.2f}%", end="\r")
            ts = now
        db.executemany("insert into tab values (?, ?)", mcache)
        dbconn.commit()
        ccount = commit
        mcache = []
    else:
        ccount -= 1
    index += 1

db.executemany("insert into tab values (?, ?)", mcache)
dbconn.commit()
source.close()
