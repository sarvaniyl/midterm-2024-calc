# Advanced Python Calculator

This is an advanced Python calculator application designed for a software engineering graduate course. The application demonstrates professional software development practices, including clean code, design patterns, logging, environment variables, data handling with Pandas, and a command-line interface.

## Key Components

### Design Patterns
The calculator implements several design patterns for maintainable and scalable code:

- **Singleton Pattern** ([Calculator class](app/calculator.py)): Ensures single calculator instance for consistent state management
- **Command Pattern** ([commands.py](app/commands/system.py)): Encapsulates operations as objects for uniform interface
- **Factory Method** ([plugin_loader.py](app/plugins/plugin_loader.py)): Creates command objects dynamically
- **Facade Pattern** ([history_manager.py](app/history_manager.py)): Simplifies Pandas operations behind clean interface

### Environment Variables
Configuration is managed through environment variables ([main.py](main.py)):

```python
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', './logs/calculator.log')
HISTORY_FILE = os.getenv('HISTORY_FILE', 'history.csv')
```

### Logging System
Comprehensive logging implementation ([logging.yaml](logging.yaml)):

- Multiple severity levels (INFO, WARNING, ERROR)
- File and console output
- Configurable through environment variables
- Rotated log files

### Error Handling Examples

LBYL (Look Before You Leap):
```python
# From app/calculator.py
def divide(self, a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
```

EAFP (Easier to Ask Forgiveness):
```python
# From app/history.py
try:
    df = pd.read_csv(self.history_file)
except FileNotFoundError:
    df = pd.DataFrame()
```

## Features

- Interactive REPL interface
- Basic arithmetic operations
- History management with Pandas
- Dynamic plugin system
- Environment variable configuration
- Comprehensive logging

## Installation & Usage

1. Clone and install:
```bash
git clone https://github.com/yourusername/calculator.git
pip install -r requirements.txt
```

2. Run:
```bash
python main.py
```

## Available Commands

- Basic operations: `add`, `subtract`, `multiply`, `divide`
- History: `history`, `export_csv`, `import_csv`, `clear`, `delete`
- System: `help`, `quit`
- Plugins: Additional commands loaded dynamically

## Testing

Run tests:
```bash
pytest tests/
```

## Plugin Development

Create plugins in the `plugins` directory implementing the `Command` interface.
