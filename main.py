import time

import pygame
import game_data as gd
import game_functions as f
from board import Board

pygame.init()
pygame.display.set_caption("Chess")

gd.board_length = f.get_board_length()
gd.square_length = gd.board_length // 8

screen = pygame.display.set_mode((gd.board_length, gd.board_length))

board = Board(screen)
board.set_up_board()
board.place_pieces()

moving = False
stop = False
initial_square = None
image = None

clock = pygame.time.Clock()


while not stop:
    clock.tick(gd.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
    board.draw_board()
    moving, initial_square, image = f.move(screen, board, moving, initial_square, image)
    pygame.display.flip()
