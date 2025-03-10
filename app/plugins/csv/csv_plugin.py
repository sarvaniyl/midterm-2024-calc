"""CSV plugin for importing and exporting calculation history."""
import logging
import os
from pathlib import Path

import pandas as pd
from app.commands.base import Command
from app.history_manager import HistoryManager

logger = logging.getLogger(__name__)
file_dir = os.path.dirname(__file__)

class ExportCSVCommand(Command):
    """Command to export calculation history to a CSV file."""
    """Command to export calculation history to a CSV file."""
    name = "export_csv"
    help = "Export calculation history to a CSV file (export_csv <filename>)"

    def execute(self, *args) -> str:
        if not args:
            return "Error: Please provide a filename for export"

        filename = args[0]
        if not filename.endswith('.csv'):
            filename += '.csv'

        data_dir = os.path.join(file_dir, "..", "Data")
        filename = os.path.join(data_dir, filename)

        history_manager = HistoryManager()
        history = history_manager.get_history()

        if history.empty:
            return "No history to export"

        try:
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            history.to_csv(filename, index=False)
            logger.info("Exported history to %s", filename)
            return f"History exported to {filename}"
        except OSError as err:
            logger.error("Failed to export CSV: %s", str(err))
            return f"Error exporting CSV: {str(err)}"

class ImportCSVCommand(Command):
    """Command to import calculation history from a CSV file."""
    name = "import_csv"
    help = "Import calculation history from a CSV file (import_csv <filename>)"

    def execute(self, *args) -> str:
        if not args:
            return "Error: Please provide a filename to import"

        filename = args[0]
        data_dir = os.path.join(file_dir, "..", "Data")
        filename = os.path.join(data_dir, filename)

        if not os.path.exists(filename):
            return f"Error: File {filename} does not exist"

        try:
            data = pd.read_csv(filename)
            required_columns = ['operation', 'expression', 'result']

            # Check if required columns exist
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                return f"Error: CSV is missing required columns: {', '.join(missing_columns)}"

            history_manager = HistoryManager()
            # Clear existing history and load the new one
            history_manager.set_history(data)

            logger.info("Imported history from %s", filename)
            return f"History imported from {filename} with {len(data)} records"
        except OSError as err:
            logger.error("Failed to import CSV: %s", str(err))
            return f"Error importing CSV: {str(err)}"