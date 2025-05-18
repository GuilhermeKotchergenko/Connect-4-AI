import pygame

# Configuration object for window and board settings
CONFIG = {
    "window_width": 1280,
    "window_height": 900,
    "board_width": 680,
    "board_height": 680,
    "rows": 5,
    "cols": 5
}

CONFIG["square_size"] = CONFIG["board_width"] // CONFIG["cols"]
CONFIG["board_x"] = (CONFIG["window_width"] - CONFIG["board_width"]) // 1.2
CONFIG["board_y"] = (CONFIG["window_height"] - CONFIG["board_height"]) // 2

# Colors
board_color = (237, 169, 90)
move_color = (255, 255, 255)
white = (255, 255, 255)
black = (0, 0, 0)

# Icon
icon = pygame.image.load('./Assets/Logo32.png')

# Buttons
BUTTON_WIDTH = 450
BUTTON_HEIGHT = 100
BUTTON_GAP = 50
BUTTON_X = int((CONFIG["window_width"] - BUTTON_WIDTH) // 1.5)
BUTTON_Y_START = 200
