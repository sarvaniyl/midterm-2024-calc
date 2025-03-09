# main.py
import logging
import os
import sys
import yaml
from dotenv import load_dotenv

from app.repl import REPL
from app.plugins.plugin_loader import PluginLoader
def configure_logging():
    """Configure logging using YAML configuration."""
    import yaml
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Load logging configuration
    with open('logging.yaml', 'r') as f:
        config = yaml.safe_load(f)
        
    # Configure logging using the YAML configuration
    import logging.config
    logging.config.dictConfig(config)
    
    logging.info("Logging configured from YAML file")
        

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

