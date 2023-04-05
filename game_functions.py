import copy
import pygame
import game_data as gd
from pieces import Pawn, Knight, Bishop, Rook, Queen, King

pieces_dict = {
    'p': Pawn,
    'N': Knight,
    'B': Bishop,
    'R': Rook,
    'Q': Queen,
    'K': King,
}


def get_board_length():
    native_res = pygame.display.Info()
    side_length = (min(native_res.current_h, native_res.current_w) - 100)
    side = side_length - (side_length % 8)
    return side


def get_pos(x, y):
    s_x = x // gd.square_length
    s_y = y // gd.square_length
    return s_x, s_y


def get_square(board, pos):
    x, y = pos
    if x < 0 or y < 0:
        return None
    try:
        square = board.data[y][x]
    except IndexError:
        return None
    else:
        return square


def check_and_castle(board, piece, pos1, pos2, moves):
    # Three rules to be followed 1 -> The king and the rook must not have moves previously -> already done in
    # 'update_castling_rights' 2 -> The squares between the king and the rook must be vacant -> already done in
    # 'King.get_available_moves' 3 -> The king should leave, crossover or finish in a square which is attacked ->
    #                                 already done in 'King.get_available_moves'

    if piece.__class__ == King:
        if pos1 == (4, 7):
            # white
            if pos2 == (6, 7) and pos2 in moves:
                # short
                board.update_piece(pos1, pos2)
                board.update_piece((7, 7), (5, 7))
                gd.white_castle_short = False
                print(gd.black_castle_long, gd.black_castle_short, gd.white_castle_long, gd.white_castle_short)
                return True
            elif pos2 == (2, 7) and pos2 in moves:
                # long
                print(pos1, pos2)
                board.update_piece(pos1, pos2)
                board.update_piece((0, 7), (3, 7))
                gd.white_castle_long = False
                print(gd.black_castle_long, gd.black_castle_short, gd.white_castle_long, gd.white_castle_short)
                return True
        elif pos1 == (4, 0):
            # black
            if pos2 == (6, 0) and pos2 in moves:
                # short
                board.update_piece(pos1, pos2)
                board.update_piece((7, 0), (5, 0))
                gd.black_castle_short = False
                return True
            elif pos2 == (2, 0) and pos2 in moves:
                # long
                board.update_piece(pos1, pos2)
                board.update_piece((0, 0), (3, 0))
                gd.black_castle_long = False
                return True
        return False


def check_not_attacked(position, pos_list, opp_color):
    for pos in pos_list:
        if pos_attacked(position, pos, opp_color):
            return False
    return True


def toggle_turn():
    if gd.turn == 'white':
        gd.turn = 'black'
    else:
        gd.turn = 'white'


def turn_square_active(board, pos):
    square = get_square(board, pos)
    square.set_active()


def turn_square_inactive(board, pos):
    square = get_square(board, pos)
    square.set_inactive()


def turn_all_squares_inactive(board):
    for col in board.data:
        for square in col:
            if square.is_active:
                square.set_inactive()


def remove_all_squares_hint(board):
    for col in board.data:
        for square in col:
            if square.is_hinted:
                square.toggle_hint()


def highlight_available_moves(board, pos1):
    piece = get_square(board, pos1).piece
    available_moves = piece.get_available_moves(board.position, pos1)
    moves = checkmate_filter(board.position, pos1, available_moves)
    for pos in moves:
        square = get_square(board, pos)
        if square:
            square.toggle_hint()


def is_checkmate(position):
    white_king_pos = get_king(position, 'w')
    black_king_pos = get_king(position, 'b')
    wc = pos_attacked(position, white_king_pos, 'b')
    bc = pos_attacked(position, black_king_pos, 'w')
    return wc, bc


def pos_attacked(position, pos, opp_color):
    for y in range(8):
        for x in range(8):
            piece = position[y][x]
            if piece[0] == opp_color:
                piece_class = pieces_dict[piece[1]]
                attacked = piece_class.get_available_moves(position, (x, y))
                if pos in attacked:
                    return True
    return False


def get_king(position, color):
    for y in range(8):
        for x in range(8):
            if position[y][x] == color + 'K':
                return x, y


def display_checkmate(board):
    wc, bc = is_checkmate(board.position)
    if wc:
        white_king_pos = get_king(board.position, 'w')
        white_king_square = get_square(board, white_king_pos)
        white_king_square.is_in_danger = True
    if bc:
        black_king_pos = get_king(board.position, 'b')
        white_king_square = get_square(board, black_king_pos)
        white_king_square.is_in_danger = True


def remove_checkmate(board):
    # removes red square for king
    for col in board.data:
        for square in col:
            square.is_in_danger = False


def checkmate_filter(position, pos, available_moves):
    # filtered out moves of pinned pieces
    filtered_moves = []
    color = position[pos[1]][pos[0]][0]
    for move in available_moves:
        temp_position = copy.deepcopy(position)
        update_piece(temp_position, pos, move)
        wc, bc = is_checkmate(temp_position)
        if (not wc and color == 'w') or (not bc and color == 'b'):
            filtered_moves.append(move)
    return filtered_moves


def update_piece(position, pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    piece = position[y1][x1]
    position[y2][x2] = piece
    position[y1][x1] = '--'


def display_game_over(screen):
    if gd.turn == 'black':
        color = 'White'
    else:
        color = 'Black'
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Game Over - ' + color + ' wins!', True, gd.black, gd.white)
    text_rect = text.get_rect()
    text_rect.center = (gd.board_length // 2, gd.board_length // 2)
    screen.blit(text, text_rect)


def check_game_over(board):
    # if no available moves exist then game is over
    all_available_moves = []
    current_turn = gd.turn
    for row in board.data:
        for sqr in row:
            piece = sqr.piece
            if piece and sqr.piece.color == current_turn[0]:
                moves = piece.get_available_moves(board.position, sqr.pos)
                moves = checkmate_filter(board.position, sqr.pos, moves)
                all_available_moves += moves
    if len(all_available_moves) == 0:
        gd.game_over = True


def update_castling_rights(piece, pos1):
    # Disables castling rights if king or rook is moved
    if piece.name == 'wK' and pos1 == (4, 7):
        gd.white_castle_short = False
        gd.white_castle_long = False
    elif piece.name == 'wK' and pos1 == (4, 0):
        gd.black_castle_short = False
        gd.black_castle_long = False
    if piece.name == 'wR':
        if pos1 == (0, 7):
            gd.white_castle_long = False
        elif pos1 == (7, 7):
            gd.white_castle_short = False
    elif piece.name == 'bR':
        if pos1 == (0, 0):
            gd.black_castle_long = False
        elif pos1 == (7, 0):
            gd.black_castle_short = False



