# app/commands/arithmetic.py
import logging
from typing import List

from app.commands.base import Command

logger = logging.getLogger(__name__)


class AddCommand(Command):
    """Command to add two numbers."""

    name = "add"
    help = "Add two numbers (add <num1> <num2>)"

    def execute(self, *args) -> str:
        if len(args) != 2:
            return "Error: 'add' requires exactly two arguments"

        try:
            result = self.calculator.calculate("add", *args)
            return f"Result: {result}"
        except ValueError as e:
            return f"Error: {str(e)}"


class SubtractCommand(Command):
    """Command to subtract two numbers."""

    name = "subtract"
    help = "Subtract two numbers (subtract <num1> <num2>)"

    def execute(self, *args) -> str:
        if len(args) != 2:
            return "Error: 'subtract' requires exactly two arguments"

        try:
            result = self.calculator.calculate("subtract", *args)
            return f"Result: {result}"
        except ValueError as e:
            return f"Error: {str(e)}"


class MultiplyCommand(Command):
    """Command to multiply two numbers."""

    name = "multiply"
    help = "Multiply two numbers (multiply <num1> <num2>)"

    def execute(self, *args) -> str:
        if len(args) != 2:
            return "Error: 'multiply' requires exactly two arguments"

        try:
            result = self.calculator.calculate("multiply", *args)
            return f"Result: {result}"
        except ValueError as e:
            return f"Error: {str(e)}"


class DivideCommand(Command):
    """Command to divide two numbers."""

    name = "divide"
    help = "Divide two numbers (divide <num1> <num2>)"

    def execute(self, *args) -> str:
        if len(args) != 2:
            return "Error: 'divide' requires exactly two arguments"

        try:
            result = self.calculator.calculate("divide", *args)
            return f"Result: {result}"
        except ValueError as e:
            return f"Error: {str(e)}"
