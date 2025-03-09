# app/plugins/csv/csv_plugin.py
import logging
import os
import pandas as pd
from typing import List, Optional

from app.commands.base import Command
from app.history_manager import HistoryManager

logger = logging.getLogger(__name__)

class ExportCSVCommand(Command):
    """Command to export calculation history to a CSV file."""
    name = "export_csv"
    help = "Export calculation history to a CSV file"
    
    def execute(self, *args) -> str:
        if not args:
            return "Error: Please provide a filename for export"
        
        filename = args[0]
        if not filename.endswith('.csv'):
            filename += '.csv'
            
        history_manager = HistoryManager()
        history = history_manager.get_history()
        
        if history.empty:
            return "No history to export"
        
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            history.to_csv(filename, index=False)
            logger.info(f"Exported history to {filename}")
            return f"History exported to {filename}"
        except Exception as e:
            logger.error(f"Failed to export CSV: {str(e)}")
            return f"Error exporting CSV: {str(e)}"


class ImportCSVCommand(Command):
    """Command to import calculation history from a CSV file."""
    name = "import_csv"
    help = "Import calculation history from a CSV file"
    
    def execute(self, *args) -> str:
        if not args:
            return "Error: Please provide a filename to import"
        
        filename = args[0]
        
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
            
            logger.info(f"Imported history from {filename}")
            return f"History imported from {filename} with {len(data)} records"
        except Exception as e:
            logger.error(f"Failed to import CSV: {str(e)}")
            return f"Error importing CSV: {str(e)}"