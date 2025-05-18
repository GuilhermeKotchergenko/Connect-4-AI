from pygame import *
from .constants import *
from .board import *
from .messages import display_message_image
import time

NanahiraMenu = image.load('./Assets/NanahiraMenu.png')
Nanahira = image.load('./Assets/Nanahira.png')
logo = image.load('./Assets/Nanahira Connect4 Logo.png')
quit_img = image.load('./Assets/quit.png')
joever_img = image.load('./Assets/joever.png')

pygame.mixer.init()
hover_sound = pygame.mixer.Sound('./Nanahira/hover.wav')
click_sound = pygame.mixer.Sound('./Nanahira/click.wav')

menu_options = ["Player x Player", "Player x AI", "AI x AI"]

def draw_button(screen, rect, text, font, is_hovered, play_hover_sound=True):
    if not hasattr(draw_button, "hovered_buttons"):
        draw_button.hovered_buttons = set()
    if not hasattr(draw_button, "last_hover_time"):
        draw_button.last_hover_time = {}

    button_id = (rect.x, rect.y, rect.width, rect.height)
    now = time.time()
    delay = 0.2

    if play_hover_sound and is_hovered:
        last_time = draw_button.last_hover_time.get(button_id, 0)
        if now - last_time >= delay and button_id not in draw_button.hovered_buttons:
            hover_sound.play()
            draw_button.last_hover_time[button_id] = now
            draw_button.hovered_buttons.add(button_id)
    elif not is_hovered:
        draw_button.hovered_buttons.discard(button_id)

    button_color = (255, 222, 213) if is_hovered else (250, 192, 203)
    draw.rect(screen, button_color, rect, 0, 30)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_ai_selection_menu(screen, bg):
    screen.blit(bg, (0, 0))
    font_menu = font.Font('./Assets/Starborn.ttf', 35)
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(bg, (0, 0))
        mouse_x, mouse_y = mouse.get_pos()

        id3_rect = Rect(BUTTON_X, 50 + BUTTON_Y_START + 100, BUTTON_WIDTH, BUTTON_HEIGHT)
        mcts_rect = Rect(BUTTON_X, 50 + BUTTON_Y_START + 100 + BUTTON_HEIGHT + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
        back_rect = Rect(BUTTON_X - 150, BUTTON_Y_START + 100 + 2 * (BUTTON_HEIGHT + BUTTON_GAP), BUTTON_WIDTH // 3.2, BUTTON_HEIGHT)

        is_hovered_id3 = id3_rect.collidepoint(mouse_x, mouse_y)
        is_hovered_mcts = mcts_rect.collidepoint(mouse_x, mouse_y)
        is_hovered_back = back_rect.collidepoint(mouse_x, mouse_y)

        draw_button(screen, id3_rect, "ID3 Decision Tree", font_menu, is_hovered_id3)
        draw_button(screen, mcts_rect, "MCTS", font_menu, is_hovered_mcts)
        draw_button(screen, back_rect, "<--", font_menu, is_hovered_back)

        screen.blit(Nanahira, (5, (CONFIG["window_height"] - Nanahira.get_height()) // 2))
        display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                display_message_image(screen, image=joever_img)
                pygame.time.wait(600)
                pygame.quit()
                exit()

            elif event.type == MOUSEBUTTONDOWN:
                if is_hovered_id3:
                    click_sound.play()
                    return "ID3"
                elif is_hovered_mcts:
                    click_sound.play()
                    return "MCTS"
                elif is_hovered_back:
                    click_sound.play()
                    return "BACK"
