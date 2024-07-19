#!/usr/bin/python3
## Generate *game.html* with annotated board (last move, top moves, engine eval),
## navigation buttons (PGN game1.pgn)
## <br> <img src="examples/game-eval/pgn-to-html-move.png" width="256" />

# Todo:
# - analyze but skip book moves

import chess
import chess.svg
import chess.pgn
import chess.engine

# Input
gamefile = "game1.pgn"

# Engine options
time_limit = 0.1
threads = 2
hashmb = 64
pv = 4
engine = None
enginename = 'stockfish'

def gen_navistr(board, ply):
    ret = ''
    bprev = ply - 1
    bnext = ply + 1
    if bprev < 1:
        bprev = 1
    q = "'"
    ret += f'<div id="ply{ply}">'
    ret += f'<input type=button value="[PREV]" onclick="document.getElementById({q}ply{bprev}{q}).scrollIntoView();" /> '
    ret += f'<input type=button value="[NEXT]" onclick="document.getElementById({q}ply{bnext}{q}).scrollIntoView();" /><br/>'
    ret += '</div>'
    return ret

def pretty_score(score):
    if score.is_mate():
        return str(score.white())

    cp = float(score.white().score()) / 100.0
    return str(cp)

def calc_nscore(score):
    return score.white().score(mate_score=1000) / 100.0

def pretty_score_bar(score):
    width = 20
    halfw = float(width)/2
    nscore = calc_nscore(score)
    beval = '█'
    weval = '░'
    if nscore < -halfw:
        scorestr = beval * width
    elif nscore > halfw:
        scorestr = weval * width
    else:
        nscore += halfw
        times = int(nscore + 0.5)
        scorestr = beval * (width - times)
        scorestr += weval * times
    print(f"SCORESTR {nscore:.2f} {nscore-halfw:.2f}:", scorestr)
    return scorestr

def move_to_arr(move, color):
    arr = chess.svg.Arrow(move.from_square, move.to_square)
    arr.color = color
    return arr

def evaluate_move(board, rootmove):
    global engine
    colors = [ 'green', 'green', 'blue', 'blue' ]
    if not engine:
        print(f"Starting engine {enginename}, time/move={time_limit} threads={threads} hash={hashmb} pv={pv}")
        engine = chess.engine.SimpleEngine.popen_uci(enginename)
        engine.configure({"Threads": threads})
        engine.configure({"Hash": hashmb})

    pcolor = ''
    if board.turn == chess.BLACK:
        pcolor = '...'

    result = engine.analyse(board, chess.engine.Limit(time=time_limit), multipv=pv)
    score0 = result[0]['score']
    ret = f"Move {pcolor}{(board.ply() // 2) + 1}: " + board.san(rootmove)
    ret += "<br><b>Eval: " + pretty_score(score0) + "</b>"
    arrows = []
    # Threat/ponder
    try:
        pondermove = result[0]['pv'][1]
        arrows.append(move_to_arr(pondermove, 'red'))
        ret += f"<br><font color=red>Ponder: {board.san(pondermove)}</font>"
    except:
        pass
    for i in range(len(result)):
        #print("PV", i, " ", result[i])
        pvmove = result[i]['pv'][0]
        san = board.san(pvmove)
        arrows.append(move_to_arr(pvmove, colors[i]))
        score = pretty_score(result[i]['score'])
        print(f"Move: {san} Score: {score}")
        ret += f"<br><font color={colors[i]}>{i+1}: {san}, score {score}</font>"
    scorestr = pretty_score_bar(score0)
    ret += f"<br><div style='border: 1px solid black; background: #eee;'>{scorestr}</div>";
    return (ret, arrows)

# Main

with open(gamefile, 'r') as f:
    game = chess.pgn.read_game(f)
board = chess.Board()

outhtml = open("game.html", "w")
outhtml.write("<html><body><table>")

ply = 1
for mv in game.mainline_moves():
    outhtml.write("<tr>")
    print(f"Generating move {mv}")
    evalstr, arrows = evaluate_move(board, mv)
    navistr = gen_navistr(board, ply)
    board.push(mv)
    svg = chess.svg.board(board=board, lastmove=mv, arrows=arrows, size=480)
    outhtml.write("<td>" + svg + "</td>")
    outhtml.write("<td valign=top>")
    outhtml.write(navistr)
    outhtml.write(evalstr)
    outhtml.write("</td>")
    outhtml.write("</tr>")
    ply += 1

outhtml.write("</table>")
outhtml.write("</body></html>")
outhtml.close()

if engine:
    engine.quit()
