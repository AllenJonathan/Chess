import pygame
import game_data as gd


def get_board_length():
    native_res = pygame.display.Info()
    side_length = (min(native_res.current_h, native_res.current_w) - 100)
    side = side_length - (side_length % 8)
    return side


def move(screen, board, moving, pos1):
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
                return False, None
        # left click hold
        display_temp_image(screen, board, pos1, x1, y1)
        return True, pos1

    elif not left_click and moving:
        # left click released
        move_piece(board, pos1)
        return False, None
    return False, None


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


def display_temp_image(screen, board, pos1, x1, y1):
    s_x1, s_y1 = pos1
    if board.data[s_y1][s_x1].piece:
        temp_image = board.data[s_y1][s_x1].piece.image.copy()
        temp_image.set_alpha(100)
        rect = temp_image.get_rect()
        rect.center = (x1, y1)
        screen.blit(temp_image, rect)


def move_piece(board, pos1):
    x2, y2 = pygame.mouse.get_pos()
    pos2 = get_pos(x2, y2)
    piece = get_square(board, pos1).piece
    if piece:
        am = piece.get_available_moves(board, pos1)
        if pos2 in am:
            board.update_board(pos1, pos2)
            toggle_turn()
            display_checkmate(board)
            turn_square_active(board, pos2)
            remove_all_squares_hint(board)


def turn_square_active(board, pos):
    square1 = get_square(board, pos)
    square1.toggle_active()


def turn_all_squares_inactive(board):
    for col in board.data:
        for square in col:
            if square.is_active:
                square.toggle_active()
            if square.is_in_danger:
                square.is_in_danger = False


def remove_all_squares_hint(board):
    for col in board.data:
        for square in col:
            if square.is_hinted:
                square.toggle_hint()


def highlight_available_moves(board, pos1):
    piece = get_square(board, pos1).piece
    moves = piece.get_available_moves(board, pos1)
    for pos in moves:
        square = get_square(board, pos)
        if square:
            square.toggle_hint()


def is_checkmate(board):
    ws = get_king(board, 'w')
    white_king_pos = get_pos(ws.x, ws.y)
    bs = get_king(board, 'b')
    black_king_pos = get_pos(bs.x, bs.y)
    wc = checkmate(board, white_king_pos, 'b')
    bc = checkmate(board, black_king_pos, 'w')
    return wc, bc


def checkmate(board, pos, opp_color):
    for col in board.data:
        for square in col:
            if square and square.piece and square.piece.color == opp_color:
                current_pos = get_pos(square.x, square.y)
                attacked = square.piece.get_available_moves(board, current_pos)
                if pos in attacked:
                    return True
    return False


def get_king(board, color):
    for col in board.data:
        for square in col:
            if square and square.piece and square.piece.name == color + 'K':
                return square


def display_checkmate(board):
    wc, bc = is_checkmate(board)
    print(wc, bc)
    if wc:
        white_king_square = get_king(board, 'w')
        white_king_square.is_in_danger = True
    if bc:
        white_king_square = get_king(board, 'b')
        white_king_square.is_in_danger = True
        board.print_data()


def toggle_turn():
    if gd.turn == 'white':
        gd.turn = 'black'
    else:
        gd.turn = 'white'
