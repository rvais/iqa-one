import logging

from iqa.utils.walk_package import walk_package_and_import
from iqa.system.executor.base.executor import ExecutorBase
from iqa.utils.utils import get_subclass_with_prop_value
from iqa.system.executor import __package__

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Type


class ExecutorFactory(object):
    logger = logging.getLogger(__name__)
    __known_implementations: 'List[Type[ExecutorBase]]' = walk_package_and_import(__package__, ExecutorBase)

    @staticmethod
    def get_known_implementations() -> 'List[Type[ExecutorBase]]':
        return ExecutorFactory.__known_implementations.copy()

    @staticmethod
    def create_executor(implementation: str, **kwargs) -> 'ExecutorBase':
        """
            Loops through all implementations of the Executor class
            and returns an instance of the executor initialized from kwargs.

            Args:
                implementation:
                **kwargs:

            Returns:
    """
        try:
            executor = get_subclass_with_prop_value(
                superclass=ExecutorBase,
                in_class_property='implementation',
                cls_property_val=implementation
            )
            return executor(**kwargs)
        except ValueError:
            ExecutorFactory.logger.error('Implementation of "%s" executor was not found!' % implementation)
