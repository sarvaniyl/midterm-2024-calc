"""
Plugin loader for the calculator application.
"""
import os
import logging
import importlib.util
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger("calculator.plugins")

class PluginLoader:
    """
    Loads and manages plugins for the calculator application.
    """
    def __init__(self):
        """
        Initialize the plugin loader with a plugin directory from environment variables.
        """
        self.plugin_dir = os.environ.get("PLUGIN_DIR", "app/plugins")
        self.plugins = {}
        logger.info(f"Plugin loader initialized with directory: {self.plugin_dir}")
    
    def load_plugins(self) -> Dict[str, Any]:
        """
        Load plugins from the plugin directory and its subdirectories.
        
        Returns:
            Dictionary mapping command names to command objects
        """
        plugin_commands = {}
        plugin_dir_path = Path(self.plugin_dir)
        
        if not plugin_dir_path.exists():
            logger.info(f"Creating plugin directory: {self.plugin_dir}")
            plugin_dir_path.mkdir(parents=True, exist_ok=True)
            return plugin_commands
        
        # Find all plugin modules in plugin directory and subdirectories
        plugin_files = []
        for subdir in [d for d in plugin_dir_path.iterdir() if d.is_dir() and not d.name.startswith("__")]:
            plugin_files.extend(subdir.glob("*_plugin.py"))
        
        for plugin_file in plugin_files:
            try:
                logger.info(f"Loading plugin: {plugin_file}")
                module_name = f"app.plugins.{plugin_file.parent.name}.{plugin_file.stem}"
                spec = importlib.util.spec_from_file_location(module_name, plugin_file)
                plugin_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(plugin_module)
                
                if hasattr(plugin_module, "register_commands"):
                    new_commands = plugin_module.register_commands()
                    plugin_commands.update(new_commands)
                    logger.info(f"Registered commands from plugin {plugin_file.stem}: {list(new_commands.keys())}")
                else:
                    logger.warning(f"Plugin {plugin_file} does not have a register_commands function")
            except Exception as e:
                logger.error(f"Error loading plugin {plugin_file}: {str(e)}")
        
        return plugin_commands