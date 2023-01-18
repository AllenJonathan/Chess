from pieces import Knight
from pieces import Pawn, Bishop, Rook, King
import game_functions as f

position = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bp', 'bp', 'bp', '--', 'bp', 'bp', 'bp', 'bp'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', 'wB', '--', 'bp', '--', '--', '--', '--'],
    ['--', '--', '--', '--', 'wp', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['wp', 'wp', 'wp', 'wp', '--', 'wp', 'wp', 'wp'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', '--', 'wN', 'wR'],
        ]

am = Pawn.get_available_moves(position, (2, 1))
m = f.checkmate_filter(position, (2,1), am)

print(am)
print(m)
