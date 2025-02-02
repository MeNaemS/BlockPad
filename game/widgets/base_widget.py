from abc import ABC, abstractmethod
from typing import Tuple, overload, Callable, List
from functools import singledispatch
from pygame import Surface


class ABCWidget(ABC):
    __slots__: Tuple[str, ...] = ('__parent', '__surface', '__coords', '__child_surfaces',)

    def __init__(
        self,
        parent: Surface,
        surface_object: Surface,
        coords: Tuple[int, int]
    ):
        self.__parent: Surface = parent
        self.__surface: Surface = surface_object
        self.__coords: Tuple[int, int] = coords

    @property
    def surface(self) -> Surface:
        return self.__surface

    @property
    def parent(self) -> Surface:
        return self.__parent

    @property
    def coords(self) -> Tuple[int, int]:
        return self.__coords

    @property
    def x(self) -> int:
        return self.__coords[0]

    @property
    def y(self) -> int:
        return self.__coords[1]

    @property
    def size(self) -> Tuple[int, int]:
        return self.__surface.get_size()

    @property
    def width(self) -> int:
        return self.__surface.get_width()

    @property
    def height(self) -> int:
        return self.__surface.get_height()

    @abstractmethod
    def draw(self):
        self.__parent.blit(self.__surface, self.__coords)


class BaseWidget(ABCWidget):
    def __init__(
        self,
        parent: Surface,
        surface_object: Surface,
        coords: Tuple[int, int],
        child_surfaces: List[ABCWidget] = []
    ):
        super().__init__(parent, surface_object, coords)
        self.__child_surfaces: List[ABCWidget] = child_surfaces

    def draw(self):
        self.parent.blit(self.surface, self.coords)
        for surface in self.__child_surfaces:
            surface.draw()

    @property
    def child_surfaces(self) -> List[ABCWidget]:
        return self.__child_surfaces

    def add_child_surfaces(self, surfaces: List[ABCWidget] | ABCWidget) -> ABCWidget:
        all_surfaces: List[ABCWidget] = self.__child_surfaces
        if isinstance(surfaces, ABCWidget):
            surfaces = [surfaces]
        for surface in surfaces:
            if isinstance(surface, ABCWidget):
                all_surfaces.append(surface)
                continue
            raise TypeError(
                (
                    'The surface argument must be of type List[ABCWidget] '
                    f'or ABCWidget, type error: {type(surface)}.'
                )
            )
        return self.__class__(self.parent, self.surface, self.coords, all_surfaces)


class Widget:
    @staticmethod
    def __singledispatcher(
        func: Callable[[Surface, Surface, Tuple[int, int]], BaseWidget]
    ) -> Callable:
        def wrapper(
            parent: Surface,
            surface_object: Surface | Tuple[int, int],
            coords: Tuple[int, int]
        ) -> None | BaseWidget:
            return valid_parameters(parent, surface_object, coords)

        @singledispatch
        def valid_parameters(
            parent: Surface,
            surface_object: Surface | Tuple[int, int],
            coords: Tuple[int, int]
        ):
            # name_of_variable, description_of_variable, valid_types, invalid_type
            error_message: str = 'The "{}" parameter ({}) must be of type {}, invalid type: {}.'
            if not isinstance(parent, Surface):
                message: str = error_message.format(
                    'parent',
                    'aka the parent on which other pygame.Surface type objects will be located',
                    'pygame.Surface',
                    type(coords)
                )
            elif not isinstance(surface_object, (tuple, Surface)):
                message = error_message.format(
                    'surface_object',
                    'also the main surface',
                    (
                        'pygame.Surface (an already created surface) or '
                        'Tuple[int, int] (the size of the surface that will be created)'
                    ),
                    type(surface_object)
                )
            elif not isinstance(coords, tuple):
                message = error_message.format(
                    'coords',
                    'surface coordinates',
                    'Tuple[int, int] (pos_x, pos_y)',
                    type(coords)
                )
            raise NotImplementedError(message)

        @valid_parameters.register
        def _(
            parent: Surface, surface_object: Tuple[int, int], coords: Tuple[int, int]
        ) -> BaseWidget:
            return func(parent, Surface(surface_object), coords)

        @valid_parameters.register
        def _(
            parent: Surface, surface_object: Surface, coords: Tuple[int, int]
        ) -> BaseWidget:
            return func(parent, surface_object, coords)

        return wrapper

    @staticmethod
    @overload
    def create_widget(
        parent: Surface, surface_object: Surface, coords: Tuple[int, int]
    ) -> BaseWidget: ...
    @staticmethod
    @overload
    def create_widget(
        parent: Surface, surface_object: Tuple[int, int], coords: Tuple[int, int]
    ) -> BaseWidget: ...

    @staticmethod
    @__singledispatcher
    def create_widget(
        parent: Surface,
        surface_object: Surface,
        coords: Tuple[int, int]
    ) -> BaseWidget:
        return BaseWidget(parent, surface_object, coords)

    @staticmethod
    def resize_widget(widget: BaseWidget, size: Tuple[int, int]) -> BaseWidget:
        return BaseWidget(widget.parent, Surface(size), widget.coords, widget.child_surfaces)

    @staticmethod
    def recoords_widget(widget: BaseWidget, coords: Tuple[int, int]) -> BaseWidget:
        return BaseWidget(widget.parent, widget.surface, coords, widget.child_surfaces)
