# main.py
import logging
import os
import sys
from dotenv import load_dotenv

from app.repl import REPL
from app.plugins.plugin_loader import PluginLoader

def configure_logging():
    """Configure logging based on environment variables."""
    # Load environment variables
    load_dotenv()
    
    # Get log level from environment variable or default to INFO
    log_level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    
    # Get log file from environment variable or default to None (console only)
    log_file = os.getenv('LOG_FILE', '')
    
    # Configure logging
    handlers = []
    
    # Always log to console
    console_handler = logging.StreamHandler(sys.stdout)
    handlers.append(console_handler)
    
    # Log to file if specified
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_handler = logging.FileHandler(log_file)
        handlers.append(file_handler)
    
    # Configure logging format and level
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    
    logging.info(f"Logging configured with level: {log_level_name}")
    if log_file:
        logging.info(f"Logging to file: {log_file}")

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

