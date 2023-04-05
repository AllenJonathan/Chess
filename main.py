import time

import pygame
import game_data as gd
import game_functions as f
from board import Board
from move import Move

pygame.init()
pygame.display.set_caption("Chess")

gd.board_length = f.get_board_length()
gd.square_length = gd.board_length // 8

screen = pygame.display.set_mode((gd.board_length, gd.board_length))

board = Board(screen)
board.set_up_board()
board.place_pieces()
move_engine = Move(screen, board)

clock = pygame.time.Clock()

stop = False

while not stop:
    clock.tick(gd.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
    board.draw_board()
    move_engine.move()
    if gd.game_over:
        f.display_game_over(screen)
    pygame.display.flip()
