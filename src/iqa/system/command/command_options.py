"""
This modules defines all supported command line options for external
abstract clients, with specialized classes for sender and receivers.
Each implementation of ClientOptionsBase must provide a list of
OptionAbstract (optconstruct) that is supported.
"""

from typing import TYPE_CHECKING
from optconstruct.types import Toggle, Prefixed, KWOption, ListOption

if TYPE_CHECKING:
    from typing import Optional, Union, List, Callable, Dict, Tuple, Set

__all__ = ['OptionsBase', 'EmptyOptions', ]


class _OptionDescriptor:

    def __set_name__(self, owner: type, name: str):
        self.name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            raise AttributeError

        if owner is None:
            owner = instance.__class__

        class_attr: str = 'valid_options'
        instance_attr: str = '__options_dict__'
        key_list: str = 'key_list'

        if hasattr(owner, class_attr) and hasattr(instance, instance_attr):
            dictionary: Dict
            instance_attr = instance.__getattribute__(instance_attr)
            if isinstance(instance_attr, dict):
                dictionary: Dict = instance_attr
            else:
                raise AttributeError

            if self.name in dictionary.keys():
                return dictionary[self.name]

            if hasattr(instance, key_list):
                key_list: List[str] = instance.__getattribute__(key_list)
                if self.name in key_list:
                    return None

            options = owner.__getattribute__(owner, class_attr)
            option_list: 'List[Union[Toggle, Prefixed, KWOption, ListOption]]' = []
            if hasattr(options, '__func__'):
                option_list = options.__func__()
            elif callable(options):
                option_list = options()
            elif isinstance(options, (tuple, list)):
                option_list = options

            for opt in option_list:
                key: str = opt.key.replace('-', '_')
                if key == self.name:
                    return None

        raise AttributeError

    def __set__(self, instance, value):
        owner = instance.__class__
        class_attr: str = 'valid_options'
        instance_attr: str = '__options_dict__'
        key_list: str = 'key_list'

        if hasattr(owner, class_attr) and hasattr(instance, instance_attr):
            dictionary: Dict
            instance_attr = instance.__getattribute__(instance_attr)
            if isinstance(instance_attr, dict):
                dictionary: Dict = instance_attr
            else:
                raise AttributeError

            if self.name in dictionary.keys():
                dictionary[self.name] = value
                return

            if hasattr(instance, key_list):
                key_list: List[str] = instance.__getattribute__(key_list)
                if self.name in key_list:
                    dictionary[self.name] = value
                    return

            options = owner.__getattribute__(owner, class_attr)
            option_list: 'List[Union[Toggle, Prefixed, KWOption, ListOption]]' = []
            if hasattr(options, '__func__'):
                option_list = options.__func__()
            elif callable(options):
                option_list = options()
            elif isinstance(options, (tuple, list)):
                option_list = options

            for opt in option_list:
                key: str = opt.key.replace('-', '_')
                if key == self.name:
                    dictionary[self.name] = value
                    return

        raise AttributeError


class OptionsMeta(type):

    def __new__(mcs: type, clsname, bases, classdict):
        attr_name: str = 'valid_options'
        valid_options_list: 'List[Union[Toggle, Prefixed, KWOption, ListOption]]' = []
        empty_list: 'Callable[[], List[Union[Toggle, Prefixed, KWOption, ListOption]]]' = lambda: []

        if attr_name in classdict.keys():
            if hasattr(classdict[attr_name], '__func__'):
                valid_options_list = classdict[attr_name].__func__()
            elif callable(classdict[attr_name]):
                valid_options_list = classdict[attr_name]()
            elif isinstance(classdict[attr_name], (tuple, list)):
                valid_options_list = list(classdict[attr_name])

        for base in bases:
            if base.__class__ == mcs:
                if hasattr(base, attr_name):
                    inherited_options = base.__getattribute__(base, attr_name)
                else:
                    inherited_options = empty_list
                valid_options_list.extend(inherited_options())

        valid_options: 'Callable[[], List[Union[Toggle, Prefixed, KWOption, ListOption]]]'

        def valid_options():
            return valid_options_list

        classdict[attr_name] = valid_options
        for option in valid_options_list:
            key: str = option.key.replace('-', '_')
            classdict[key] = _OptionDescriptor()

        customized = super().__new__(mcs, clsname, bases, classdict)
        return customized


class OptionsBase(metaclass=OptionsMeta):

    def __init__(self, **kwargs):
        self.__options_dict__: \
            'Dict[str, Tuple[Union[Toggle, Prefixed, KWOption, ListOption], Optional[Union[bool, str, List]]]]' = {}
        self._key_set: Optional[Set] = None
        update_set = set(kwargs.keys()).intersection(self.key_set)
        for key in update_set:
            self.__options_dict__[key] = kwargs[key]

    def to_dictionary(self) -> 'Dict':
        return self.__options_dict__.copy()

    def set_options(self, **kwargs) -> None:
        for option, value in kwargs.items():
            self.__setattr__(option, value)

    @property
    def key_set(self) -> 'Set[str]':
        if (self._key_set is None) or not bool(self._key_set):
            self._key_set = {opt.key.replace('-', '_') for opt in self.__class__.valid_options()}
        return self._key_set

    @staticmethod
    def valid_options() -> 'List[Union[Toggle, Prefixed, KWOption, ListOption]]':
        return []


class EmptyOptions(OptionsBase):
    pass
