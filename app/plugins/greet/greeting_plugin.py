# app/plugins/greet/greeting_plugin.py
import logging
import datetime
from typing import List

from app.commands.base import Command

logger = logging.getLogger(__name__)

class GreetCommand(Command):
    """Command to display a greeting message."""
    name = "greet"
    help = "Display a greeting message"
    
    def execute(self, *args) -> str:
        name = args[0] if args else "User"
        current_hour = datetime.datetime.now().hour
        
        if 5 <= current_hour < 12:
            greeting = "Good morning"
        elif 12 <= current_hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        message = f"{greeting}, {name}! Welcome to the Advanced Calculator."
        logger.info(f"Greeted user: {name}")
        return message


class HelpPluginCommand(Command):
    """Command to display help for all plugin commands."""
    name = "plugin_help"
    help = "Display help for all plugin commands"
    
    def execute(self, *args) -> str:
        from app.plugins.plugin_loader import PluginLoader
        
        plugin_loader = PluginLoader()
        commands = plugin_loader.commands
        
        if not commands:
            return "No plugin commands available"
        
        # If a specific command is requested
        if args:
            cmd_name = args[0].lower()
            cmd_class = commands.get(cmd_name)
            if cmd_class:
                return f"{cmd_name}: {cmd_class.help}"
            else:
                return f"Unknown command: {cmd_name}"
        
        # Otherwise list all commands
        result = "Available plugin commands:\n"
        result += "\n".join([f"{name}: {cmd.help}" for name, cmd in sorted(commands.items())])
        
        return result