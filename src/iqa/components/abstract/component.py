from inspect import signature
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from iqa.system.node.base.node import Node


class Component:
    """
    Main class that represents a abstract component.
    """

    def __init__(self, name: str, node: 'Node') -> None:
        self.instance_name: str = name
        self._node: Node = node

    @property
    def implementation(self):
        raise NotImplementedError

    @property
    def node(self) -> 'Optional[Node]':
        return self._node

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
        arg_dict: dict = {
            k: v
            for k, v in kwargs.items()
            if k in list(signature(func).parameters.keys())
        }
        func(**arg_dict)
