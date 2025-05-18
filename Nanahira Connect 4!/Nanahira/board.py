import pygame
from .constants import *
from .menu import *
import sys 

board_rows, board_cols = 6, 7
scaled_board_width = 800
scaled_board_height = 800
square_size = scaled_board_width // board_cols
board_x_centered = (CONFIG["window_width"] - scaled_board_width) // 2
board_y_centered = (CONFIG["window_height"] - scaled_board_height) // 0.65

white_piece = pygame.transform.scale(pygame.image.load('./Assets/WhitePiece.png'), (square_size, square_size))
black_piece = pygame.transform.scale(pygame.image.load('./Assets/BlackPiece.png'), (square_size, square_size))

def create_board():
    return [[0 for _ in range(board_cols)] for _ in range(board_rows)]

def draw_board(screen, board, bg):
    screen.blit(bg, (0, 0))
    board_main_color = (255, 230, 240)
    hole_color = (255, 192, 203)
    pygame.draw.rect(screen, board_main_color, (board_x_centered - 10, board_y_centered - 10, 20 + board_cols * square_size, 20 + board_rows * square_size), 7)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if board_y_centered - 100 <= mouse_y <= board_y_centered:
        col = get_column_from_click(mouse_x, mouse_y + 50)
        if col is not None and board[0][col] == 0:
            circle_radius = square_size // 2 - 8
            indicator_padding = 16
            indicator_surface = pygame.Surface(
                (square_size, circle_radius * 2 + indicator_padding),
                pygame.SRCALPHA
            )
            pygame.draw.circle(
                indicator_surface,
                (255, 255, 255, 150),
                (square_size // 2, circle_radius + indicator_padding // 2),
                circle_radius + 4
            )
            indicator_y = board_y_centered - (circle_radius * 2 + indicator_padding)
            screen.blit(indicator_surface, (board_x_centered + col * square_size, indicator_y - 20))

    for row in range(board_rows):
        for col in range(board_cols):
            cell_rect = pygame.Rect(board_x_centered + col * square_size, board_y_centered + row * square_size, square_size, square_size)
            pygame.draw.rect(screen, board_main_color, cell_rect.inflate(-2, -2), 2)
            pygame.draw.circle(screen, hole_color, cell_rect.center, square_size // 2 - 5)

            piece = board[row][col]
            if piece == 1:
                screen.blit(white_piece, (cell_rect.x + 5, cell_rect.y + 5))
            elif piece == 2:
                screen.blit(black_piece, (cell_rect.x + 5, cell_rect.y + 5))

    button_rect = pygame.Rect(BUTTON_X - 500, BUTTON_Y_START + 550, BUTTON_WIDTH // 3.2, BUTTON_HEIGHT)
    mouseX, mouseY = pygame.mouse.get_pos()
    is_hovered = button_rect.collidepoint(mouseX, mouseY)
    font = pygame.font.Font('./Assets/Starborn.ttf', 30)
    draw_button(screen, button_rect, "<--", font, is_hovered)

    return button_rect

def get_column_from_click(x, y):
    if y + 80 < board_y_centered - 50 or y > board_y_centered:
        return None
    if x < board_x_centered or x > board_x_centered + board_cols * square_size:
        return None
    return (x - board_x_centered) // square_size

def drop_piece(board, col, player):
    for row in reversed(range(board_rows)):
        if board[row][col] == 0:
            board[row][col] = player
            return row, col
    return None, None

def is_board_full(board):
    return all(cell != 0 for row in board for cell in row)

def check_win(board, player):
    for r in range(board_rows):
        for c in range(board_cols - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True
    for r in range(board_rows - 3):
        for c in range(board_cols):
            if all(board[r+i][c] == player for i in range(4)):
                return True
    for r in range(board_rows - 3):
        for c in range(board_cols - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True
            if all(board[r+3-i][c+i] == player for i in range(4)):
                return True
    return False

def handle_pvp_game(screen, bg):
    screen.fill((0, 0, 0))
    pygame.display.update()
    from .menu import animate_selection_menu_intro

    board = create_board()
    player = 1
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
                from .messages import display_message_image
                display_message_image(screen, image=joever_img)
                pygame.time.wait(600)
                pygame.quit()
                sys.exit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if button_rect.collidepoint(x, y):
                    pygame.mixer.Sound.play(click_sound)
                    animate_selection_menu_intro(screen, bg)
                    return

                col = get_column_from_click(x, y)
                if col is not None:
                    row, col = drop_piece(board, col, player)
                    pygame.mixer.Sound.play(piece_sound)
                    if row is not None:
                        draw_board(screen, board, bg)
                        pygame.display.update()
                        pygame.time.wait(150)

                        if check_win(board, player):
                            winner = player
                            running = False
                        elif is_board_full(board):
                            running = False
                        else:
                            player = 3 - player

    from .messages import display_message
    display_message(screen, f"Player {winner} wins!" if winner else "It's a tie!")
    return "TO_MENU"
