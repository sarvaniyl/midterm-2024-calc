"""
Arithmetic command implementations for the calculator.
"""
import logging
from app.commands.base import Command
from app.calculator import Calculator

__all__ = ['AddCommand', 'SubtractCommand', 'MultiplyCommand', 'DivideCommand']

logger = logging.getLogger("calculator.commands.arithmetic")

class AddCommand(Command):
    """Command to add two numbers."""
    def execute(self, *args) -> float:
        """
        Execute the add command.
        
        Args:
            args: Should contain exactly two number arguments
            
        Returns:
            The sum of the two numbers
            
        Raises:
            ValueError: If the wrong number or type of arguments is provided
        """
        if len(args) != 2:
            raise ValueError("Add command requires exactly 2 arguments")
        try:
            a, b = float(args[0]), float(args[1])
            return Calculator().add(a, b)
        except ValueError as e:
            logger.error(f"Invalid arguments for add command: {args}")
            raise ValueError(f"Invalid arguments for add command: {e}")
    
    def get_help(self) -> str:
        """Get the help text for the add command."""
        return "add <a> <b> - Add two numbers"

class SubtractCommand(Command):
    """Command to subtract one number from another."""
    def execute(self, *args) -> float:
        """
        Execute the subtract command.
        
        Args:
            args: Should contain exactly two number arguments
            
        Returns:
            The result of the subtraction
            
        Raises:
            ValueError: If the wrong number or type of arguments is provided
        """
        if len(args) != 2:
            raise ValueError("Subtract command requires exactly 2 arguments")
        try:
            a, b = float(args[0]), float(args[1])
            return Calculator().subtract(a, b)
        except ValueError as e:
            logger.error(f"Invalid arguments for subtract command: {args}")
            raise ValueError(f"Invalid arguments for subtract command: {e}")
    
    def get_help(self) -> str:
        """Get the help text for the subtract command."""
        return "subtract <a> <b> - Subtract b from a"

class MultiplyCommand(Command):
    """Command to multiply two numbers."""
    def execute(self, *args) -> float:
        """
        Execute the multiply command.
        
        Args:
            args: Should contain exactly two number arguments
            
        Returns:
            The product of the two numbers
            
        Raises:
            ValueError: If the wrong number or type of arguments is provided
        """
        if len(args) != 2:
            raise ValueError("Multiply command requires exactly 2 arguments")
        try:
            a, b = float(args[0]), float(args[1])
            return Calculator().multiply(a, b)
        except ValueError as e:
            logger.error(f"Invalid arguments for multiply command: {args}")
            raise ValueError(f"Invalid arguments for multiply command: {e}")
    
    def get_help(self) -> str:
        """Get the help text for the multiply command."""
        return "multiply <a> <b> - Multiply two numbers"

class DivideCommand(Command):
    """Command to divide one number by another."""
    def execute(self, *args) -> float:
        """
        Execute the divide command.
        
        Args:
            args: Should contain exactly two number arguments
            
        Returns:
            The result of the division
            
        Raises:
            ValueError: If the wrong number or type of arguments is provided or if division by zero
        """
        if len(args) != 2:
            raise ValueError("Divide command requires exactly 2 arguments")
        try:
            a, b = float(args[0]), float(args[1])
            return Calculator().divide(a, b)
        except (ValueError, ZeroDivisionError) as e:
            logger.error(f"Invalid arguments for divide command: {args}")
            raise ValueError(f"Invalid arguments for divide command: {e}")
    
    def get_help(self) -> str:
        """Get the help text for the divide command."""
        return "divide <a> <b> - Divide a by b"