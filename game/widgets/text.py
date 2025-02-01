from .base_widget import BaseWidget
from pygame.font import SysFont, Font
from pygame import Surface, Color


class Text(BaseWidget):
    __slots__: tuple[int, ...] = ('__parent', '__coords', '__size', '__text',)

    def __init__(
        self,
        parent: Surface,
        coords: tuple[int, int],
        size: tuple[int, int],
        font: Font = SysFont('Times New Roman', 15),
        text: str = 'text',
        color: Color = Color(255, 255, 255, 1)
    ):
        super().__init__(parent, coords, size)
        self.__font: Font = font
        self.__text: str = text
        self.__color: Color = color

    def set_coords(self, coords: tuple[int, int]) -> BaseWidget:
        return self.__class__(
            self.parent, coords, self.size, self.__font, self.__text, self.__color
        )

    def set_size(self, size: tuple[int, int]) -> BaseWidget:
        return self.__class__(
            self.parent, self.coords, size, self.__font, self.__text, self.__color
        )

    def set_font(self, font: Font) -> BaseWidget:
        return self.__class__(
            self.parent, self.coords, self.size, font, self.__text, self.__color
        )

    def draw(self):
        self.__parent.blit(
            self.__font.render(self.__text, color=self.__color),
            self.coords,
            self.size
        )
    