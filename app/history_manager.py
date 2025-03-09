# app/history_manager.py
import logging
import os
import pandas as pd
from typing import Any

logger = logging.getLogger(__name__)

__all__ = ['HistoryManager']

class HistoryManager:
    """
    Manages the calculation history using Pandas.
    This class follows the Singleton pattern to ensure only one instance exists.
    """
    
    _instance = None
    _history = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HistoryManager, cls).__new__(cls)
            
            # Initialize empty history DataFrame
            cls._instance._history = pd.DataFrame(columns=['operation', 'expression', 'result'])
            
            # Try to load history from environment variable if specified
            cls._instance._try_load_history_from_env()
            
            logger.info("HistoryManager initialized")
        return cls._instance
    
    def _try_load_history_from_env(self):
        """Try to load history from a file specified in the environment variable."""
        history_file = os.getenv('HISTORY_FILE', '')
        if history_file and os.path.exists(history_file):
            try:
                self.load_history(history_file)
                logger.info(f"Loaded history from {history_file}")
            except Exception as e:
                logger.error(f"Failed to load history from {history_file}: {str(e)}")
    
    def add_entry(self, operation: str, expression: str, result: Any) -> None:
        """
        Add a new entry to the history.
        
        Args:
            operation: The operation performed (e.g., 'add', 'subtract')
            expression: The expression that was evaluated
            result: The result of the calculation
        """
        try:
            # Convert result to string to ensure compatibility
            result_str = str(result)
            
            new_entry = pd.DataFrame({
                'operation': [operation],
                'expression': [expression],
                'result': [result_str]
            })
            
            # Append the new entry
            self._history = pd.concat([self._history, new_entry], ignore_index=True)
            
            # Try to save history if environment variable is set
            self._try_save_history_to_env()
            
            logger.info(f"Added history entry: {operation} {expression} = {result_str}")
        except Exception as e:
            logger.error(f"Error adding history entry: {str(e)}")
            raise ValueError(f"Could not add history entry: {str(e)}")
    
    def get_history(self) -> pd.DataFrame:
        """
        Get the current history DataFrame.
        
        Returns:
            The history DataFrame
        """
        return self._history.copy()
    
    def set_history(self, history: pd.DataFrame) -> None:
        """
        Set the history DataFrame.
        
        Args:
            history: The new history DataFrame
        """
        # Validate the DataFrame has required columns
        required_columns = ['operation', 'expression', 'result']
        if not all(col in history.columns for col in required_columns):
            raise ValueError(f"History DataFrame must have columns: {', '.join(required_columns)}")
        
        self._history = history.copy()
        logger.info(f"Set history with {len(history)} entries")
        
        # Try to save history if environment variable is set
        self._try_save_history_to_env()
    
    def clear_history(self) -> None:
        """Clear the history."""
        self._history = pd.DataFrame(columns=['operation', 'expression', 'result'])
        logger.info("Cleared history")
        
        # Try to save empty history if environment variable is set
        self._try_save_history_to_env()
    
    def delete_entry(self, index: int) -> bool:
        """
        Delete an entry from the history by index.
        
        Args:
            index: The index of the entry to delete (0-based)
            
        Returns:
            True if the entry was deleted, False otherwise
        """
        try:
            # Check if index is valid
            if index < 0 or index >= len(self._history):
                logger.warning(f"Invalid history index: {index}")
                return False
            
            # Delete the entry
            self._history = self._history.drop(index).reset_index(drop=True)
            logger.info(f"Deleted history entry at index {index}")
            
            # Try to save history if environment variable is set
            self._try_save_history_to_env()
            
            return True
        except Exception as e:
            logger.error(f"Error deleting history entry: {str(e)}")
            return False
    
    def save_history(self, filename: str) -> bool:
        """
        Save the history to a CSV file.
        
        Args:
            filename: The filename to save to
            
        Returns:
            True if the history was saved, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            self._history.to_csv(filename, index=False)
            logger.info(f"Saved history to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving history: {str(e)}")
            return False
    
    def load_history(self, filename: str) -> bool:
        """
        Load the history from a CSV file.
        
        Args:
            filename: The filename to load from
            
        Returns:
            True if the history was loaded, False otherwise
        """
        try:
            if not os.path.exists(filename):
                logger.warning(f"History file not found: {filename}")
                return False
                
            history = pd.read_csv(filename)
            
            # Validate the DataFrame has required columns
            required_columns = ['operation', 'expression', 'result']
            missing_columns = [col for col in required_columns if col not in history.columns]
            if missing_columns:
                logger.error(f"History file missing columns: {', '.join(missing_columns)}")
                return False
            
            self._history = history
            logger.info(f"Loaded history from {filename} with {len(history)} entries")
            return True
        except Exception as e:
            logger.error(f"Error loading history: {str(e)}")
            return False
    
    def _try_save_history_to_env(self):
        """Try to save history to a file specified in the environment variable."""
        history_file = os.getenv('HISTORY_FILE', '')
        if history_file:
            try:
                self.save_history(history_file)
                logger.debug(f"Auto-saved history to {history_file}")
            except Exception as e:
                logger.error(f"Failed to auto-save history to {history_file}: {str(e)}")