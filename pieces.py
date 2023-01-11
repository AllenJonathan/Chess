import pygame
import game_data as gd
import game_functions as f


class Piece(pygame.sprite.Sprite):

    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color  # 'b' if black and 'w' if white
        self.rect = self.image.get_rect()

    @property
    def opp_color(self):
        opp_color = 'w'
        if self.color == 'w':
            opp_color = 'b'
        return opp_color

    @staticmethod
    def get_image(name):
        img = pygame.image.load("E:/Projects/Chess/res/pieces/" + name + ".png")
        image = pygame.transform.smoothscale(img, (gd.square_length, gd.square_length))
        return image

    def get_bishop_moves(self, board, pos):
        available_moves = []
        diagonals = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        for diagonal in diagonals:
            x, y = pos
            x, y, square = self.update_bishop_square_pos(board, x, y, diagonal)
            # x += diagonal[0]
            # y += diagonal[1]
            # square = f.get_square(board, (x, y))
            self.add_capture_move(available_moves, x, y, square)
            while square and (not square.piece):
                available_moves.append((x, y))
                x, y, square = self.update_bishop_square_pos(board, x, y, diagonal)
                self.add_capture_move(available_moves, x, y, square)
        return available_moves

    @staticmethod
    def update_bishop_square_pos(board, x, y, diagonal):
        x += diagonal[0]
        y += diagonal[1]
        square = f.get_square(board, (x, y))
        return x, y, square

    def get_rook_moves(self, board, pos):
        moves_x = self.get_rook_axis_moves(board, pos, 'x')
        moves_y = self.get_rook_axis_moves(board, pos, 'y')
        available_moves = moves_x + moves_y
        return available_moves

    def get_rook_axis_moves(self, board, pos, axis):
        moves = []
        lines = (1, -1)
        for line in lines:
            x, y = pos
            x, y, square = self.increment_rook_axis_and_get_square(board, line, axis, x, y)
            self.add_capture_move(moves, x, y, square)
            while square and (not square.piece):
                moves.append((x, y))
                x, y, square = self.increment_rook_axis_and_get_square(board, line, axis, x, y)
                self.add_capture_move(moves, x, y, square)
        return moves

    def add_capture_move(self, arr, x, y, square):
        if square and square.piece:
            if square.piece.color != self.color:
                arr.append((x, y))

    @staticmethod
    def increment_rook_axis_and_get_square(board, line, axis, x, y):
        if axis == 'x':
            x += line
        else:
            y += line
        square = f.get_square(board, (x, y))
        return x, y, square


class Rook(Piece):

    def __init__(self, color):
        self.name = color + 'R'
        self.image = self.get_image(self.name)
        super().__init__(color)

    def get_available_moves(self, board, pos):
        return self.get_rook_moves(board, pos)


class Knight(Piece):

    def __init__(self, color):
        self.name = color + 'N'
        self.image = self.get_image(self.name)
        super().__init__(color)

    def get_available_moves(self, board, pos):
        x, y = pos
        available_moves = []
        possible_moves = [
            (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2),
            (x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
        ]
        for n in range(len(possible_moves)):
            move = possible_moves[n]
            square = f.get_square(board, move)
            if square:
                if square.piece:
                    if square.piece.color == self.color:
                        possible_moves[n] = 0
            else:
                possible_moves[n] = 0
        for move in possible_moves:
            if move != 0:
                available_moves.append(move)
        return available_moves


class Bishop(Piece):

    def __init__(self, color):
        self.name = color + 'B'
        self.image = self.get_image(self.name)
        super().__init__(color)

    def get_available_moves(self, board, pos):
        return self.get_bishop_moves(board, pos)


class Queen(Piece):

    def __init__(self, color):
        self.name = color + 'Q'
        self.image = self.get_image(self.name)
        super().__init__(color)

    def get_available_moves(self, board, pos):
        rook_moves = self.get_rook_moves(board, pos)
        bishop_moves = self.get_bishop_moves(board, pos)
        queen_moves = rook_moves + bishop_moves
        return queen_moves


class King(Piece):

    def __init__(self, color):
        self.name = color + 'K'
        self.image = self.get_image(self.name)
        super().__init__(color)
        self.is_checkmated = False

    def get_available_moves(self, board, pos):
        available_moves = []
        x, y = pos
        possible_moves = [(x+1, y+1), (x, y+1), (x-1, y+1), (x+1, y), (x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1)]
        for move in possible_moves:
            print(move)
            square = f.get_square(board, move)
            if square:
                if not square.piece:
                    available_moves.append(move)
                elif square.piece.color != self.color:
                    available_moves.append(move)
        return available_moves


class Pawn(Piece):

    def __init__(self, color):
        self.name = color + 'p'
        self.image = self.get_image(self.name)
        super().__init__(color)

    def get_available_moves(self, board, pos):
        available_moves = []
        x, y = pos
        if self.color == 'w':
            a1 = (x, y - 1)
            a2 = (x, y - 2)
            b1 = (x - 1, y - 1)
            b2 = (x + 1, y - 1)
            self.get_moves(board, available_moves, 'w', y, a1, a2, b1, b2)
        elif self.color == 'b':
            a1 = (x, y + 1)
            a2 = (x, y + 2)
            b1 = (x - 1, y + 1)
            b2 = (x + 1, y + 1)
            self.get_moves(board, available_moves, 'b', y, a1, a2, b1, b2)
        return available_moves

    @staticmethod
    def get_moves(board, available_moves, color, y, a1, a2, b1, b2):
        opp_color = 'w'
        if color == 'w':
            opp_color = 'b'
        ahead_one = f.get_square(board, a1).piece
        ahead_two = f.get_square(board, a2).piece
        if not ahead_one:
            available_moves.append(a1)
        if y == 6 and color == 'w' and (not ahead_two):
            available_moves.append(a2)
        if y == 1 and color == 'b' and (not ahead_two):
            available_moves.append(a2)
        left = b1
        right = b2
        left_square = f.get_square(board, left)
        right_square = f.get_square(board, right)
        if left_square and left_square.piece:
            if left_square.piece.color == opp_color:
                available_moves.append(left)
        if right_square and right_square.piece:
            if right_square.piece.color == opp_color:
                available_moves.append(right)
