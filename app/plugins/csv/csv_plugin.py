# app/plugins/csv/csv_plugin.py
import logging
import os
import pandas as pd
from typing import List, Optional

from app.commands.base import Command
from app.history_manager import HistoryManager

logger = logging.getLogger(__name__)
from pathlib import Path
cwd = Path.cwd()
dir = os.path.dirname(__file__)

class ExportCSVCommand(Command):
    """Command to export calculation history to a CSV file."""
    name = "export_csv"
    help = "Export calculation history to a CSV file (export_csv <filename>)"
    
    def execute(self, *args) -> str:
        if not args:
            return "Error: Please provide a filename for export"
        
        filename = args[0]
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        # Construct path to ../plugins/data directory
        #data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'plugins', 'data')
        data_dir = os.path.join(dir,"..", "Data")
        filename = os.path.join(data_dir, filename)
            
        history_manager = HistoryManager()
        history = history_manager.get_history()
        
        if history.empty:
            return "No history to export"
        
        try:
            # Create data directory if it doesn't exist
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                
            history.to_csv(filename, index=False)
            logger.info(f"Exported history to {filename}")
            return f"History exported to {filename}"
        except Exception as e:
            logger.error(f"Failed to export CSV: {str(e)}")
            return f"Error exporting CSV: {str(e)}"


class ImportCSVCommand(Command):
    """Command to import calculation history from a CSV file."""
    name = "import_csv"
    help = "Import calculation history from a CSV file (import_csv <filename>)"
    
    def execute(self, *args) -> str:
        if not args:
            return "Error: Please provide a filename to import"
        
        filename = args[0]
        data_dir = os.path.join(dir,"..", "Data")
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
            
            logger.info(f"Imported history from {filename}")
            return f"History imported from {filename} with {len(data)} records"
        except Exception as e:
            logger.error(f"Failed to import CSV: {str(e)}")
            return f"Error importing CSV: {str(e)}"