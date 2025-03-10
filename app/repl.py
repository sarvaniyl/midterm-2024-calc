# app/repl.py
import logging
from typing import Dict, Optional, Type
import os
from dotenv import load_dotenv
from app.calculator import Calculator
from app.commands.arithmetic import AddCommand, SubtractCommand, MultiplyCommand, DivideCommand
from app.commands.base import Command
from app.commands.history import HistoryCommand, ClearHistoryCommand, DeleteCommand
from app.commands.system import ExitCommand, HelpCommand
from app.plugins.csv.csv_plugin import ImportCSVCommand, ExportCSVCommand
from app.plugins.plugin_loader import PluginLoader

logger = logging.getLogger(__name__)

class REPL:
    """
    Read-Eval-Print Loop for the calculator application.
    This class follows the Facade pattern to provide a simplified interface
    for interacting with the calculator and its commands.
    """
    
    def __init__(self):
        self.calculator = Calculator()
        self.running = False
        self._commands = self._register_builtin_commands()
        self._load_plugin_commands()
        logger.info("REPL initialized")
        
    def _register_builtin_commands(self) -> Dict[str, Type[Command]]:
        """Register built-in commands."""
        commands = {
            # Arithmetic commands
            'add': AddCommand,
            'subtract': SubtractCommand,
            'multiply': MultiplyCommand,
            'divide': DivideCommand,
            
            # History commands
            'history': HistoryCommand,
            'clear': ClearHistoryCommand,
            'delete': DeleteCommand,
            
            # System commands
            'exit': ExitCommand,
            'quit': ExitCommand,  # Alias for exit
            'help': HelpCommand,
            
            "export_csv": ExportCSVCommand,
            "import_csv": ImportCSVCommand,


        }
        
        logger.debug(f"Registered {len(commands)} built-in commands")
        return commands
    
    def _load_plugin_commands(self):
        """Load commands from plugins."""
        plugin_loader = PluginLoader()
        plugin_commands = plugin_loader.load_plugins()
        
        # Update commands with plugin commands
        self._commands.update(plugin_commands)
        logger.info(f"Loaded {len(plugin_commands)} commands from plugins")
    
    # Modify this method in app/repl.py
    def get_command(self, command_name: str) -> Optional[Command]:
        """
        Get a command by name.
        
        Args:
            command_name: The name of the command to get
            
        Returns:
            An instance of the command if found, otherwise None
        """
        command_class = self._commands.get(command_name.lower())
        if command_class:
            # Create a new instance of the command with the calculator
            return command_class(self.calculator)
        return None
    def get_command_list(self):
        """Get a list of all available command names."""
        return sorted(self._commands.keys())
    
    def parse_input(self, user_input: str) -> tuple:
        """
        Parse user input into command and arguments.
        
        Args:
            user_input: The raw user input
            
        Returns:
            A tuple containing the command name and a list of arguments
        """
        parts = user_input.strip().split()
        if not parts:
            return None, []
        
        command_name = parts[0].lower()
        args = parts[1:]
        return command_name, args
    
    def run(self):
        """Run the REPL loop."""
        self.running = True
        print("Advanced Calculator")
        print("Type 'help' for a list of commands, 'exit' to quit")
        
        while self.running:
            try:
                # Read
                user_input = input("> ")
                
                # Parse
                command_name, args = self.parse_input(user_input)
                if not command_name:
                    continue
                
                # Get command
                command = self.get_command(command_name)
                if not command:
                    print(f"Unknown command: {command_name}")
                    print("Type 'help' for a list of commands")
                    continue
                
                # Execute
                logger.info(f"Executing command: {command_name} with args: {args}")
                result = command.execute(*args)
                
                # Print
                print(result)
                
            except KeyboardInterrupt:
                print("\nExiting...")
                self.running = False
            except Exception as e:
                logger.error(f"Error in REPL: {str(e)}")
                print(f"Error: {str(e)}")
    
    def stop(self):
        """Stop the REPL loop."""
        self.running = False
        logger.info("REPL stopped")