from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Set, Any, Type


def remove_prefix(string, prefix) -> str:
    if string.startswith(prefix):
        return string[len(prefix):]
    else:
        return string


def get_all_subclasses(cls: Type) -> Set[Type]:
    """
    Recursively returns all know subclasses of given class as a Set

    Args:
        cls: Superclass type

    Returns: List[Type], list of subclasses
    """
    return set(cls.__subclasses__()).union(
        [subcls for clss in cls.__subclasses__() for subcls in get_all_subclasses(clss)])


def get_subclass_with_prop_value(superclass: Type, cls_property_val: Any, in_class_property: str = '__name__') -> Type:
    """
    Returns subclass of given class based on supplied class property from class subclasses

    Args:
        superclass: In which which class to search
        cls_property_val: Expected value contained by property supplied by name
        in_class_property: in_class property for compare with class_name (default is class-name __name__)

    Returns: Type (class)
    """
    if hasattr(superclass, '__subclasses__'):
        for cls in get_all_subclasses(superclass):
            if getattr(cls, in_class_property) == cls_property_val:
                return cls

    raise ValueError('A subclass with "%s" value of "%s" property not found as subclasses of %s' % (cls_property_val, in_class_property, superclass))


def get_subclass(superclass: Type, name: str) -> Type:
    """
    Returns subclass of given class based on supplied class property from class subclasses

    Args:
        superclass: In which which class to search
        name: name of the subclass

    Returns: Type (class)
    """
    return get_subclass_with_prop_value(superclass, cls_property_val=name)


