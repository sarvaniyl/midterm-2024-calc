import logging
from app import App

if __name__ == "__main__":
    try:
        logging.info("Starting the application...")
        app = App()
        app.start()
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}", exc_info=True)
