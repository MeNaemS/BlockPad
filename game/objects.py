import pygame
from dynaconf import settings


class DrawImage:
    @staticmethod
    def _draw_shadows(
            surface: pygame.Surface,
            inner_rect: pygame.Rect,
            padding: int,
            block_size: int,
            top_highlight: tuple[int, int, int],
            left_shadow: tuple[int, int, int],
            right_shadow: tuple[int, int, int],
            bottom_shadow: tuple[int, int, int],
    ) -> None:
        """Рисует тени для 3D-блока."""
        pygame.draw.polygon(surface, top_highlight, [
            (inner_rect.x, inner_rect.y),
            (inner_rect.x + inner_rect.width, inner_rect.y),
            (inner_rect.x + inner_rect.width - padding, inner_rect.y + padding),
            (inner_rect.x + padding, inner_rect.y + padding),
        ])
        pygame.draw.polygon(surface, left_shadow, [
            (inner_rect.x, inner_rect.y),
            (inner_rect.x + padding, inner_rect.y + padding),
            (inner_rect.x + padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x, inner_rect.y + inner_rect.height),
        ])
        pygame.draw.polygon(surface, right_shadow, [
            (inner_rect.x + inner_rect.width, inner_rect.y),
            (inner_rect.x + inner_rect.width - padding, inner_rect.y + padding),
            (inner_rect.x + inner_rect.width - padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x + block_size, inner_rect.y + block_size),
        ])
        pygame.draw.polygon(surface, bottom_shadow, [
            (inner_rect.x, inner_rect.y + inner_rect.height),
            (inner_rect.x + padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x + block_size - padding, inner_rect.y + inner_rect.height - padding),
            (inner_rect.x + block_size, inner_rect.y + block_size),
        ])

    def draw_3d_block(
            self,
            surface: pygame.Surface,
            x: int,
            y: int,
            colors: tuple[tuple[int, int, int], ...],
            block_size: int,
            padding: int,
            border_thickness: int
    ) -> None:
        """Рисует 3D-блок с тенями."""
        main_color, top_highlight, left_shadow, right_shadow, bottom_shadow = colors
        outer_rect = pygame.Rect(x, y, block_size, block_size)
        pygame.draw.rect(surface, (255, 255, 255), outer_rect)
        inner_rect = outer_rect.inflate(-border_thickness, -border_thickness)
        pygame.draw.rect(surface, main_color, inner_rect)
        self._draw_shadows(surface, inner_rect, padding, block_size, top_highlight, left_shadow, right_shadow,
                           bottom_shadow)

    def draw_shape(
            self,
            shape: list[tuple[int, int]],
            colors: tuple[tuple[int, int, int], ...],
            block_size: int,
            padding: int,
            border_thickness: int
    ) -> pygame.Surface:
        """Рисует фигуру с использованием блоков."""
        width, height, min_x, min_y = self.calculate_screen_size(shape, block_size)
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        for (x, y) in shape:
            self.draw_3d_block(
                surface,
                (x - min_x) * block_size,
                (y - min_y) * block_size,
                colors,
                block_size,
                padding,
                border_thickness
            )
        return surface

    @staticmethod
    def calculate_screen_size(
            shape: list[tuple[int, int]],
            block_size: int
    ) -> tuple[int, int, int, int]:
        """Вычисляет размер экрана для фигуры."""
        min_x = min(x for x, y in shape)
        min_y = min(y for x, y in shape)
        max_x = max(x for x, y in shape)
        max_y = max(y for x, y in shape)
        width = (max_x - min_x + 1) * block_size
        height = (max_y - min_y + 1) * block_size
        return width, height, min_x, min_y


class ShapeImageGenerator:
    def __init__(
            self,
            block_size: int = 43,
            padding: int = 4,
            border_thickness: int = 1
    ) -> None:
        self.__block_size = block_size
        self.__padding = padding
        self.__border_thickness = border_thickness
        # Используем settings.colors напрямую
        self.COLORS: dict[str, list[tuple[int, int, int]]] = {
            key: [tuple(color) for color in value] for key, value in settings.colors.items()
        }
        self.input_strings: list[str] = list(settings.shapes)
        self.drawer = DrawImage()

    @property
    def images(self) -> dict[str, list[pygame.Surface]]:
        """Генерирует изображения фигур и возвращает их."""
        images: dict[str, list[pygame.Surface]] = {}
        for color_name, colors in self.COLORS.items():
            surfaces: list[pygame.Surface] = []
            shapes_with_surfaces: list[tuple[int, pygame.Surface]] = []

            for input_string in self.input_strings:
                shape = self.parse_input(input_string)
                surface = self.drawer.draw_shape(shape, colors, self.__block_size, self.__padding,
                                                 self.__border_thickness)
                shapes_with_surfaces.append((len(shape), surface))

            # Сортируем по возрастанию количества блоков
            shapes_with_surfaces.sort(key=lambda x: x[0])

            # Извлекаем только поверхности
            surfaces = [surface for _, surface in shapes_with_surfaces]
            images[color_name] = surfaces

        return images

    @staticmethod
    def parse_input(input_string: str) -> list[tuple[int, int]]:
        """Парсит входную строку и возвращает координаты фигуры."""
        shape: list[tuple[int, int]] = []
        for y, row in enumerate(input_string.split("\n")):
            for x, char in enumerate(row):
                if char == 'o':
                    shape.append((x, y))
        return shape
