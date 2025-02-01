from .base_widget import BaseWidget
from .text import Text
from pygame import Rect, Surface

BUTTON_TEXT_LENGTH_ERROR: str = 'Text: {}, exceeds the allowed number of characters: {}'


class Validate:
    def length_of_text(
        text: str | None,
        max_length: int,
        error_msg: str = BUTTON_TEXT_LENGTH_ERROR
    ):
        if text is not None and len(text) > max_length:
            raise ValueError(error_msg.format(text, max_length))


class Button(BaseWidget):
    __slots__: tuple[int, ...] = ('__parent', '__coords', '__size', '__text', '__button',)

    def __init__(
        self,
        parent: Surface,
        coords: tuple[int, int],
        size: tuple[int, int],
        text: str | None = None
    ):
        super().__init__(parent, coords, size)
        self.__text: Text = Text(
            self.parent,
            self.get_coords(),
            self.get_size(),
            '' if text is None else text
        )
        self.__button: Rect = Rect(self.__coords, self.__size)

    def set_coords(self, coords: tuple[int, int]) -> BaseWidget:
        return self.__class__(
            self.parent, coords, self.size, self.__font, self.__text, self.__color
        )

    def set_size(self, size: tuple[int, int]) -> BaseWidget:
        return self.__class__(
            self.parent, self.coords, size, self.__font, self.__text, self.__color
        )

    def draw(self):
        self.parent.blit(
            self.__button,
            self.coords,
            self.size
        )
        self.__text.draw()
