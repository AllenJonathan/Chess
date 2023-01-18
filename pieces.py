import pygame
import game_data as gd


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

    @staticmethod
    def filter_available_moves(available_moves):
        filtered_moves = []
        for move in available_moves:
            x = move[0]
            y = move[1]
            if -1 < x < 8 and -1 < y < 8:
                filtered_moves.append(move)
        return filtered_moves


class Rook(Piece):

    def __init__(self, color):
        self.name = color + 'R'
        self.image = self.get_image(self.name)
        super().__init__(color)

    @staticmethod
    def get_available_moves(position, pos):
        color = position[pos[1]][pos[0]][0]
        moves_x = Rook.get_rook_axis_moves(position, pos, 'x', color)
        moves_y = Rook.get_rook_axis_moves(position, pos, 'y', color)
        available_moves = moves_x + moves_y
        return available_moves

    @staticmethod
    def get_rook_axis_moves(position, pos, axis, color):
        moves = []
        lines = (1, -1)
        for line in lines:
            x, y = pos
            piece = '--'
            while piece == '--':
                if (x, y) != pos:
                    moves.append((x, y))
                x, y = Rook.increment_rook_axis(line, axis, x, y)
                if -1 < x < 8 and -1 < y < 8:
                    piece = position[y][x]
                else:
                    break
            if -1 < x < 8 and -1 < y < 8 and position[y][x][0] != color:
                moves.append((x, y))
        return moves

    @staticmethod
    def increment_rook_axis(line, axis, x, y):
        if axis == 'x':
            x += line
        else:
            y += line
        return x, y


class Knight(Piece):

    def __init__(self, color):
        self.name = color + 'N'
        self.image = self.get_image(self.name)
        super().__init__(color)

    @staticmethod
    def get_available_moves(position, pos):
        x, y = pos
        color = position[y][x][0]
        available_moves = []
        possible_moves = [
            (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2),
            (x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
        ]
        possible_moves = Piece.filter_available_moves(possible_moves)
        for n in range(len(possible_moves)):
            move = possible_moves[n]
            x = move[0]
            y = move[1]
            if position[y][x] == '--' or position[y][x][0] != color:
                available_moves.append(move)
        return available_moves


class Bishop(Piece):

    def __init__(self, color):
        self.name = color + 'B'
        self.image = self.get_image(self.name)
        super().__init__(color)

    @staticmethod
    def get_available_moves(position, pos):
        color = position[pos[1]][pos[0]][0]
        available_moves = []
        diagonals = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        for diagonal in diagonals:
            x, y = pos
            piece = '--'
            while piece == '--':
                if (x, y) != pos:
                    available_moves.append((x, y))
                x += diagonal[0]
                y += diagonal[1]
                if -1 < x < 8 and -1 < y < 8:
                    piece = position[y][x]
                else:
                    break
            if -1 < x < 8 and -1 < y < 8 and position[y][x][0] != color:
                available_moves.append((x, y))
        return available_moves


class Queen(Piece):

    def __init__(self, color):
        self.name = color + 'Q'
        self.image = self.get_image(self.name)
        super().__init__(color)

    @staticmethod
    def get_available_moves(position, pos):
        rook_moves = Rook.get_available_moves(position, pos)
        bishop_moves = Bishop.get_available_moves(position, pos)
        queen_moves = rook_moves + bishop_moves
        return queen_moves


class King(Piece):

    def __init__(self, color):
        self.name = color + 'K'
        self.image = self.get_image(self.name)
        super().__init__(color)
        self.is_checkmated = False

    @staticmethod
    def get_available_moves(position, pos):
        available_moves = []
        x, y = pos
        color = position[y][x][0]
        possible_moves = [(x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x + 1, y), (x - 1, y), (x - 1, y - 1),
                          (x, y - 1), (x + 1, y - 1)]
        possible_moves = Piece.filter_available_moves(possible_moves)
        for n in range(len(possible_moves)):
            move = possible_moves[n]
            x = move[0]
            y = move[1]
            if position[y][x] == '--' or position[y][x][0] != color:
                available_moves.append(move)
        return available_moves


class Pawn(Piece):

    def __init__(self, color):
        self.name = color + 'p'
        self.image = self.get_image(self.name)
        super().__init__(color)

    @staticmethod
    def get_available_moves(position, pos):
        available_moves = []
        x, y = pos
        color = position[y][x][0]
        if color == 'w':
            a1 = (x, y - 1)
            a2 = (x, y - 2)
            b1 = (x - 1, y - 1)
            b2 = (x + 1, y - 1)
            Pawn.get_moves(position, available_moves, 'w', y, a1, a2, b1, b2)
        elif color == 'b':
            a1 = (x, y + 1)
            a2 = (x, y + 2)
            b1 = (x - 1, y + 1)
            b2 = (x + 1, y + 1)
            Pawn.get_moves(position, available_moves, 'b', y, a1, a2, b1, b2)
        return available_moves

    @staticmethod
    def get_moves(position, available_moves, color, y, a1, a2, b1, b2):
        opp_color = 'w'
        if color == 'w':
            opp_color = 'b'
        a1x, a1y = a1[0], a1[1]
        a2x, a2y = a2[0], a2[1]
        if position[a1y][a1x] == '--':
            available_moves.append(a1)
        if position[a2y][a2x] == '--' and color == 'w' and y == 6:
            available_moves.append(a2)
        if position[a2y][a2x] == '--' and color == 'b' and y == 1:
            available_moves.append(a2)
        b1x, b1y = b1[0], b1[1]
        b2x, b2y = b2[0], b2[1]
        if -1 < b1x < 8 and -1 < b1y < 8 and position[b1y][b1x][0] == opp_color:
            available_moves.append(b1)
        if -1 < b2x < 8 and -1 < b2y < 8 and position[b2y][b2x][0] == opp_color:
            available_moves.append(b2)
