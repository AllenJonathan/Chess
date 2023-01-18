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


def move(screen, board, moving, pos1, temp_image):
    left_click = pygame.mouse.get_pressed()[0]
    if left_click:
        x1, y1 = pygame.mouse.get_pos()
        if not moving:
            # left click downpress
            turn_all_squares_inactive(board)
            remove_all_squares_hint(board)
            pos1 = get_pos(x1, y1)
            piece = get_square(board, pos1).piece
            if piece and gd.turn[0] == piece.color:
                turn_square_active(board, pos1)
                highlight_available_moves(board, pos1)
            else:
                return False, None, None
        # left click hold
        s_x1, s_y1 = pos1
        if board.data[s_y1][s_x1].piece:
            print('yes')
            if not temp_image:
                temp_image = board.data[s_y1][s_x1].piece.image.copy()
                temp_image.set_alpha(100)
            rect = temp_image.get_rect()
            rect.center = (x1, y1)
            screen.blit(temp_image, rect)
        return True, pos1, temp_image
    elif not left_click and moving:
        # left click released
        move_piece(board, pos1)
        return False, None, None
    return False, None, None


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


def move_piece(board, pos1):
    x2, y2 = pygame.mouse.get_pos()
    pos2 = get_pos(x2, y2)
    piece = get_square(board, pos1).piece
    if piece:
        available_moves = piece.get_available_moves(board.position, pos1)
        moves = checkmate_filter(board.position, pos1, available_moves)
        if pos2 in moves:
            # move made
            remove_checkmate(board)
            board.update_piece(pos1, pos2)
            toggle_turn()
            display_checkmate(board)
            turn_square_active(board, pos2)
            remove_all_squares_hint(board)
            gd.game_over = True


def turn_square_active(board, pos):
    square1 = get_square(board, pos)
    square1.toggle_active()


def turn_all_squares_inactive(board):
    for col in board.data:
        for square in col:
            if square.is_active:
                square.toggle_active()


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
    wc = checkmate(position, white_king_pos, 'b')
    bc = checkmate(position, black_king_pos, 'w')
    print(wc, bc)
    return wc, bc


def checkmate(position, king_pos, opp_color):
    for y in range(8):
        for x in range(8):
            piece = position[y][x]
            if piece[0] == opp_color:
                piece_class = pieces_dict[piece[1]]
                attacked = piece_class.get_available_moves(position, (x, y))
                if king_pos in attacked:
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


def toggle_turn():
    if gd.turn == 'white':
        gd.turn = 'black'
    else:
        gd.turn = 'white'


def remove_checkmate(board):
    for col in board.data:
        for square in col:
            square.is_in_danger = False


def checkmate_filter(position, pos, available_moves):
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
    if gd.turn == 'b':
        color = 'White'
    else:
        color = 'Black'
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Game Over - ' + color + ' wins!', True, gd.black, gd.white)
    text_rect = text.get_rect()
    text_rect.center = (gd.board_length // 2, gd.board_length // 2)
    screen.blit(text, text_rect)
