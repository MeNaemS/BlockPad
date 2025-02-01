from schemas.config import Config
import pygame
import sys


def menu(configs: Config):
    screen: pygame.Surface = pygame.display.set_mode(tuple(configs.window.size))
    pygame.display.set_caption(configs.window.title)
    menu_background: pygame.Surface = pygame.image.load(configs.background_menu_path).convert()
    menu_background = pygame.transform.scale(menu_background, tuple(configs.window.size))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(menu_background, (0, 0))
        pygame.display.update()
