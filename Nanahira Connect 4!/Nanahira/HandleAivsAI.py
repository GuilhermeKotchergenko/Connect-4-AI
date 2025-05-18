import pygame
from .board import create_board, draw_board, drop_piece, is_board_full, check_win, board_x_centered, board_y_centered, board_cols, board_rows, square_size, BUTTON_X, BUTTON_Y_START, BUTTON_WIDTH, BUTTON_HEIGHT
from .messages import display_message, display_message_image
from .menu import animate_selection_menu_intro
from .match_logger import log_match_step
from .ai_id3 import State
import time

class DummyGame:
    def __init__(self, board, player):
        self.state = State()
        self.state.board = [row[:] for row in board]
        self.state.player = player
        self.state.column_heights = [
            next((r for r in range(len(board)) if board[r][c] != 0), 6) - 1
            for c in range(7)
        ]
        self.state.available_moves = [c for c in range(7) if board[0][c] == 0]
        self.state.update_winner()

def make_dummy_game(board, player):
    return DummyGame(board, player)

def run_headless_simulations(ai_white, ai_black, runs):
    results = {1: 0, 2: 0, 0: 0}
    for i in range(runs):
        board = create_board()
        current = 1
        ai_map = {1: ai_white, 2: ai_black}
        winner = None
        while True:
            dummy = make_dummy_game(board, current)
            col = ai_map[current](dummy)
            if board[0][col] != 0:
                winner = 3 - current
                break
            row, col = drop_piece(board, col, current)
            dummy = make_dummy_game(board, current)
            ai_type = getattr(ai_map[current], '__name__', 'ai')
            log_match_step(dummy.state, current, ai_type, col)
            if check_win(board, current):
                winner = current
                break
            elif is_board_full(board):
                winner = 0
                break
            current = 3 - current
        results[winner] += 1
    print("Headless simulation results:")
    print(f"White wins: {results[1]}")
    print(f"Black wins: {results[2]}")
    print(f"Ties:       {results[0]}")

def handle_ai_vs_ai_game(screen, bg, ai_func1, ai_func2, label1, label2):
    board = create_board()
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
        text = font.render("<--", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=button_rect.center))

        pygame.display.update()
        clock.tick(60)

    current_player = 1
    ai_map = {1: ai_func1, 2: ai_func2}
    label_map = {1: label1, 2: label2}
    running = True
    winner = None

    while running:
        button_rect = draw_board(screen, board, bg)
        pygame.display.update()
        clock.tick(60)

        delay = 0
        while delay < 300:
            delay += clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display_message_image(screen, image=pygame.image.load('./Assets/joever.png'))
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        animate_selection_menu_intro(screen, bg)
                        return "TO_MENU"

        dummy = DummyGame(board, current_player)
        col = ai_map[current_player](dummy)

        if board[0][col] != 0:
            winner = 3 - current_player
            break

        row, col = drop_piece(board, col, current_player)
        piece_sound.play()

        dummy = DummyGame(board, current_player)
        ai_type_str = getattr(ai_map[current_player], '__name__', label_map[current_player])
        log_match_step(dummy.state, current_player, ai_type_str, col)

        if check_win(board, current_player):
            winner = current_player
            running = False
        elif is_board_full(board):
            winner = 0
            running = False
        else:
            current_player = 3 - current_player

    draw_board(screen, board, bg)
    pygame.display.update()
    pygame.time.wait(500)

    if winner == 0:
        display_message(screen, "It's a tie!")
    else:
        display_message(screen, f"{label_map[winner].capitalize()} (Player {winner}) wins!")

    return "TO_MENU"
