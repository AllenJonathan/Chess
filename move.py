import pygame
import game_functions as f
import game_data as gd


class Move:
    screen = None
    board = None
    moving = False
    pos = None
    clicked_move = False
    move_img = None
    active_pos = []

    @classmethod
    def __init__(cls, screen, board):
        cls.screen = screen
        cls.board = board

    @classmethod
    def move(cls):
        left_click = pygame.mouse.get_pressed()[0]
        if left_click:
            x1, y1 = pygame.mouse.get_pos()

            if not cls.moving:
                # clicked
                cls.move_clicked(x1, y1)

            elif cls.moving:
                # hold
                cls.move_hold(x1, y1)

        elif not left_click and cls.moving:
            # released
            cls.move_released()

    @classmethod
    def move_piece(cls, pos1, pos2):
        piece = f.get_square(cls.board, pos1).piece
        if piece and piece.color == gd.turn[0]:
            available_moves = piece.get_available_moves(cls.board.position, pos1)
            moves = f.checkmate_filter(cls.board.position, pos1, available_moves)
            if pos2 in moves:
                # move made
                f.remove_checkmate(cls.board)
                if f.check_and_castle(cls.board, piece, pos1, pos2, moves):
                    pass
                elif f.check_and_en_passant(cls.board, piece, pos1, pos2):
                    print('en passant')
                    pass
                else:
                    f.update_castling_rights(piece, pos1)
                    cls.board.update_piece(pos1, pos2)
                f.update_en_passant(piece, pos1, pos2)
                # check for pawn promotion
                if piece.name == 'wp' and pos2[1] == 0:
                    cls.board.position[pos2[1]][pos2[0]] = 'wQ'
                    cls.board.place_pieces()
                    print(cls.board.position)
                elif piece.name == 'bp' and pos2[1] == 7:
                    cls.board.position[pos2[1]][pos2[0]] = 'bQ'
                    cls.board.place_pieces()
                # changes after move
                cls.wrap_up_after_move(pos1, pos2)

    @classmethod
    def move_clicked(cls, x1, y1):

        cls.clicked_move = False

        # pos0 -> previous position clicked
        prev_pos = cls.pos

        # pos1 -> current position clicked
        cls.pos = f.get_pos(x1, y1)
        curr_square = f.get_square(cls.board, cls.pos)
        curr_piece = curr_square.piece

        # click move
        if prev_pos and curr_square and curr_square.is_hinted:
            if prev_pos != cls.pos:
                cls.move_piece(prev_pos, cls.pos)
                cls.clicked_move = True

        # set square highlighting
        f.turn_all_squares_inactive(cls.board)
        f.remove_all_squares_hint(cls.board)
        for pos in cls.active_pos:
            f.turn_square_active(cls.board, pos)

        # select piece and show moves
        if not cls.clicked_move and curr_piece and gd.turn[0] == curr_piece.color:
            f.turn_square_active(cls.board, cls.pos)
            f.highlight_available_moves(cls.board, cls.pos)

        # started to hold
        cls.moving = True

    @classmethod
    def move_hold(cls, x1, y1):
        s_x1, s_y1 = cls.pos
        piece = cls.board.data[s_y1][s_x1].piece
        if piece and piece.color == gd.turn[0]:
            if not cls.move_img:
                cls.move_img = cls.board.data[s_y1][s_x1].piece.image.copy()
                cls.move_img.set_alpha(100)
            rect = cls.move_img.get_rect()
            rect.center = (x1, y1)
            cls.screen.blit(cls.move_img, rect)

    @classmethod
    def move_released(cls):
        x2, y2 = pygame.mouse.get_pos()
        pos2 = f.get_pos(x2, y2)
        cls.move_piece(cls.pos, pos2)
        cls.moving = False
        cls.move_img = False

    @classmethod
    def wrap_up_after_move(cls, pos1, pos2):
        f.toggle_turn()
        f.display_checkmate(cls.board)

        # highlight squares
        for pos in cls.active_pos:
            f.turn_square_inactive(cls.board, pos)
        f.turn_square_active(cls.board, pos2)
        f.turn_square_active(cls.board, pos1)
        f.remove_all_squares_hint(cls.board)
        cls.active_pos = [pos1, pos2]
        f.check_game_over(cls.board)

