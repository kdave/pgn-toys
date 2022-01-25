#!/usr/bin/python3
# Generate arrows.html with svg images of piece movement

# TODO:
# - castling
# - en passant
# - promotion

import chess
import chess.pgn
import chess.svg

gamefile = "game2.pgn"
f = open(gamefile, 'r')
game = chess.pgn.read_game(f)
board = chess.Board()

# Initial positions of white pieces
winitial = {
    # White panws
    'wpa': 'a2',
    'wpb': 'b2',
    'wpc': 'c2',
    'wpd': 'd2',
    'wpe': 'e2',
    'wpf': 'f2',
    'wpg': 'g2',
    'wph': 'h2',
    # White pieces
    'wRa': 'a1',
    'wNb': 'b1',
    'wBc': 'c1',
    'wQ':  'd1',
    'wK':  'e1',
    'wBf': 'f2',
    'wNg': 'g1',
    'wRh': 'h1'
}
wlast = {}

binitial = {
    # Black panws
    'bph': 'h7',
    'bpg': 'g7',
    'bpf': 'f7',
    'bpe': 'e7',
    'bpd': 'd7',
    'bpc': 'c7',
    'bpb': 'b7',
    'bpa': 'a7',
    # Black pieces
    'bRh': 'h8',
    'bNg': 'g8',
    'bBf': 'f8',
    'bK':  'e8',
    'bQ':  'd8',
    'bBc': 'c8',
    'bNb': 'b8',
    'bRa': 'a8'
}
blast = {}

def update_move(pmoves, oppmoves, mv, castling, enpassant):
    #print(f"UPDATE: {mfrom} -> {mto}")
    capture = board.is_capture(mv)
    a, b, c, d = str(mv)
    mfrom = a + b
    mto = c + d
    if castling:
        print("CASTLING")
    for k, v in pmoves.items():
        #print(f"k={k} v={v}")
        if mfrom == v[-1]:
            print(f"Move {k} from {mfrom} to {mto}")
            pmoves[k].append(mto)
            if capture:
                # Find opponent's piece in the target square
                for ok, ov in oppmoves.items():
                    if mto == ov[-1]:
                        print("Captured")
                        oppmoves[ok].append('C')
            return

def squares_to_moves(slist):
    # [0, 1, 2, ...]
    ret = []
    if len(slist) < 2:
        return ret
    a = slist[0]
    for i in range(1, len(slist)):
        b = slist[i]
        if b == 'C':
            break
        arr = chess.svg.Arrow(chess.parse_square(a), chess.parse_square(b))
        ret.append(arr)
        a = b
    return ret

for k, v in winitial.items():
    wlast[k] = [v]

for k, v in binitial.items():
    blast[k] = [v]

for mv in game.mainline_moves():
    turn = board.turn
    castling = board.is_castling(mv)
    enpassant = board.is_en_passant(mv)
    board.push(mv)
    if turn == chess.WHITE:
        update_move(wlast, blast, mv, castling, enpassant)
    else:
        update_move(blast, wlast, mv, castling, enpassant)

def generate_moves(color, last, outfile, cols=8, size=160, flipped=False):
    i = 1
    for piece, moves in last.items():
        print(f"MOVES: {piece} -> {moves}")
        arrows = squares_to_moves(moves)
        print(arrows)
        board = chess.Board()
        board.clear()
        piece = chess.Piece.from_symbol(piece[1])
        piece.color = color
        board.set_piece_at(square=chess.parse_square(moves[0]), piece=piece)
        svgb = chess.svg.board(board=board, orientation=color, arrows=arrows,
                size=size, flipped=flipped)
        outfile.write("<td>" + svgb + "</td>")
        if i == cols:
            outhtml.write("</tr><tr>")
            i = 1
        else:
            i += 1

# main()
outhtml = open("arrows.html", "w")

outhtml.write("<html><body><table>")
outhtml.write("<tr>")

view = chess.WHITE
view = chess.BLACK

if view == chess.WHITE:
    print("Black movement")
    generate_moves(chess.BLACK, blast, outhtml, flipped=True)
    print("White movement")
    generate_moves(chess.WHITE, wlast, outhtml)
else:
    print("White movement")
    generate_moves(chess.WHITE, wlast, outhtml, flipped=True)
    print("Black movement")
    generate_moves(chess.BLACK, blast, outhtml)

outhtml.write("</tr></table>")
outhtml.write("</body></html>")
outhtml.close()
