import pkgutil
import importlib
from typing import TypeVar, List


def load_common[T](package_name: str, attr_name: str, expected_type: type[T]) -> List[T]:
    """
    Dynamically loads all modules in the given package and extracts common objects 
    with a specified attribute name.    

    :param package_name: Name of the package (e.g., "bot.routers" or "app.api.v1"), use __name__.
    :param attr_name: Name of the attribute in each module (e.g., "router").
    :param expected_type: Expected type of the attribute (e.g., aiogram.Router or fastapi.APIRouter).
    :return: List of found objects matching the expected type.
    """
    found_objects = []

    # Import the package and iterate over its modules
    package = importlib.import_module(package_name)
    
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")

        if hasattr(module, attr_name):
            obj = getattr(module, attr_name)
            if isinstance(obj, expected_type):
                found_objects.append(obj)

    return found_objects
