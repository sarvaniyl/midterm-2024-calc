# app/plugins/plugin_loader.py
import importlib
import inspect
import logging
import pkgutil
from typing import Dict, List, Type

from app.commands.base import Command

logger = logging.getLogger(__name__)

class PluginLoader:
    """
    A class that dynamically loads plugins from specified directories.
    This class follows the Singleton pattern to ensure only one instance exists.
    """
    _instance = None

    def __init__(self):
        self.plugins = {}
        self.commands = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PluginLoader, cls).__new__(cls)
        return cls._instance
    def load_plugins(self, package_name: str = "app.plugins") -> Dict[str, object]:
        """
        Dynamically loads all plugins from the specified package.

        Args:
            package_name: The package name to search for plugins

        Returns:
            A dictionary of loaded plugins
        """
        logger.info("Loading plugins from %s", package_name)

        package = importlib.import_module(package_name)

        for _, name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
            if is_pkg and not name.endswith('__pycache__'):
                try:
                    # Import the module
                    module = importlib.import_module(name)
                    logger.debug("Loaded module: %s", name)

                    # Look for command classes in the module
                    self._register_commands_from_module(module)

                except ImportError as e:
                    logger.error("Failed to load plugin %s: %s", name, str(e))

        logger.info("Loaded %d commands from plugins", len(self.commands))
        return self.commands

    def _register_commands_from_module(self, module):
        """
        Register all Command subclasses from a module.

        Args:
            module: The module to search for Command subclasses
        """
        for _, obj in inspect.getmembers(module, inspect.isclass):
            # Check if the class is a subclass of Command but not Command itself
            if issubclass(obj, Command) and obj is not Command:
                # Get the command name from the class
                command_name = getattr(obj, 'name', obj.__name__.lower())
                logger.debug("Registering command: %s", command_name)
                self.commands[command_name] = obj
                # Get the command name from the class
    def get_command_list(self) -> List[str]:
        """
        Returns a list of all available command names.

        Returns:
            A list of command names
        """
        return sorted(self.commands.keys())

    def get_command(self, command_name: str) -> Type[Command]:
        """
        Get a command class by name.

        Args:
            command_name: The name of the command to get

        Returns:
            The command class if found, otherwise None
        """
        return self.commands.get(command_name.lower())
