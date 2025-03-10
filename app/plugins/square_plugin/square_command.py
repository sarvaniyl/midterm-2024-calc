from app.commands.base import Command
class SquareCommand(Command):
    name = "square"
    help = "square of number (square <number>)"
    
    def execute(self, args):
        """Calculate the square of a number
        
        Args:
            args: Should contain a single number
            
        Returns:
            float: The square of the input number
        """
        # Debug line to see what's coming in
        print(f"Debug - received args: {args}, type: {type(args)}")
        
        if not args:
            return "Usage: square <number>"
        
        try:
            # Try to parse the first argument as a float
            number = float(args[0])
            result = number ** 2
            return f"The square of {number} is {result}"
        except (ValueError, IndexError) as e:
            print(f"Error: {str(e)}")
            return "Please provide a valid number"