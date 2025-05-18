import pygame
from .constants import *
from .menu import draw_button
from .messages import display_message_image
from .MenuAISelection import Nanahira, joever_img, click_sound

def draw_ai_vs_ai_selection_menu(screen, bg, label="White"):
    screen.blit(bg, (0, 0))
    font_menu = pygame.font.Font('./Assets/Starborn.ttf', 30)
    clock = pygame.time.Clock()
    options = [("Random", "random"), ("Ensemble ID3", "id3"), ("Parallel MCTS", "mcts")]
    running = True

    while running:
        screen.blit(bg, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        button_rects = []
        for i, (text, value) in enumerate(options):
            rect = pygame.Rect(BUTTON_X, BUTTON_Y_START + i * (BUTTON_HEIGHT + BUTTON_GAP), BUTTON_WIDTH, BUTTON_HEIGHT)
            is_hovered = rect.collidepoint(mouse_x, mouse_y)
            draw_button(screen, rect, f"{label} - {text}", font_menu, is_hovered)
            button_rects.append((rect, value))

        back_btn = pygame.Rect(BUTTON_X - 150, BUTTON_Y_START + 3 * (BUTTON_HEIGHT + BUTTON_GAP), BUTTON_WIDTH // 3.2, BUTTON_HEIGHT)
        is_hovered = back_btn.collidepoint(mouse_x, mouse_y)
        draw_button(screen, back_btn, "<--", font_menu, is_hovered)

        screen.blit(Nanahira, (5, (CONFIG["window_height"] - Nanahira.get_height()) // 2))
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_message_image(screen, image=joever_img)
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, value in button_rects:
                    if rect.collidepoint(mouse_x, mouse_y):
                        click_sound.play()
                        return value
                if back_btn.collidepoint(mouse_x, mouse_y):
                    click_sound.play()
                    return "BACK"

def draw_ai_vs_ai_mode_menu(screen, bg):
    screen.blit(bg, (0, 0))
    font_menu = pygame.font.Font('./Assets/Starborn.ttf', 30)
    clock = pygame.time.Clock()
    options = [("Normal Match", "visual"), ("Headless Simulation", "headless")]
    running = True

    while running:
        screen.blit(bg, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        button_rects = []
        for i, (label, value) in enumerate(options):
            btn = pygame.Rect(BUTTON_X, BUTTON_Y_START + i * (BUTTON_HEIGHT + BUTTON_GAP), BUTTON_WIDTH, BUTTON_HEIGHT)
            is_hovered = btn.collidepoint(mouse_x, mouse_y)
            draw_button(screen, btn, label, font_menu, is_hovered)
            button_rects.append((btn, value))

        back_btn = pygame.Rect(BUTTON_X - 150, BUTTON_Y_START + 3 * (BUTTON_HEIGHT + BUTTON_GAP), BUTTON_WIDTH // 3.2, BUTTON_HEIGHT)
        is_hovered = back_btn.collidepoint(mouse_x, mouse_y)
        draw_button(screen, back_btn, "<--", font_menu, is_hovered)

        screen.blit(Nanahira, (5, (CONFIG["window_height"] - Nanahira.get_height()) // 2))
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_message_image(screen, image=joever_img)
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, value in button_rects:
                    if rect.collidepoint(mouse_x, mouse_y):
                        click_sound.play()
                        return value
                if back_btn.collidepoint(mouse_x, mouse_y):
                    click_sound.play()
                    return "BACK"

def prompt_headless_runs(screen, bg):
    font = pygame.font.Font('./Assets/Starborn.ttf', 26)
    clock = pygame.time.Clock()
    input_str = ""
    active = True

    while active:
        screen.blit(bg, (0, 0))
        text = font.render("Enter number of headless runs: ", True, white)
        input_text = font.render(input_str, True, white)

        screen.blit(text, (BUTTON_X - 50, BUTTON_Y_START))
        screen.blit(input_text, (BUTTON_X, BUTTON_Y_START + 100))

        screen.blit(Nanahira, (5, (CONFIG["window_height"] - Nanahira.get_height()) // 2))
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_message_image(screen, image=joever_img)
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_str.isdigit() and int(input_str) > 0:
                        return int(input_str)
                elif event.key == pygame.K_BACKSPACE:
                    input_str = input_str[:-1]
                elif event.unicode.isdigit():
                    input_str += event.unicode
