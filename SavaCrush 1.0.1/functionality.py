import pygame as pg
from random import choice, shuffle
from typing import Any
from assets import *

pg.init()

def draw_board() -> None:
    """draws the main board: background of the board and the outline"""
    pg.draw.rect(SCREEN, colors["field"], pg.Rect(0, 0, GEM_SCALE * GAPS,
                 GEM_SCALE * GAPS))
    for i in range(GAPS + 1):
        pg.draw.line(SCREEN, colors["border"], (GEM_SCALE * i, 0), 
                     (GEM_SCALE * i, GAPS * GEM_SCALE))
        pg.draw.line(SCREEN, colors["border"], (0, GEM_SCALE * i),
                     (GAPS * GEM_SCALE, GEM_SCALE * i))


def generate_gems(board: list[int | None]) -> None:
    """spawns gems from the top row"""
    for idx in range(GAPS):
        if board[idx] is None:
            board[idx] = choice(generation_subjects)


def gravity(board: list[int | None]) -> None:
    for idx, gem in enumerate(board[:-GAPS]):
        if gem is not None and board[idx + GAPS] is None:
            board[idx], board[idx + GAPS] = \
                board[idx + GAPS], board[idx]


def draw_gems(board: list[int | None], 
              coordinates: tuple[tuple[int, int], ...]) -> None:
    """draws the gems + adds mechanics for 
    them to fall and fill the whole field"""

    for coord, number in zip(coordinates, board):
        if number is not None:
            if number not in {9, 10, 11}:
                SCREEN.blit(numbers_to_images[number], (coord[1] * GEM_SCALE,
                            coord[0] * GEM_SCALE))
            else:
                SCREEN.blit(numbers_to_images[number].image, 
                            (coord[1] * GEM_SCALE,
                            coord[0] * GEM_SCALE))


def destroy_gems(board: list[int | None], 
                 coordinates: tuple[tuple[int, int], ...]=coords) -> None:
    """check for matches and if there are any,
    removes the gems in the matches"""
    
    for match_length in range(5, 2, -1):        # rows check
        for idx in (index for index in range(len(board)) if (index + 1) % GAPS \
                    not in ({0, GAPS - 1, GAPS - 2, GAPS - 3} if \
                            match_length == 5 else {0, GAPS - 1, GAPS - 2} \
                                if match_length == 4 else {0, GAPS - 1})):
            if (all(board[idx] == board[idx + i] for i in range(match_length))\
                and all(coordinates[idx][0] == coordinates[idx + j][0] 
                    for j in range(match_length))) and board[idx] is not None:
                for i in range(match_length):
                    board[idx + i] = None
                if match_length == 4:
                    board[idx + 1] = 9
                elif match_length == 5:
                    board[idx + 2] = 11

    for match_length in range(5, 2, -1):        # columns check
        for idx in range(len(board) - GAPS * (match_length - 1)):
            if all(board[idx] == board[idx + GAPS * i] 
                   for i in range(match_length)) and board[idx] is not None:
                for i in range(match_length):
                    board[idx + GAPS * i] = None
                if match_length == 4:
                    board[idx + GAPS] = 10
                elif match_length == 5:
                    board[idx + GAPS * 2] = 11


def legit_swap(board: list[int | None], idx1: int, idx2: int, 
               coordinates: tuple[tuple[int, int], ...]=coords) -> bool:
    """checks if the player swaps the gems legitimately"""

    pos1: tuple[int, int] = coordinates[idx1]
    pos2: tuple[int, int] = coordinates[idx2]

    if ((pos1[0] - pos2[0] == 1 and pos1[1] == pos2[1]) or \
            (pos2[0] - pos1[0] == 1 and pos1[1] == pos2[1]) or \
                (pos1[1] - pos2[1] == 1 and pos1[0] == pos2[0]) \
                    or (pos2[1] - pos1[1] == 1 and pos1[0] == pos2[0])):
        if board[idx1] in {9, 10, 11} or \
        board[idx2] in {9, 10, 11}:
            return True



        # temporary board for simulating swaps
        temp_board_scheme: list[int | None] = board.copy()
            
        temp_board_scheme[idx1], temp_board_scheme[idx2] = \
            temp_board_scheme[idx2], temp_board_scheme[idx1]
        destroy_gems(temp_board_scheme, coordinates)
        gems_destroyed: int = temp_board_scheme.count(None)

        if gems_destroyed < 1:
            return False

        return True
        
    return False
                       

def check_matches(board: list[int | None], 
                  coordinates: tuple[tuple[int, int], ...]) -> bool:
    """algorithm for checking the field for possible moves,
    if there are no such, the board is shuffled in the main loop"""
    temp_board_scheme: list[pg.Surface | None] = board.copy()
    for idx in range(len(temp_board_scheme) - GAPS):
        temp_board_scheme[idx], temp_board_scheme[idx + GAPS] = \
        temp_board_scheme[idx + GAPS], temp_board_scheme[idx]
        destroy_gems(temp_board_scheme, coordinates)
        if not all(temp_board_scheme):
            return True

        temp_board_scheme[idx], temp_board_scheme[idx + GAPS] = \
        temp_board_scheme[idx + GAPS], temp_board_scheme[idx]

    for idx, object in enumerate(temp_board_scheme[:-1]):
        if object in {9, 10, 11}:
            return True
        if coordinates[idx][0] == coordinates[idx + 1][0]:
            temp_board_scheme[idx], temp_board_scheme[idx + 1] = \
            temp_board_scheme[idx + 1], temp_board_scheme[idx]
            destroy_gems(temp_board_scheme)
            if not all(temp_board_scheme):
                return True

            temp_board_scheme[idx], temp_board_scheme[idx + 1] = \
            temp_board_scheme[idx + 1], temp_board_scheme[idx]
        
    return False