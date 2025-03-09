# app/commands/system.py
import logging
import sys
from typing import List

from app.commands.base import Command

logger = logging.getLogger(__name__)

class ExitCommand(Command):
    """Command to exit the application."""
    name = "exit"
    help = "Exit the application"
    
    def execute(self, *args) -> str:
        from app.repl import REPL
        
        # Get the REPL instance
        repl = REPL()
        repl.stop()
        
        return "Exiting application"

class HelpCommand(Command):
    """Command to display help information."""
    name = "help"
    help = "Display help information"
    
    def execute(self, *args) -> str:
        from app.repl import REPL
        
        logger.info("Displaying help information")
        
        # Get the REPL instance
        repl = REPL()
        commands = repl.get_command_list()
        
        # If a specific command is requested
        if args:
            cmd_name = args[0].lower()
            cmd = repl.get_command(cmd_name)
            if cmd:
                return f"{cmd_name}: {cmd.help}"
            else:
                return f"Unknown command: {cmd_name}"
        
        # Otherwise list all commands
        result = "Available commands:\n"
        
        # Get all command instances
        command_instances = {name: repl.get_command(name) for name in commands}
        
        # Group commands by category
        categories = {
            "Arithmetic": ["add", "subtract", "multiply", "divide"],
            "History": ["history", "clear", "delete"],
            "System": ["exit", "quit", "help", "menu"],
            "Plugins": [cmd for cmd in commands if cmd not in ["add", "subtract", "multiply", "divide", 
                                                               "history", "clear", "delete", 
                                                               "exit", "quit", "help", "menu"]]
        }
        
        # Format help text
        for category, cmd_names in categories.items():
            if cmd_names:  # Only show category if it has commands
                result += f"\n{category}:\n"
                for name in sorted(cmd_names):
                    if name in command_instances and command_instances[name]:
                        result += f"  {name}: {command_instances[name].help}\n"
        
        return result.strip()

class MenuCommand(Command):
    """Command to display available commands."""
    name = "menu"
    help = "Display available commands"
    
    def execute(self, *args) -> str:
        from app.repl import REPL
        
        # Get the REPL instance
        repl = REPL()
        commands = repl.get_command_list()
        
        result = "Available commands:\n"
        result += ", ".join(sorted(commands))
        
        return result