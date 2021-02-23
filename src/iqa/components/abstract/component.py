import logging
from abc import ABC, abstractmethod
from inspect import signature
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Dict
    from iqa.system.node.base.node import Node


class Component(ABC):
    """
    Main class that represents a abstract component.
    """

    def __init__(self, name: 'Optional[str]' = None, node: 'Optional[Node]' = None, **kwargs) -> None:
        super(Component, self).__init__(**kwargs)
        self._node: Node = node

        # Changes necessary due to the fact this class is used as one of the bases in multiple inheritance
        if name is None and node is not None:
            name = f"{self.__class__.__name__}_at_{node.hostname}"
        elif name is None and node is None:
            name = self.__class__.__name__

        if not hasattr(self, '_name'):
            self._name = name
        elif not hasattr(self, '_name') and name is None:
            self._name = self.__class__.__name__

        if not hasattr(self, '_logger') or not isinstance(self._logger, logging.Logger):
            self._logger: logging.Logger = logging.getLogger(self._name)
        self._logger: logging.Logger = logging.getLogger(self._name)

    @property
    @abstractmethod
    def implementation(self):
        raise NotImplementedError

    @property
    def node(self) -> 'Optional[Node]':
        return self._node

    @property
    def name(self) -> 'Optional[str]':
        return self._name

    @staticmethod
    def call_if_all_arguments_in_kwargs(func, **kwargs) -> None:
        """
        Call the given function if all declared arguments exist in
        the kwargs dictionary. In example, if passed function is set_ssl_auth,
        it will be called if kwargs contains the following keys:
        pem_file, key_file, keystore, keystore_pass and keystore_alias.
        :param func:
        :return:
        """
        # kwargs not informed
        if not kwargs:
            return

        # Not all function arguments needed are available in kwargs
        if not all(
            [k in list(kwargs.keys()) for k in list(signature(func).parameters.keys())]
        ):
            return

        # Calling function if all args present in kwargs
        arg_dict: Dict = {
            k: v
            for k, v in kwargs.items()
            if k in list(signature(func).parameters.keys())
        }
        func(**arg_dict)
