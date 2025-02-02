import pygame
from os import environ
from settings import settings
from .scenes.menu import menu


def main():
    environ['SDL_VIDEO_CENTERED'] = '1'
    clock: pygame.time.Clock = pygame.time.Clock()
    menu(settings, clock)
