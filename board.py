import pygame
import game_data as gd
from pieces import Rook, Knight, Bishop, Queen, King, Pawn


class Board:

    def __init__(self, screen):
        self.screen = screen
        self.data = [[0] * 8 for i in range(8)]
        self.position = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]

    def set_up_board(self):
        # draws the square grid
        square_color = gd.light_color
        for y in range(8):
            square_color = self.toggle_color(square_color)
            for x in range(8):
                s_x = gd.square_length * x
                s_y = gd.square_length * y
                square = Square(str(x) + str(y), square_color, s_x, s_y)
                self.data[y][x] = square
                square_color = self.toggle_color(square_color)

    def place_pieces(self):
        # places pieces in initial position
        c = 0
        r = 0
        for col in self.data:
            r = 0
            for square in col:
                pos = self.position[c][r]
                if pos != '--':
                    color = pos[0]
                    piece = pos[1]
                    if piece == 'R':
                        new_piece = Rook(color)
                    elif piece == 'N':
                        new_piece = Knight(color)
                    elif piece == 'B':
                        new_piece = Bishop(color)
                    elif piece == 'Q':
                        new_piece = Queen(color)
                    elif piece == 'K':
                        new_piece = King(color)
                    elif piece == 'p':
                        new_piece = Pawn(color)
                    square.piece = new_piece
                r += 1
            c += 1

    @staticmethod
    def toggle_color(square_color):
        if square_color == gd.light_color:
            square_color = gd.dark_color
        elif square_color == gd.dark_color:
            square_color = gd.light_color
        return square_color

    def draw_board(self):
        for col in self.data:
            for square in col:
                self.draw_square(square)

    def draw_square(self, square):
        rect = pygame.Rect(square.x, square.y, gd.square_length, gd.square_length)
        pygame.draw.rect(self.screen, square.color, rect)
        if square.piece:
            self.screen.blit(square.piece.image, (square.x, square.y))
        if square.is_hinted and (not square.piece):
            square.draw_hint(self.screen)
        elif square.is_hinted and square.piece:
            square.draw_capture_hint(self.screen)

    def update_piece_position(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        piece = self.position[y1][x1]
        self.position[y2][x2] = piece
        self.position[y1][x1] = '--'

    def update_square_data(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        sqr_1_piece = self.data[y1][x1].piece
        self.data[y2][x2].piece = sqr_1_piece
        self.data[y1][x1].piece = None

    def update_piece(self, pos1, pos2):
        self.update_piece_position(pos1, pos2)
        self.update_square_data(pos1, pos2)

    def print(self):
        for col in self.position:
            print()
            for sqr in col:
                print(sqr, end=" ")
            print()
        print("")


class Square:
    hinted_image = pygame.image.load("E:/Projects/Chess/res/others/black_circle.png")
    hinted_capture_image = pygame.image.load("E:/Projects/Chess/res/others/black_ring.png")

    def __init__(self, id, color, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.default_color = color
        self.piece = None
        self.is_active = False
        self.is_hinted = False
        self.is_in_danger = False

    def __str__(self):
        return self.id

    @property
    def active_color(self):
        if self.default_color == gd.light_color:
            return gd.light_active_color
        elif self.default_color == gd.dark_color:
            return gd.dark_active_color

    @property
    def color(self):
        if self.is_in_danger:
            return gd.danger_color
        if self.is_active:
            return self.active_color
        else:
            return self.default_color

    def toggle_active(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True

    def toggle_hint(self):
        if self.is_hinted:
            self.is_hinted = False
        else:
            self.is_hinted = True

    def draw_hint(self, screen):
        x = self.x + gd.square_length // 2 + 1
        y = self.y + gd.square_length // 2 + 4
        center = (x, y)
        diameter = gd.square_length * 0.4
        self.hinted_image.set_alpha(60)
        image = pygame.transform.smoothscale(self.hinted_image, (diameter, diameter))
        rect = image.get_rect()
        rect.center = center
        screen.blit(image, rect)

    def draw_capture_hint(self, screen):
        x = self.x + gd.square_length // 2 + 1
        y = self.y + gd.square_length // 2 + 3
        center = (x, y)
        diameter = gd.square_length * 1.2
        self.hinted_capture_image.set_alpha(60)
        image = pygame.transform.smoothscale(self.hinted_capture_image, (diameter, diameter))
        rect = image.get_rect()
        rect.center = center
        screen.blit(image, rect)
