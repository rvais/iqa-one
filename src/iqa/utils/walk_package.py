import importlib
import inspect
from importlib import resources
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Union, Type, List, Any, Iterator
    from os import PathLike


def walk_package_and_import(
        package_path: Union[PathLike[Any], str],
        superclass: Optional[Type] = None,
        skip_modules: Optional[List[PathLike[Any]]] = None
) -> List[Type]:
    """Recursively walk the supplied package to retrieve all plugins
       :param package_path: path to package that is supposed to be iterated
       over to find and import submodules. Usually it is __path__ variable
       of the file that calls this function.
       :param superclass: 'Type' object that represents
       :param skip_modules: list of paths of packages to be skipped and not imported again
       :return imported types
    """

    results: List[type] = []

    if skip_modules is None:
        skip_modules = []

    files: Iterator[str] = resources.contents(package_path)
    modules: List[str] = [f[:-3] for f in files if f.endswith(".py") and f[0] != "_"]
    submodules: List[str] = [f[:-3] for f in files if not f.endswith(".py")]

    # Filter out submodules to skip
    for skip in skip_modules:
        submodules = [subm for subm in submodules if not subm.startswith(skip)]

    # import modules from subpackages/submodules
    for subm in submodules:
        results.extend(walk_package_and_import(subm, superclass, skip_modules))

    for mod in modules:
        imported = importlib.import_module(mod)
        classes = inspect.getmembers(imported, inspect.isclass)
        if superclass is not None:
            results.extend([cls for _, cls in classes if isinstance(cls, superclass)])

    return results
