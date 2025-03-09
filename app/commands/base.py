"""
Base command classes for the calculator REPL.
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

logger = logging.getLogger("calculator.commands")

class Command(ABC):
    """
    Abstract base class for all calculator commands.
    Implements the Command pattern.
    """
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the command with the given arguments.
        
        Args:
            *args: Positional arguments for the command
            **kwargs: Keyword arguments for the command
            
        Returns:
            The result of the command execution
        """
        pass
    
    @abstractmethod
    def get_help(self) -> str:
        """
        Get the help text for the command.
        
        Returns:
            Help text string
        """
        pass

class CommandFactory:
    """
    Factory for creating command instances.
    Implements the Factory Method pattern.
    """
    @staticmethod
    def create_command(command_name: str, command_registry: Dict[str, Command]) -> Command:
        """
        Create a command instance based on the command name.
        
        Args:
            command_name: The name of the command
            command_registry: Dictionary mapping command names to command objects
            
        Returns:
            Command instance
            
        Raises:
            ValueError: If the command is not found in the registry
        """
        logger.debug(f"Creating command: {command_name}")
        if command_name in command_registry:
            return command_registry[command_name]
        else:
            logger.warning(f"Unknown command: {command_name}")
            raise ValueError(f"Unknown command: {command_name}")