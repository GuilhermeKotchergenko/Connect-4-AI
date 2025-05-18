import pygame
from .constants import *
from .menu import draw_button
from .messages import *

Nanahira = pygame.image.load('./Assets/Nanahira.png')
click_sound = pygame.mixer.Sound('./Nanahira/click.wav')
joever_img = pygame.image.load('./Assets/joever.png')

def draw_mcts_configuration_menu(screen, bg):
    """
    Menu to select player piece color and MCTS type.
    Returns tuple (player_color, mcts_type) or None if BACK selected.
    """
    clock = pygame.time.Clock()
    font_menu = pygame.font.Font('./Assets/Starborn.ttf', 40)
    selected_color = None
    selected_type = None
    running = True

    while running:
        screen.blit(bg, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Piece color selection
        white_btn = pygame.Rect(BUTTON_X, BUTTON_Y_START, BUTTON_WIDTH // 2 - 10, BUTTON_HEIGHT)
        black_btn = pygame.Rect(BUTTON_X + BUTTON_WIDTH // 2 + 10, BUTTON_Y_START, BUTTON_WIDTH // 2 - 10, BUTTON_HEIGHT)
        is_white_hovered = white_btn.collidepoint(mouse_x, mouse_y)
        is_black_hovered = black_btn.collidepoint(mouse_x, mouse_y)
        white_selected = selected_color == 1
        black_selected = selected_color == 2
        draw_button(screen, white_btn, "White", font_menu, is_white_hovered or white_selected)
        draw_button(screen, black_btn, "Black", font_menu, is_black_hovered or black_selected)

        # MCTS type options
        normal_btn = pygame.Rect(BUTTON_X, BUTTON_Y_START + 180, BUTTON_WIDTH, BUTTON_HEIGHT)
        parallel_btn = pygame.Rect(BUTTON_X, BUTTON_Y_START + 180 + BUTTON_HEIGHT + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
        is_normal_hovered = normal_btn.collidepoint(mouse_x, mouse_y)
        is_parallel_hovered = parallel_btn.collidepoint(mouse_x, mouse_y)
        draw_button(screen, normal_btn, "Normal MCTS", font_menu, is_normal_hovered or selected_type == "normal")
        draw_button(screen, parallel_btn, "Parallel MCTS", font_menu, is_parallel_hovered or selected_type == "parallel")

        # Back button
        back_btn = pygame.Rect(BUTTON_X - 150, BUTTON_Y_START + 500, BUTTON_WIDTH // 3.2, BUTTON_HEIGHT)
        is_back_hovered = back_btn.collidepoint(mouse_x, mouse_y)
        draw_button(screen, back_btn, "<--", font_menu, is_back_hovered)

        character_y = (CONFIG["window_height"] - Nanahira.get_height()) // 2
        screen.blit(Nanahira, (5, character_y))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_message_image(screen, image=joever_img)
                pygame.time.wait(600)
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_white_hovered:
                    click_sound.play()
                    selected_color = 1
                elif is_black_hovered:
                    click_sound.play()
                    selected_color = 2
                elif is_normal_hovered:
                    click_sound.play()
                    selected_type = "normal"
                elif is_parallel_hovered:
                    click_sound.play()
                    selected_type = "parallel"
                elif is_back_hovered:
                    click_sound.play()
                    return None

                if selected_color and selected_type:
                    return (selected_color, selected_type)

def draw_mcts_epoch_menu(screen, bg):
    """Menu to select MCTS epoch depth."""
    clock = pygame.time.Clock()
    font_menu = pygame.font.Font('./Assets/Starborn.ttf', 40)
    running = True

    options = [
        ("Quick", 100),
        ("Standard", 500),
        ("Deep", 2000)
    ]

    while running:
        screen.blit(bg, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for i, (label, value) in enumerate(options):
            btn_rect = pygame.Rect(BUTTON_X, 50 + BUTTON_Y_START + i * (BUTTON_HEIGHT + BUTTON_GAP + 10), BUTTON_WIDTH, BUTTON_HEIGHT)
            is_hovered = btn_rect.collidepoint(mouse_x, mouse_y)
            draw_button(screen, btn_rect, label, font_menu, is_hovered)

        back_btn = pygame.Rect(BUTTON_X - 150, BUTTON_Y_START + 3 * (BUTTON_HEIGHT + BUTTON_GAP), BUTTON_WIDTH // 3.2, BUTTON_HEIGHT)
        is_back_hovered = back_btn.collidepoint(mouse_x, mouse_y)
        draw_button(screen, back_btn, "<--", font_menu, is_back_hovered)

        character_y = (CONFIG["window_height"] - Nanahira.get_height()) // 2
        screen.blit(Nanahira, (5, character_y))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_message_image(screen, image=joever_img)
                pygame.time.wait(600)
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (label, value) in enumerate(options):
                    btn_rect = pygame.Rect(BUTTON_X, 50 + BUTTON_Y_START + i * (BUTTON_HEIGHT + BUTTON_GAP), BUTTON_WIDTH, BUTTON_HEIGHT)
                    if btn_rect.collidepoint(mouse_x, mouse_y):
                        click_sound.play()
                        return value

                if back_btn.collidepoint(mouse_x, mouse_y):
                    click_sound.play()
                    return None
