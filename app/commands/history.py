# app/commands/history.py
import logging
from typing import List

from app.commands.base import Command

logger = logging.getLogger(__name__)


class HistoryCommand(Command):
    """Command to display calculation history."""

    name = "history"
    help = "Display calculation history"

    def execute(self, *args) -> str:
        history = self.calculator.get_history()

        if history.empty:
            return "No calculation history"

        # Format the history as a readable string
        lines = []
        for idx, (_, row) in enumerate(history.iterrows()):
            lines.append(f"{idx}: {row['expression']} = {row['result']}")

        return "Calculation History:\n" + "\n".join(lines)


class ClearHistoryCommand(Command):
    """Command to clear calculation history."""

    name = "clear"
    help = "Clear calculation history"

    def execute(self, *args) -> str:
        self.calculator.clear_history()
        return "Calculation history cleared"


class DeleteCommand(Command):
    """Command to delete a specific history entry."""

    name = "delete"
    help = "Delete a specific history entry (delete <index>)"

    def execute(self, *args) -> str:
        if not args:
            return "Error: Please specify an index to delete"

        try:
            index = int(args[0])
            if self.calculator.history_manager.delete_entry(index):
                return f"Deleted history entry at index {index}"
            else:
                return f"Error: No history entry at index {index}"
        except ValueError:
            return f"Error: Invalid index '{args[0]}'"
