import pygame
import os


# Класс
class DrawImage:
    surface: pygame.Surface

    @staticmethod
    def __draw_shadows(surface, inner_rect, padding, block_size, top_highlight, left_shadow, right_shadow,
                      bottom_shadow):
        """Рисует тени для 3D-блока."""
        pygame.draw.polygon(surface, [
            (inner_rect.x, inner_rect.y),
            (inner_rect.x + inner_rect.width, inner_rect.y),
            (inner_rect.x + inner_rect.width - padding, inner_rect.y + padding),
            (inner_rect.x + padding, inner_rect.y + padding),
        ], top_highlight)

        pygame.draw.polygon(surface, [
            (inner_rect.x, inner_rect.y),
            (inner_rect.x + padding, inner_rect.y + padding),
            (inner_rect.x + padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x, inner_rect.y + inner_rect.height),
        ], left_shadow)

        pygame.draw.polygon(surface, [
            (inner_rect.x + inner_rect.width, inner_rect.y),
            (inner_rect.x + inner_rect.width - padding, inner_rect.y + padding),
            (inner_rect.x + inner_rect.width - padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x + block_size, inner_rect.y + block_size),
        ], right_shadow)

        pygame.draw.polygon(surface, [
            (inner_rect.x, inner_rect.y + inner_rect.height),
            (inner_rect.x + padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x + block_size - padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x + block_size, inner_rect.y + block_size),
        ], bottom_shadow)

    def __draw_3d_block(self, surface, x, y, colors):
        """Рисует 3D-блок с тенями."""
        main_color, top_highlight, left_shadow, right_shadow, bottom_shadow = colors

        # Внешняя рамка
        outer_rect = pygame.Rect(x, y, self.block_size, self.block_size)
        pygame.draw.rect(surface, (255, 255, 255), outer_rect)

        # Основной квадрат
        inner_rect = outer_rect.inflate(-self.border_thickness, -self.border_thickness)
        pygame.draw.rect(surface, main_color, inner_rect)

        # Тени
        self._draw_shadows(
            surface, inner_rect, self.padding, self.block_size, top_highlight, left_shadow, right_shadow, bottom_shadow
        )

    def __draw_shape(self, shape, colors, surface: None | pygame.Surface = None):
        """Рисует фигуру с использованием блоков."""
        width, height, min_x, min_y = self.__calculate_screen_size(shape)
        if surface is None:
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        for (x, y) in shape:
            self.draw_3d_block(
                surface,
                (x - min_x) * self.block_size,
                (y - min_y) * self.block_size,
                colors,
            )
        return surface


# Интерфейс
class ShapeImageGenerator:
    def __init__(self, block_size=43, padding=4, border_thickness=1, config):
        pygame.init()

        self.__block_size = block_size
        self.__padding = padding
        self.__border_thickness = border_thickness

        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            self.COLORS = {key: [tuple(color) for color in value] for key, value in config.colors.items()}
            self.input_strings = config.shapes

    @property
    def images(self):
        """Генерирует изображения фигур и возвращает их."""
        images = {}
        for color_name, colors in self.COLORS.items():
            shapes = []
            for input_string in self.input_strings:
                shape = self.parse_input(input_string)
                surface = DrawImage.draw_shape(shape, colors)
                shapes.append((len(shape), surface))  # Сохраняем количество блоков вместе с изображением
            shapes.sort(key=lambda x: x[0])  # Сортируем по количеству блоков
            images[color_name] = shapes  # Храним пары (количество блоков, поверхность)
        return images



# Убрать pygame.init()
# Заняться тайпхинтом везде где это можно
# Вынести эту часть в settings и использовать dynaconf, вместо json.load:
#     with open(config_path, "r") as config_file:
#             config = json.load(config_file)
#             self.COLORS = {key: [tuple(color) for color in value] for key, value in config.colors.items()}
#             self.input_strings = config.shapes
# Сделать метод images геттером
# Все методы, отвечающие за рисование объекта вынести в соответсвующий класс и вызывать посредством интерфейса
