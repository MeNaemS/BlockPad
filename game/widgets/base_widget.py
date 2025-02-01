from abc import ABC, abstractmethod
from pygame import Surface


class BaseWidget(ABC):
    __slots__: tuple[int, ...] = ('__parent', '__coords', '__size',)

    def __init__(self, parent: Surface, coords: tuple[int, int], size: tuple[int, int]):
        self.__parent: Surface = parent
        self.__coords: tuple[int, int] = coords
        self.__size: tuple[int, int] = size

    @abstractmethod
    def draw(self):
        self.__parent.blit(Surface((0, 0)), self.__coords, self.__size)

    @property
    def parent(self) -> Surface:
        return self.__parent

    def get_coords(self) -> tuple[int, int]:
        return self.__coords

    @abstractmethod
    def set_coords(self, coords: tuple[int, int]) -> object:
        return self.__class__(self.__parent, coords, self.__size)

    @property
    def x(self) -> int:
        return self.__coords[0]

    @property
    def y(self) -> int:
        return self.__coords[1]

    def get_size(self) -> tuple[int, int]:
        return self.__size

    @abstractmethod
    def set_size(self, size: tuple[int, int]) -> object:
        return self.__class__(self.__parent, self.__coords, size)

    @property
    def width(self) -> int:
        return self.__size[0]

    @property
    def height(self) -> int:
        return self.__size[1]
