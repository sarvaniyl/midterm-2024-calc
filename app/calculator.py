# app/calculator.py
import logging
import operator
from typing import Any, Dict, Callable

from app.history_manager import HistoryManager

logger = logging.getLogger(__name__)

class Calculator:
    """
    Calculator class that performs basic arithmetic operations.
    This class implements the Facade pattern to provide a simplified interface
    for performing calculations and managing history.
    """
    
    def __init__(self):
        self.history_manager = HistoryManager()
        self.operations = self._register_operations()
        logger.info("Calculator initialized")
        
    def _register_operations(self) -> Dict[str, Callable]:
        """Register basic operations."""
        return {
            'add': operator.add,
            'subtract': operator.sub,
            'multiply': operator.mul,
            'divide': operator.truediv,
        }
    
    def calculate(self, operation: str, *args) -> Any:
        """
        Perform a calculation and add it to the history.
        
        Args:
            operation: The operation to perform
            *args: The arguments for the operation
            
        Returns:
            The result of the calculation
            
        Raises:
            ValueError: If the operation is invalid or the arguments are invalid
        """
        if operation not in self.operations:
            logger.error(f"Invalid operation: {operation}")
            raise ValueError(f"Invalid operation: {operation}")
        
        # Convert arguments to numbers
        try:
            numeric_args = [float(arg) for arg in args]
        except ValueError:
            logger.error(f"Invalid arguments for {operation}: {args}")
            raise ValueError(f"Invalid arguments for {operation}: {args}")
        
        # Check for division by zero
        if operation == 'divide' and numeric_args[1] == 0:
            logger.error("Division by zero")
            raise ValueError("Division by zero")
        
        # Perform the calculation
        try:
            # For binary operations like add, subtract, etc.
            if len(numeric_args) == 2:
                result = self.operations[operation](numeric_args[0], numeric_args[1])
            else:
                logger.error(f"Invalid number of arguments for {operation}: {len(numeric_args)}")
                raise ValueError(f"Invalid number of arguments for {operation}: expected 2, got {len(numeric_args)}")
                
            # Format the expression
            expression = self._format_expression(operation, numeric_args)
            
            # Add to history
            self.history_manager.add_entry(operation, expression, result)
            
            logger.info(f"Calculated: {expression} = {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in calculation: {str(e)}")
            raise ValueError(f"Error in calculation: {str(e)}")
    
    def _format_expression(self, operation: str, args) -> str:
        """
        Format the expression for display in the history.
        
        Args:
            operation: The operation performed
            args: The arguments for the operation
            
        Returns:
            A string representation of the expression
        """
        operation_symbols = {
            'add': '+',
            'subtract': '-',
            'multiply': '*',
            'divide': '/'
        }
        
        symbol = operation_symbols.get(operation, operation)
        
        # For binary operations
        if len(args) == 2:
            return f"{args[0]} {symbol} {args[1]}"
        
        return f"{operation}({', '.join(map(str, args))})"
    
    def get_history(self):
        """Get the calculation history."""
        return self.history_manager.get_history()
    
    def clear_history(self):
        """Clear the calculation history."""
        self.history_manager.clear_history()
        logger.info("Cleared calculator history")