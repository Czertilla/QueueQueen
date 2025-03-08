import pkgutil
import importlib


def load_common[T](
    package_name: str, attr_name: str, expected_type: type[T]
) -> list[T]:
    """
    Dynamically loads all modules in the given package and extracts common objects
    with a specified attribute name.

    Args:
        package_name (str): Name of the package (e.g., "bot.routers" or "app.api.v1"), use __name__.
        attr_name (str): Name of the attribute in each module (e.g., "router").
        expected_type (T): Expected type of the attribute (e.g., aiogram.Router or fastapi.APIRouter).

    Returns:
        List of found objects matching the expected type.
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
