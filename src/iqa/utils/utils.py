from typing import Any


def remove_prefix(string, prefix) -> str:
    if string.startswith(prefix):
        return string[len(prefix):]
    else:
        return string


def get_subclasses(given_name: str, in_class: Any, in_class_property: str = '__name__') -> Any:
    """
    Get class of given class or class property from class subclasses

    Args:
        given_name: Which string should be match
        in_class: In which which class to search
        in_class_property: in_class property for compare with class_name (default is class-name __name__)

    Returns: Any

    """
    if hasattr(in_class, '__subclasses__'):
        for cls in in_class.__subclasses__():  # type: Any
            if getattr(cls, in_class_property) == given_name:
                return cls  # type: Any

    raise ValueError('The name "%s" not found as a subclasses of %s' % (given_name, in_class))

