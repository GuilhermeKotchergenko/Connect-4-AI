import pygame
import os
from .constants import *
from .menu import draw_button
from .messages import *
from .ai_id3 import trainnn, learned_trees_p1, learned_trees_p2

Nanahira = pygame.image.load('./Assets/Nanahira.png')
click_sound = pygame.mixer.Sound('./Nanahira/click.wav')
training_done_sound = pygame.mixer.Sound('./Nanahira/done_training.wav')
joever_img = pygame.image.load('./Assets/joever.png')
training_img = pygame.image.load('./Assets/training.png')

def is_training_available():
    return os.path.exists("trees_p1_easy.pkl") or os.path.exists("trees_p2_easy.pkl")

training_done = is_training_available()

def draw_id3_configuration_menu(screen, bg):
    """
    Menu to select player piece color and ID3 type.
    Returns tuple (player_color, id3_type) or None if BACK selected.
    """
    global training_done
    clock = pygame.time.Clock()
    font_menu = pygame.font.Font('./Assets/Starborn.ttf', 40)
    selected_color = None
    selected_type = None
    running = True

    while running:
        screen.blit(bg, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        white_btn = pygame.Rect(BUTTON_X, BUTTON_Y_START, BUTTON_WIDTH // 2 - 10, BUTTON_HEIGHT)
        black_btn = pygame.Rect(BUTTON_X + BUTTON_WIDTH // 2 + 10, BUTTON_Y_START, BUTTON_WIDTH // 2 - 10, BUTTON_HEIGHT)
        is_white_hovered = white_btn.collidepoint(mouse_x, mouse_y)
        is_black_hovered = black_btn.collidepoint(mouse_x, mouse_y)
        white_selected = selected_color == 1
        black_selected = selected_color == 2
        simple_selected = selected_type == "simple"
        adv_selected = selected_type == "advanced"
        draw_button(screen, white_btn, "White", font_menu, is_white_hovered or white_selected)
        draw_button(screen, black_btn, "Black", font_menu, is_black_hovered or black_selected)

        simple_btn = pygame.Rect(BUTTON_X, BUTTON_Y_START + 180, BUTTON_WIDTH, BUTTON_HEIGHT)
        adv_btn = pygame.Rect(BUTTON_X, BUTTON_Y_START + 180 + BUTTON_HEIGHT + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
        is_simple_hovered = simple_btn.collidepoint(mouse_x, mouse_y)
        is_adv_hovered = adv_btn.collidepoint(mouse_x, mouse_y)
        draw_button(screen, simple_btn, "Simple ID3", font_menu, is_simple_hovered or simple_selected)
        draw_button(screen, adv_btn, "Ensemble ID3", font_menu, is_adv_hovered or adv_selected)

        # Train button
        train_btn = pygame.Rect(BUTTON_X, BUTTON_Y_START + 500, BUTTON_WIDTH, BUTTON_HEIGHT)
        is_train_hovered = train_btn.collidepoint(mouse_x, mouse_y)
        draw_button(screen, train_btn, "Train AI" if not training_done else "Retrain AI", font_menu, is_train_hovered)

        # Back button
        back_btn = pygame.Rect(BUTTON_X - 150, BUTTON_Y_START + 500, BUTTON_WIDTH // 3.2, BUTTON_HEIGHT)
        is_back_hovered = back_btn.collidepoint(mouse_x, mouse_y)
        draw_button(screen, back_btn, "<--", font_menu, is_back_hovered)

        # Character
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
                elif is_simple_hovered:
                    click_sound.play()
                    selected_type = "simple"
                elif is_adv_hovered:
                    click_sound.play()
                    selected_type = "advanced"
                elif is_back_hovered:
                    click_sound.play()
                    return None
                elif is_train_hovered:
                    click_sound.play()
                    display_message_image_training(screen, training_img, "Training AI...")
                    for level in ["Easy", "Medium", "Hard"]:
                        trainnn(1, difficulty=level)
                        trainnn(2, difficulty=level)
                    training_done = True
                    training_done_sound.play()
                    done_img = image.load('./Assets/done.png')
                    display_message_image_training(screen, done_img, "Training Complete!")


                if selected_color and selected_type:
                    return (selected_color, selected_type)

def draw_difficulty_selection_menu(screen, bg):
    """ Separate menu to select difficulty level after color/type are chosen. """
    clock = pygame.time.Clock()
    font_menu = pygame.font.Font('./Assets/Starborn.ttf', 40)
    selected_difficulty = None
    difficulties = ["Easy", "Medium", "Hard"]
    running = True

    while running:
        screen.blit(bg, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for i, level in enumerate(difficulties):
            diff_btn = pygame.Rect(BUTTON_X, 50 + BUTTON_Y_START + i * (BUTTON_HEIGHT + BUTTON_GAP + 10), BUTTON_WIDTH, BUTTON_HEIGHT)
            is_hovered = diff_btn.collidepoint(mouse_x, mouse_y)
            draw_button(screen, diff_btn, level, font_menu, is_hovered or selected_difficulty == level)

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
                for i, level in enumerate(difficulties):
                    diff_btn = pygame.Rect(BUTTON_X, 50 + BUTTON_Y_START + i * (BUTTON_HEIGHT + BUTTON_GAP + 10), BUTTON_WIDTH, BUTTON_HEIGHT)
                    if diff_btn.collidepoint(mouse_x, mouse_y):
                        click_sound.play()
                        return level

                if back_btn.collidepoint(mouse_x, mouse_y):
                    click_sound.play()
                    return None