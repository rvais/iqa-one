import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from iqa.components.implementations import __package__

from iqa.components.abstract.component import Component
from iqa.utils.walk_package import walk_package_and_import

if TYPE_CHECKING:
    from typing import Optional, List, Type, Union
    from iqa.system.node.base.node import Node
    # from iqa.system.service.base.service import Service


def get_singular_name(name: str) -> str:
    if name.endswith('s'):
        return name[:-1]
    return name


class SpecificComponentFactory(ABC):

    @classmethod
    @abstractmethod
    def get_type(cls) -> 'Type[Component]':
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_component(implementation: str, node: 'Node', **kwargs) -> Component:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_available_implementations(cls) -> 'List[Type]':
        raise NotImplementedError


class ComponentFactory(SpecificComponentFactory):
    logger = logging.getLogger(__name__)
    __known_implementations: 'Optional[List[Type[SpecificComponentFactory]]]' \
        = walk_package_and_import(__package__, SpecificComponentFactory, max_depth=1)
    __type: 'Type[Component]' = Component

    @classmethod
    def get_type(cls) -> 'Type[Component]':
        return cls.__type

    @classmethod
    def get_available_implementations(cls) -> 'List[Type[SpecificComponentFactory]]':
        return ComponentFactory.__known_implementations.copy()

    @staticmethod
    def create_specified_component(component_type: 'Union[str, Type[Component]]', **kwargs) -> Component:
        found_factory: Optional[Type[SpecificComponentFactory]] = None
        component_cls: Optional[Type] = None

        if isinstance(component_type, str):
            component_type = get_singular_name(component_type)
        elif isinstance(component_type, type):
            component_cls = component_type
            component_type = component_type.__name__

        for factory in ComponentFactory.get_available_implementations():
            if component_cls is not None and factory.get_type() == component_cls:
                found_factory = factory
                break

            if factory.get_type().__name__.lower().startswith(component_type.lower()):
                found_factory = factory
                break

        if found_factory is None:
            ComponentFactory.logger.error(f"Couldn't find appropriate factory for '{component_type}' component type.")
            raise ValueError("Unknown component type, couldn't find appropriate factory.")

        return found_factory.create_component(**kwargs)

    @staticmethod
    def create_component(implementation: str, node: 'Node', **kwargs) -> 'Component':
        # return ComponentFactory.create_specified_component(component_type=implementation, node=node, **kwargs)
        raise NotImplementedError
