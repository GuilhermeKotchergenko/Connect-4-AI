from pygame import *
from .constants import *

#Display winning message.

surface = pygame.Surface((CONFIG["window_width"], CONFIG["window_height"] + 100), pygame.SRCALPHA)

#Winning message
def display_message(screen, msg):
    pygame.draw.rect(surface, (255, 255, 255, 100), [0, 0, 1280, 900])
    screen.blit(surface, (0, 0))
    font = pygame.font.Font('./Assets/Starborn.ttf', 56)
    text = font.render(msg, True, (0, 0, 0))
    screen.blit(text, ((CONFIG["window_width"] - text.get_width()) // 2, (CONFIG["window_height"] - text.get_height()) // 2))
    pygame.display.update()
    pygame.time.wait(2000)

def display_message_image(screen, image):
    pygame.draw.rect(surface, (255, 255, 255, 100), [0, 0, CONFIG["window_width"], CONFIG["window_height"]])
    screen.blit(surface, (0, 0))

    img_scaled = image
    img_rect = img_scaled.get_rect(center=(CONFIG["window_width"] // 2, CONFIG["window_height"] // 2))
    screen.blit(img_scaled, img_rect)

    pygame.display.update()
    pygame.time.wait(1500)

def display_message_image_training(screen, image, msg):
    pygame.draw.rect(surface, (255, 255, 255, 100), [0, 0, CONFIG["window_width"], CONFIG["window_height"]])
    screen.blit(surface, (0, 0))

    img_scaled = image
    img_rect = img_scaled.get_rect(center=(CONFIG["window_width"] // 2, CONFIG["window_height"] // 1.8))
    font = pygame.font.Font('./Assets/Starborn.ttf', 56)
    text = font.render(msg, True, (0, 0, 0))
    screen.blit(text, ((CONFIG["window_width"] - text.get_width()) // 2, (CONFIG["window_height"] - text.get_height()) // 2.6))
    screen.blit(img_scaled, img_rect)

    pygame.display.update()
    pygame.time.wait(1500)