"""
History management commands for the calculator.
"""
import logging
import pandas as pd
from app.commands.base import Command
from app.calculator import Calculator

logger = logging.getLogger("calculator.commands.history")

class HistoryCommand(Command):
    """Command to display calculation history."""
    def execute(self, *_args) -> pd.DataFrame:
        """
        Execute the history command.
        
        Returns:
            DataFrame containing the calculation history
        """
        logger.info("Displaying calculation history")
        return Calculator().history_manager.get_history()
    
    def get_help(self) -> str:
        """Get the help text for the history command."""
        return "history - Display calculation history"

class SaveCommand(Command):
    """Command to save calculation history to file."""
    def execute(self, *_args) -> str:
        """
        Execute the save command.
        
        Returns:
            Success message
        """
        logger.info("Saving calculation history")
        Calculator().history_manager.save_history()
        return "History saved successfully"
    
    def get_help(self) -> str:
        """Get the help text for the save command."""
        return "save - Save calculation history to file"

class ClearCommand(Command):
    """Command to clear calculation history."""
    def execute(self, *_args) -> str:
        """
        Execute the clear command.
        
        Returns:
            Success message
        """
        logger.info("Clearing calculation history")
        Calculator().history_manager.clear_history()
        return "History cleared successfully"
    
    def get_help(self) -> str:
        """Get the help text for the clear command."""
        return "clear - Clear calculation history"

class DeleteCommand(Command):
    """Command to delete a specific entry from calculation history."""
    def execute(self, *args) -> str:
        """
        Execute the delete command.
        
        Args:
            args: Should contain the index of the entry to delete
            
        Returns:
            Success message
            
        Raises:
            ValueError: If the index is invalid
        """
        if len(args) != 1:
            raise ValueError("Delete command requires exactly 1 argument")
        try:
            index = int(args[0])
            Calculator().history_manager.delete_entry(index)
            return f"Entry at index {index} deleted successfully"
        except (ValueError, IndexError) as e:
            logger.error(f"Error in delete command: {str(e)}")
            raise ValueError(f"Error in delete command: {e}")
    
    def get_help(self) -> str:
        """Get the help text for the delete command."""
        return "delete <index> - Delete history entry at specified index"