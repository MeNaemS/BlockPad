import pygame
import os
import json


class ShapeImageGenerator:
    def __init__(self, block_size=43, padding=4, border_thickness=1, config_path="../configs/config.json"):
        pygame.init()

        self.block_size = block_size
        self.padding = padding
        self.border_thickness = border_thickness

        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            self.COLORS = {key: [tuple(color) for color in value] for key, value in config["colors"].items()}
            self.input_strings = config["shapes"]

    @staticmethod
    def draw_polygon(surface, points, color):
        pygame.draw.polygon(surface, color, points)

    @staticmethod
    def _draw_shadows(surface, inner_rect, padding, block_size, top_highlight, left_shadow, right_shadow,
                      bottom_shadow):
        """Рисует тени для 3D-блока."""
        ShapeImageGenerator.draw_polygon(surface, [
            (inner_rect.x, inner_rect.y),
            (inner_rect.x + inner_rect.width, inner_rect.y),
            (inner_rect.x + inner_rect.width - padding, inner_rect.y + padding),
            (inner_rect.x + padding, inner_rect.y + padding),
        ], top_highlight)

        ShapeImageGenerator.draw_polygon(surface, [
            (inner_rect.x, inner_rect.y),
            (inner_rect.x + padding, inner_rect.y + padding),
            (inner_rect.x + padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x, inner_rect.y + inner_rect.height),
        ], left_shadow)

        ShapeImageGenerator.draw_polygon(surface, [
            (inner_rect.x + inner_rect.width, inner_rect.y),
            (inner_rect.x + inner_rect.width - padding, inner_rect.y + padding),
            (inner_rect.x + inner_rect.width - padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x + block_size, inner_rect.y + block_size),
        ], right_shadow)

        ShapeImageGenerator.draw_polygon(surface, [
            (inner_rect.x, inner_rect.y + inner_rect.height),
            (inner_rect.x + padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x + block_size - padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x + block_size, inner_rect.y + block_size),
        ], bottom_shadow)

    def draw_3d_block(self, surface, x, y, colors):
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

    def parse_input(self, input_string):
        """Создает список координат для фигуры."""
        shape = []
        for y, line in enumerate(input_string.splitlines()):
            for x, char in enumerate(line):
                if char == "o":
                    shape.append((x, y))
        return shape

    def calculate_screen_size(self, shape):
        """Вычисляет размеры экрана под фигуру."""
        min_x = min(x for x, y in shape)
        max_x = max(x for x, y in shape)
        min_y = min(y for x, y in shape)
        max_y = max(y for x, y in shape)

        width = (max_x - min_x + 1) * self.block_size
        height = (max_y - min_y + 1) * self.block_size
        return width, height, min_x, min_y

    def draw_shape(self, shape, colors):
        """Рисует фигуру с использованием блоков."""
        width, height, min_x, min_y = self.calculate_screen_size(shape)
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

    def get_images(self):
        """Генерирует изображения фигур и возвращает их."""
        images = {}
        for color_name, colors in self.COLORS.items():
            shapes = []
            for input_string in self.input_strings:
                shape = self.parse_input(input_string)
                surface = self.draw_shape(shape, colors)
                shapes.append((len(shape), surface))  # Сохраняем количество блоков вместе с изображением
            shapes.sort(key=lambda x: x[0])  # Сортируем по количеству блоков
            images[color_name] = shapes  # Храним пары (количество блоков, поверхность)
        return images

    def result_images(self):
        images = self.get_images()
        formatted_output = "{\n"
        for color, shapes in images.items():
            formatted_output += f" '{color}': [\n"
            for count, surface in shapes:
                formatted_output += (
                    f"    <Surface({surface.get_width()}x{surface.get_height()}x32 SW)>, ({count} blocks),\n"
                )
            formatted_output += " ],\n"
        formatted_output += "}"

        print(formatted_output)


# Проверка и сохранение
if __name__ == "__main__":
    generator = ShapeImageGenerator()
    generator.result_images()
    pygame.quit()
