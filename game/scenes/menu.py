from schemas.config import Config
from game.widgets.base_widget import Widget, BaseWidget
from game.widgets.background import Background, BackgroundImage
import pygame
import sys


def menu(configs: Config, clock: pygame.time.Clock):
    screen: pygame.Surface = pygame.display.set_mode(tuple(configs.window.size))
    pygame.display.set_caption(configs.window.title)
    icon: pygame.Surface = pygame.image.load(configs.icon)
    pygame.display.set_icon(icon)

    menu_background: BackgroundImage = Background.create_background(
        screen, configs.background_menu_path, (0, 0), screen.get_size()
    )
    shadow: BaseWidget = Widget.create_widget(
        menu_background.surface,
        pygame.Surface((menu_background.width // 2, menu_background.height)),
        (menu_background.width // 4, 0)
    )
    shadow.surface.fill(pygame.Color(128, 128, 128))
    shadow.surface.set_alpha(10)
    menu_background = menu_background.add_child_surfaces(shadow)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode(tuple(configs.window.minimal_size))
                    menu_background = Background.resize(menu_background, screen.get_size())
        menu_background.draw()
        clock.tick(configs.game.FPS)
        pygame.display.flip()
