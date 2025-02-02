from typing import List, Tuple, Callable, overload
from pygame import Surface
from pygame.transform import smoothscale
from pygame.image import load
from functools import singledispatch
from .base_widget import BaseWidget


class BackgroundImage(BaseWidget):
    def __init__(
        self,
        parent: Surface,
        surface_object: Surface,
        coords: Tuple[int, int],
        size_of_surface: Tuple[int, int],
        child_surfaces: List[BaseWidget] = []
    ):
        super().__init__(parent, surface_object, coords, child_surfaces)
        self.__size_of_surface: Tuple[int, int] = size_of_surface

    def draw(self):
        self.parent.blit(smoothscale(self.surface, self.__size_of_surface), self.coords)
        for surface in self.child_surfaces:
            surface.draw()

    def add_child_surfaces(self, surfaces: List[BaseWidget] | BaseWidget) -> BaseWidget:
        all_surfaces: List[BaseWidget] = self.child_surfaces
        if isinstance(surfaces, BaseWidget):
            surfaces = [surfaces]
        for surface in surfaces:
            if isinstance(surface, BaseWidget):
                all_surfaces.append(surface)
                continue
            raise TypeError(
                (
                    'The surface argument must be of type List[BaseWidget] '
                    f'or BaseWidget, type error: {type(surface)}.'
                )
            )
        return self.__class__(
            self.parent,
            self.surface,
            self.coords,
            self.__size_of_surface,
            self.child_surfaces
        )


class Background:
    @staticmethod
    def __singledispatcher(
        func: Callable
    ) -> Callable:
        def wrapper(
            parent: Surface,
            surface_object: Surface | str,
            coords: Tuple[int, int],
            size_of_surface: Tuple[int, int] | None = None,
            child_surfaces: List[Surface] = []
        ):
            return valid_parameters(
                parent, surface_object, coords, size_of_surface, child_surfaces
            )

        @singledispatch
        def valid_parameters(
            parent: Surface,
            surface_object: Surface | str,
            coords: Tuple[int, int],
            size_of_surface: Tuple[int, int] | None = None,
            child_surfaces: List[Surface] = []
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
            elif not isinstance(surface_object, (str, Surface)):
                message = error_message.format(
                    'surface_object',
                    'also the main surface',
                    (
                        'pygame.Surface (an already created surface) or '
                        'str (path to image)'
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
            elif not isinstance(size_of_surface, (tuple, None)):
                message = error_message.format(
                    'size_of_surface',
                    'acceptable image size',
                    'Tuple[int, int] or None',
                    type(coords)
                )
            raise NotImplementedError(message)

        @valid_parameters.register
        def _(
            parent: Surface,
            surface_object: Surface,
            coords: Tuple[int, int],
            size_of_surface: Tuple[int, int] | None = None,
            child_surfaces: List[Surface] = []
        ):
            if size_of_surface is None:
                size_of_surface = surface_object.get_size()
            return func(parent, surface_object, coords, size_of_surface, child_surfaces)

        @valid_parameters.register
        def _(
            parent: Surface,
            surface_object: str,
            coords: Tuple[int, int],
            size_of_surface: Tuple[int, int] | None = None,
            child_surfaces: List[Surface] = []
        ):
            surface_object = load(surface_object)
            if size_of_surface is None:
                size_of_surface = surface_object.get_size()
            return func(parent, surface_object, coords, size_of_surface, child_surfaces)

        return wrapper

    @staticmethod
    @overload
    def create_background(
        parent: Surface,
        surface_object: Surface,
        coords: Tuple[int, int],
        size_of_surface: Tuple[int, int],
        child_surfaces: List[Surface] = []
    ) -> BackgroundImage: ...
    @staticmethod
    @overload
    def create_background(
        parent: Surface,
        surface_object: str,
        coords: Tuple[int, int],
        size_of_surface: Tuple[int, int],
        child_surfaces: List[Surface] = []
    ) -> BackgroundImage: ...

    @staticmethod
    @__singledispatcher
    def create_background(
        parent: Surface,
        surface_object: Surface,
        coords: Tuple[int, int],
        size_of_surface: Tuple[int, int],
        child_surfaces: List[Surface] = []
    ) -> BackgroundImage:
        return BackgroundImage(parent, surface_object, coords, size_of_surface, child_surfaces)

    def resize(widget: BackgroundImage, size: Tuple[int, int]) -> BackgroundImage:
        return BackgroundImage(
            widget.parent, widget.surface, widget.coords, size, widget.child_surfaces
        )
