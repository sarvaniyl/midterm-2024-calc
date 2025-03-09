# Advanced Python Calculator

This is an advanced Python calculator application designed for a software engineering graduate course. The application demonstrates professional software development practices, including clean code, design patterns, logging, environment variables, data handling with Pandas, and a command-line interface.

## Features

- Command-Line Interface (REPL) for direct interaction
- Basic arithmetic operations (add, subtract, multiply, divide)
- Calculation history management with Pandas
- Plugin system for extending functionality
- Professional logging practices
- Dynamic configuration via environment variables
- Implementation of multiple design patterns

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/midterm-2024-calc.git
cd midterm-2024-calc
```

2. Install required packages:
```
pip install -r requirements.txt
```

## Usage

Run the calculator:
```
python main.py
```

### Basic Commands

- `add <a> <b>` - Add two numbers
- `subtract <a> <b>` - Subtract b from a
- `multiply <a> <b>` - Multiply two numbers
- `divide <a> <b>` - Divide a by b
- `history` - Display calculation history
- `save` - Save calculation history to file
- `clear` - Clear calculation history
- `delete <index>` - Delete history entry at specified index
- `help` or `menu` - Display available commands
- `quit` or `exit` - Exit the calculator

### Plugin Commands

Additional commands available through the statistics plugin:
- `mean <n1> <n2> ...` - Calculate the mean of a list of numbers
- `median <n1> <n2> ...` - Calculate the median of a list of numbers
- `stddev <n1> <n2> ...` - Calculate the standard deviation of a list of numbers

## Environment Variables

The calculator uses environment variables for dynamic configuration:

- `LOG_LEVEL`: Sets the logging level (default: INFO)
- `LOG_FILE`: Specifies the log file path (default: calculator.log)
- `HISTORY_FILE`: Specifies the calculation history file path (default: calculator_history.csv)
- `PLUGIN_DIR`: Specifies the directory to load plugins from (default: plugins)

Example:
```
# Windows
set LOG_LEVEL=DEBUG
set HISTORY_FILE=my_history.csv
python main.py

# Linux/Mac
LOG_LEVEL=DEBUG HISTORY_FILE=my_history.csv python main.py
```

## Design Patterns Implementation

### Singleton Pattern

The `Calculator` class implements the Singleton pattern to ensure only one calculator instance exists in the application. This is important for maintaining a single source of truth for calculations and history.

```python
# See Calculator class in main.py
def __new__(cls):
    if cls._instance is None:
        cls._instance = super(Calculator, cls).__new__(cls)
        cls._instance._initialize()
    return cls._instance
```

### Command Pattern

The Command pattern is used to encapsulate operations as objects, allowing for a consistent interface for different calculator commands and making it easy to add new commands.

```python
# See Command class and its implementations in main.py
class Command:
    def execute(self, *args, **kwargs) -> Any:
        pass
    
    def get_help(self) -> str:
        pass
```

### Factory Method Pattern

The CommandFactory class implements the Factory Method pattern to create command objects based on user input.

```python
# See CommandFactory class in main.py
@staticmethod
def create_command(command_name: str, command_registry: Dict[str, Command]) -> Command:
    if command_name in command_registry:
        return command_registry[command_name]
    else:
        raise ValueError(f"Unknown command: {command_name}")
```

### Facade Pattern

The `HistoryManager` class implements the Facade pattern to provide a simplified interface for complex Pandas operations.

```python
# See HistoryManager class in main.py
def _load_history(self) -> pd.DataFrame:
    try:
        return pd.read_csv(self.history_file)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=['operation', 'operands', 'result', 'timestamp'])
```

## Logging Strategy

The application implements a comprehensive logging system that records operations, data manipulations, errors, and informational messages. The logging configuration is dynamic and can be controlled through environment variables.

```python
# See logging configuration in main.py
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG_FILE = os.environ.get('LOG_FILE', 'calculator.log')

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
```

The logging system differentiates messages by severity (INFO, WARNING, ERROR) and provides detailed context for effective monitoring and debugging.

## Exception Handling Approaches

The application demonstrates both "Look Before You Leap" (LBYL) and "Easier to Ask for Forgiveness than Permission" (EAFP) approaches to error handling:

### LBYL Example:
```python
# In the divide method of Calculator class
if b == 0:
    logger.error("Division by zero attempted")
    raise ValueError("Cannot divide by zero")
```

### EAFP Example:
```python
# In the _load_history method of HistoryManager class
try:
    return pd.read_csv(self.history_file)
except (FileNotFoundError, pd.errors.EmptyDataError):
    logger.info(f"Creating new history file: {self.history_file}")
    return pd.DataFrame(columns=['operation', 'operands', 'result', 'timestamp'])
```

## Testing

Run tests with pytest:
```
pytest tests/ -v
```

Tests cover all major components of the application with a target of 90% coverage.

## Plugin Development

You can extend the calculator functionality by creating plugins. Plugins should be Python files placed in the `plugins` directory and should implement a `register_commands()` function that returns a dictionary of command names and command objects.

Example plugin structure:
```python
# plugins/my_plugin.py
class MyCommand:
    def execute(self, *args):
        # Command implementation
        return result
    
    def get_help(self):
        return "mycommand <args> - Description of the command"

def register_commands():
    return {
        'mycommand': MyCommand()
    }
```