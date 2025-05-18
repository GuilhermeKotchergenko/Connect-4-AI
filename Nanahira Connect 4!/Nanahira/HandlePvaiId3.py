import pygame
import random
import pandas as pd
from .constants import *
from .messages import display_message, display_message_image
from .board import *
from .menu import animate_selection_menu_intro
from .ai_id3 import State, NUM_ROWS, NUM_COLS


def handle_player_vs_ai_game(screen, bg, player_piece, ai_piece, ai_func):
    screen.fill((0, 0, 0))
    pygame.display.update()
    from .menu import animate_selection_menu_intro

    board = create_board()
    current_player = 1
    winner = None
    clock = pygame.time.Clock()

    piece_sound = pygame.mixer.Sound('./Nanahira/piece.ogg')

    font = pygame.font.Font('./Assets/Starborn.ttf', 30)
    frames = 30
    for frame in range(frames):
        screen.blit(bg, (0, 0))
        progress = frame / frames

        board_offset = int((1 - progress) * 200)
        back_offset = int((1 - progress) * 300)

        pygame.draw.rect(screen, (255, 230, 240), (board_x_centered - 10, board_y_centered - 10 - board_offset,
                                                  20 + board_cols * square_size, 20 + board_rows * square_size), 7)

        for row in range(board_rows):
            for col in range(board_cols):
                cell_rect = pygame.Rect(board_x_centered + col * square_size,
                                        board_y_centered + row * square_size - board_offset,
                                        square_size, square_size)
                pygame.draw.rect(screen, (255, 230, 240), cell_rect.inflate(-2, -2), 2)
                pygame.draw.circle(screen, (250, 192, 203), cell_rect.center, square_size // 2 - 5)

        button_rect = pygame.Rect(BUTTON_X - 500 + back_offset, BUTTON_Y_START + 550, BUTTON_WIDTH // 3.2, BUTTON_HEIGHT)
        mouseX, mouseY = pygame.mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouseX, mouseY)
        pygame.draw.rect(screen, (255, 222, 213) if is_hovered else (250, 192, 203), button_rect, 0, 30)
        text = font.render("<--", True, white)
        screen.blit(text, text.get_rect(center=button_rect.center))

        pygame.display.update()
        clock.tick(60)

    running = True
    while running:
        button_rect = draw_board(screen, board, bg)
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_message_image(screen, image=joever_img)
                pygame.time.wait(600)
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_player == player_piece:
                x, y = pygame.mouse.get_pos()
                if button_rect.collidepoint(x, y):
                    pygame.mixer.Sound.play(click_sound)
                    animate_selection_menu_intro(screen, bg)
                    return

                col = get_column_from_click(x, y)
                if col is not None and board[0][col] == 0:
                    row, col = drop_piece(board, col, player_piece)
                    pygame.mixer.Sound.play(piece_sound)
                    if check_win(board, player_piece):
                        winner = player_piece
                        running = False
                    elif is_board_full(board):
                        running = False
                    else:
                        current_player = ai_piece

        draw_board(screen, board, bg)
        pygame.display.update()

        if current_player == ai_piece and running:
            pygame.time.wait(350)
            class DummyGame:
                def __init__(self, board, player):
                    self.state = self.convert_board_to_state(board, player)

                def convert_board_to_state(self, board, player):
                    state = State()
                    state.board = [row[:] for row in board]  # Deep copy board
                    state.player = player
                    state.column_heights = [
                        next((r for r in range(len(board)) if board[r][c] != 0), NUM_ROWS) - 1
                        for c in range(NUM_COLS)
                    ]
                    state.available_moves = [c for c in range(NUM_COLS) if board[0][c] == 0]
                    state.update_winner()
                    return state

            dummy_game = DummyGame(board, ai_piece)
            col = ai_func(dummy_game)

            from .match_logger import log_match_step

            # Log the move
            ai_type_str = getattr(ai_func, '__name__', 'unknown_ai')
            log_match_step(dummy_game.state, ai_piece, ai_type_str, col, winner=winner)

            if col is not None and board[0][col] == 0:
                row, col = drop_piece(board, col, ai_piece)
                pygame.mixer.Sound.play(piece_sound)
                if check_win(board, ai_piece):
                    winner = ai_piece
                    running = False
                elif is_board_full(board):
                    running = False
                else:
                    current_player = player_piece 
    if winner:
        ai_type_str = getattr(ai_func, '__name__', 'unknown_ai')
        log_match_step(dummy_game.state, ai_piece, ai_type_str, col, winner=winner)

    draw_board(screen, board, bg)
    pygame.display.update()
    pygame.time.wait(20)
    display_message(screen, f"Player {winner} wins!" if winner else "It's a tie!")
    return "TO_MENU"
