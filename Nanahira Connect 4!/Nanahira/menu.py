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

def animate_title_screen_intro(screen, bg):
    screen.blit(bg, (0, 0))
    font_big = font.Font('./Assets/Starborn.ttf', 64)
    font_small = font.Font('./Assets/Starborn.ttf', 40)
    clock = pygame.time.Clock()

    logo_x, logo_y = CONFIG["window_width"] // 2, CONFIG["window_height"] // 2
    logo_target_y = 90

    cover_x, cover_y = CONFIG["window_width"] // 4, CONFIG["window_height"] // 2
    cover_target_x = int(CONFIG["window_width"] * 0.75)

    button_x = (CONFIG["window_width"] - 400) // 2
    button_y = CONFIG["window_height"] // 2
    button_target_y = CONFIG["window_height"] - 150

    for frame in range(30):
        screen.blit(bg, (0, 0))
        progress = frame / 30

        current_logo_y = int(logo_y + (logo_target_y - logo_y) * progress)
        current_cover_x = int((cover_target_x - cover_x) * progress)
        current_button_y = int(button_y + (button_target_y - button_y) * progress)

        logo_rect = logo.get_rect(center=(logo_x, current_logo_y))
        screen.blit(logo, logo_rect)

        cover_rect = NanahiraMenu.get_rect(center=(current_cover_x, cover_y))
        screen.blit(NanahiraMenu, cover_rect)

        button_rect = Rect(button_x, current_button_y, 400, 100)
        mouse_x, mouse_y = mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_x, mouse_y)
        draw_button(screen, button_rect, "Start Game!", font_small, is_hovered, play_hover_sound=False)

        display.flip()
        clock.tick(60)

def animate_title_screen_exit(screen, bg):
    font_small = font.Font('./Assets/Starborn.ttf', 40)
    clock = pygame.time.Clock()

    logo_x, logo_y = CONFIG["window_width"] // 2, 90
    logo_target_y = -150

    cover_x, cover_y = int(CONFIG["window_width"] * 0.65), CONFIG["window_height"] // 2
    cover_target_x = CONFIG["window_width"] + 300

    button_x = (CONFIG["window_width"] - 400) // 2
    button_y = CONFIG["window_height"] - 150
    button_target_y = CONFIG["window_height"] + 150

    for frame in range(30):
        screen.blit(bg, (0, 0))
        progress = frame / 30

        current_logo_y = int(logo_y + (logo_target_y - logo_y) * progress)
        current_cover_x = int(cover_x + (cover_target_x - cover_x) * progress)
        current_button_y = int(button_y + (button_target_y - button_y) * progress)

        logo_rect = logo.get_rect(center=(logo_x, current_logo_y))
        screen.blit(logo, logo_rect)

        cover_rect = NanahiraMenu.get_rect(center=(current_cover_x, cover_y))
        screen.blit(NanahiraMenu, cover_rect)

        button_rect = Rect(button_x, current_button_y, 400, 100)
        mouse_x, mouse_y = mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_x, mouse_y)
        draw_button(screen, button_rect, "Start Game!", font_small, is_hovered, play_hover_sound=False)

        display.flip()
        clock.tick(60)

def draw_title_screen(screen, bg):
    screen.blit(bg, (0, 0))
    font_small = font.Font('./Assets/Starborn.ttf', 40)
    mouse_x, mouse_y = mouse.get_pos()

    cover_rect = NanahiraMenu.get_rect(center=(int(CONFIG["window_width"] // 2), CONFIG["window_height"] // 2))
    screen.blit(NanahiraMenu, cover_rect)

    logo_rect = logo.get_rect(center=(CONFIG["window_width"] // 2, 90))
    screen.blit(logo, logo_rect)

    button_width = 400
    button_height = 100
    button_x = (CONFIG["window_width"] - button_width) // 2
    button_y = CONFIG["window_height"] - 150
    button_rect = Rect(button_x, button_y, button_width, button_height)
    is_hovered = button_rect.collidepoint(mouse_x, mouse_y)
    draw_button(screen, button_rect, "Start Game!", font_small, is_hovered)

    quit_rect = quit_img.get_rect(bottomleft=(30, CONFIG["window_height"] - 30))
    screen.blit(quit_img, quit_rect)

    if mouse.get_pressed()[0] and quit_rect.collidepoint(mouse_x, mouse_y):
        display_message_image(screen, image=joever_img)
        pygame.time.wait(600)
        pygame.quit()
        exit()

    display.flip()
    clock = pygame.time.Clock()
    clock.tick(60) 

def animate_selection_menu_intro(screen, bg):
    screen.blit(bg, (0, 0))
    font_menu = font.Font('./Assets/Starborn.ttf', 40)
    clock = pygame.time.Clock()

    button_start_y = -BUTTON_HEIGHT
    target_y_list = [BUTTON_Y_START + 100 + i * (BUTTON_HEIGHT + BUTTON_GAP) for i in range(len(menu_options))]

    back_button_x = BUTTON_X - 150
    back_button_y = -BUTTON_HEIGHT
    back_target_y = target_y_list[-1] + BUTTON_HEIGHT - 150

    character_x = 5
    character_y = (CONFIG["window_height"] - Nanahira.get_height()) // 2

    for frame in range(30):
        screen.blit(bg, (0, 0))
        progress = frame / 30

        for i, option in enumerate(menu_options):
            current_y = int(button_start_y + (target_y_list[i] - button_start_y) * progress)
            rect = Rect(BUTTON_X, current_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            is_hovered = rect.collidepoint(mouse.get_pos())
            draw_button(screen, rect, option, font_menu, is_hovered, play_hover_sound=False)

        current_back_y = int(back_button_y + (back_target_y - back_button_y) * progress)
        back_rect = Rect(back_button_x, current_back_y, BUTTON_WIDTH // 3.2, BUTTON_HEIGHT)
        is_hovered_back = back_rect.collidepoint(mouse.get_pos())
        draw_button(screen, back_rect, "<--", font_menu, is_hovered_back, play_hover_sound=False)

        screen.blit(Nanahira, (character_x, character_y))
        display.flip()
        clock.tick(60)

def draw_menu(screen, bg):
    screen.blit(bg, (0, 0))
    font_menu = font.Font('./Assets/Starborn.ttf', 40)
    mouse_x, mouse_y = mouse.get_pos()
    button_y = BUTTON_Y_START + 100
    
    for mode in menu_options:
        button_rect = Rect(BUTTON_X, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        is_hovered = button_rect.collidepoint(mouse_x, mouse_y)
        draw_button(screen, button_rect, mode, font_menu, is_hovered)
        button_y += BUTTON_HEIGHT + BUTTON_GAP
    
    back_rect = Rect(BUTTON_X - 150, button_y - 150, BUTTON_WIDTH // 3.2, BUTTON_HEIGHT)
    is_hovered_back = back_rect.collidepoint(mouse_x, mouse_y)
    draw_button(screen, back_rect, "<--", font_menu, is_hovered_back)

    character_x = 5
    character_y = (CONFIG["window_height"] - Nanahira.get_height()) // 2
    screen.blit(Nanahira, (character_x, character_y))

    pygame.time.wait(10)
    display.flip()

def get_menu_selection(mouse_x, mouse_y):
    button_y = BUTTON_Y_START + 100
    for i, mode in enumerate(menu_options):
        if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH:
            btn_top = button_y
            btn_bottom = button_y + BUTTON_HEIGHT
            if btn_top <= mouse_y <= btn_bottom:
                return mode
        button_y += BUTTON_HEIGHT + BUTTON_GAP

    back_y = button_y - 150
    back_height = BUTTON_HEIGHT
    back_x = BUTTON_X - 150
    back_width = BUTTON_WIDTH // 3.2

    if back_x <= mouse_x <= back_x + back_width and back_y <= mouse_y <= back_y + back_height:
        return "BACK"

    return None

def draw_difficulty_menu(screen, bg):
    screen.blit(bg, (0, 0))
    font = font.Font('./Assets/Starborn.ttf', 40)
    button_y = BUTTON_Y_START
    mouse_x, mouse_y = mouse.get_pos()

    for difficulty in ["Easy", "Medium", "Hard"]:
        button_rect = Rect(BUTTON_X, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        is_hovered = button_rect.collidepoint(mouse_x, mouse_y)
        draw_button(screen, button_rect, difficulty, font, is_hovered)
        button_y += BUTTON_HEIGHT + BUTTON_GAP

    character_x = 5
    character_y = (CONFIG["window_height"] - Nanahira.get_height()) // 2
    screen.blit(Nanahira, (character_x, character_y))
    pygame.time.wait(10)
    display.flip()

def draw_AI_difficulty_menu(screen, bg, ai_label):
    text = font.Font('./Assets/Starborn.ttf', 40)
    running = True
    selected_difficulty = None

    while running:
        screen.blit(bg, (0, 0))
        mouse_x, mouse_y = mouse.get_pos()
        button_y = BUTTON_Y_START

        for diff in ["Easy", "Medium", "Hard"]:
            button_rect = Rect(BUTTON_X, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            is_hovered = button_rect.collidepoint(mouse_x, mouse_y)
            draw_button(screen, button_rect, f"{ai_label} - {diff}", text, is_hovered)
            button_y += BUTTON_HEIGHT + BUTTON_GAP

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = mouse.get_pos()
                if BUTTON_X <= mouseX <= BUTTON_X + BUTTON_WIDTH:
                    for i, difficulty in enumerate(["Easy", "Medium", "Hard"]):
                        button_y = BUTTON_Y_START + i * (BUTTON_HEIGHT + BUTTON_GAP)
                        if button_y <= mouseY <= button_y + BUTTON_HEIGHT:
                            selected_difficulty = difficulty
                            running = False
                            break

        character_x = 5
        character_y = (CONFIG["window_height"] - Nanahira.get_height()) // 2
        screen.blit(Nanahira, (character_x, character_y))
        pygame.time.wait(10)
        display.flip()

    return selected_difficulty