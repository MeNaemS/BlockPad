import pygame
from settings import settings
from .scenes.menu import menu


def main():
    pygame.init()
    menu(settings)
