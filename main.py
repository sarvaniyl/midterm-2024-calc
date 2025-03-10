# main.py
import logging
import logging.config
import os
import yaml
from dotenv import load_dotenv
from app.repl import REPL
from app.plugins.plugin_loader import PluginLoader
import re


def expand_env_vars(config):
    """Recursively expand environment variables in the logging config."""
    if isinstance(config, dict):
        return {key: expand_env_vars(value) for key, value in config.items()}
    elif isinstance(config, list):
        return [expand_env_vars(item) for item in config]
    elif isinstance(config, str):
        # Replace ${VAR} with os.getenv(VAR, VAR) to use defaults if not set
        return re.sub(r"\$\{(\w+)\}", lambda match: os.getenv(match.group(1), match.group(0)), config)
    else:
        return config

def configure_logging():
    """Configure logging using YAML configuration with expanded environment variables."""
    
    # Load environment variables
    load_dotenv()

    # Ensure logs directory exists
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Load and expand environment variables in YAML config
    with open('logging.yaml', 'r') as f:
        config = yaml.safe_load(f)
        config = expand_env_vars(config)  # Expand environment variables

    # Convert numeric values explicitly
    for handler in config.get("handlers", {}).values():
        if "maxBytes" in handler:
            handler["maxBytes"] = int(handler["maxBytes"])
        if "backupCount" in handler:
            handler["backupCount"] = int(handler["backupCount"])

    # Configure logging
    logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)
    logger.info("Logging configured from YAML file")

# Call the function to configure logging
configure_logging()

def main():
    """Main entry point for the calculator application."""
    # Configure logging
    configure_logging()
    
    # Create a logger for this module
    logger = logging.getLogger(__name__)
    logger.info("Starting Advanced Calculator Application")
    
    # Load plugins
    plugin_loader = PluginLoader()
    plugin_loader.load_plugins()
    
    # Start REPL
    repl = REPL()
    repl.run()
    
    logger.info("Calculator application exiting")

if __name__ == "__main__":
    main()

