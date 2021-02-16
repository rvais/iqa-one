import importlib
import inspect
from importlib import resources
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Union, Type, List, Any, Set
    from os import PathLike


def walk_package_and_import(
        package_path: 'Union[PathLike[Any], str]',
        superclass: 'Optional[Type]' = None,
        skip_modules: 'Optional[List[PathLike[Any]]]' = None,
        current_depth: int = 0,
        max_depth: int = 2
) -> 'List[Type]':
    """Recursively walk the supplied package to retrieve all plugins
       :param package_path: path to package that is supposed to be iterated
       over to find and import submodules. Usually it is __path__ variable
       of the file that calls this function.
       :param superclass: 'Type' object that represents
       :param skip_modules: list of paths of packages to be skipped and not imported again
       :param current_depth: current package depth
       :param max_depth: how deep to go to discover new subpackages
       :return imported types
    """

    results: Set[type] = set()

    if current_depth > max_depth:
        return []

    if skip_modules is None:
        skip_modules = []

    if isinstance(package_path, list):
        for pp in package_path:
            results.update(walk_package_and_import(pp, superclass, skip_modules))
        return list(results)

    files: List[str] = list(resources.contents(package_path))

    modules: List[str] = [f[:-3] for f in files if f.endswith(".py") and f[0] != "_"]
    subpackages: List[str] = [f for f in files if not f.endswith(".py")]

    # import modules from subpackages/submodules
    for subpkg in subpackages:
        subpackage_path: str = f"{package_path}.{subpkg}"
        if subpackage_path in skip_modules:
            continue
        results.update(walk_package_and_import(subpackage_path, superclass, skip_modules, current_depth + 1, max_depth))
        skip_modules.append(subpackage_path)

    for mod in modules:
        module_path: str = f"{package_path}.{mod}"
        if module_path in skip_modules:
            continue

        imported = importlib.import_module(module_path)
        classes = inspect.getmembers(imported, inspect.isclass)
        if superclass is not None:
            results.update([cls for _, cls in classes if issubclass(cls, superclass) and not inspect.isabstract(cls)])

    return list(results)
