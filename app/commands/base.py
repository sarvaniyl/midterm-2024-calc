# app/commands/base.py
import logging
from abc import ABC, abstractmethod
from typing import Any, List

logger = logging.getLogger(__name__)


class Command(ABC):
    """
    Abstract base class for all commands.
    This follows the Command pattern.
    """

    name = ""
    help = ""

    def __init__(self, calculator=None):
        self.calculator = calculator

    @abstractmethod
    def execute(self, *args) -> str:
        """
        Execute the command with the given arguments.

        Args:
            *args: Arguments for the command

        Returns:
            A string with the result of the command
        """
        pass
