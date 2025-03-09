"""
System commands for the calculator REPL.
"""
import logging
import sys
from typing import Dict
from app.commands.base import Command

logger = logging.getLogger("calculator.commands.system")

class HelpCommand(Command):
    """Command to display help information."""
    def __init__(self, command_registry):
        """
        Initialize the help command with access to the command registry.
        
        Args:
            command_registry: Dictionary of available commands
        """
        self.command_registry = command_registry
    
    def execute(self, *args) -> str:
        """
        Execute the help command.
        
        Returns:
            String containing help information for all commands
        """
        logger.info("Displaying help information")
        help_text = "Available commands:\n"
        for cmd_name, cmd in sorted(self.command_registry.items()):
            # Skip duplicate aliases
            if cmd_name == "exit" and "quit" in self.command_registry and id(cmd) == id(self.command_registry["quit"]):
                continue
            if cmd_name == "menu" and "help" in self.command_registry and id(cmd) == id(self.command_registry["help"]):
                continue
                
            help_text += f"  {cmd.get_help()}\n"
        return help_text
    
    def get_help(self) -> str:
        """Get the help text for the help command."""
        return "help - Display this help message"

class QuitCommand(Command):
    """Command to exit the calculator."""
    def execute(self, *args) -> None:
        """
        Execute the quit command.
        
        This will exit the program.
        """
        logger.info("Exiting calculator")
        print("Thank you for using the Advanced Calculator!")
        sys.exit(0)
    
    def get_help(self) -> str:
        """Get the help text for the quit command."""
        return "quit - Exit the calculator"