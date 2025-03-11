# Advanced Python Calculator

## **Overview**
This is an advanced Python-based calculator application developed for a software engineering graduate course. It follows professional software development practices, including clean and maintainable code, the application of design patterns, structured logging, dynamic configuration via environment variables, sophisticated data handling with Pandas, and a command-line interface (REPL) for real-time user interaction.

The calculator supports arithmetic operations, calculation history management, a dynamic plugin system, and integrates multiple software design patterns for scalability and flexibility.

## **Key Features**
- **Interactive Command-Line Interface (REPL)** for executing calculations in real time.
- **Arithmetic Operations**: Addition, subtraction, multiplication, and division.
- **Plugin System**: Extensible system to dynamically load new commands.
- **Calculation History Management** with Pandas, supporting CSV import/export.
- **Comprehensive Logging** with different severity levels and dynamic configuration.
- **Error Handling** using LBYL (Look Before You Leap) and EAFP (Easier to Ask for Forgiveness than Permission).
- **Automated Testing** with Pytest to achieve high test coverage.
- **CI/CD Integration**: GitHub Actions for automated testing and validation.
- **Environment Variable Configuration** to modify logging, file paths, and settings dynamically.

## **Project Structure**
```
calculator/
|-- app/
|   |-- commands/      # Command Pattern Implementation
|   |-- plugins/       # Plugin System for extending functionality
|   |-- history_manager.py   # Singleton Pattern for managing history
|   |-- calculator.py  # Core arithmetic operations (Facade Pattern)
|-- tests/             # Unit tests (pytest)
|-- logs/              # Application logs
|-- .github/workflows/ # GitHub Actions for CI/CD
|-- main.py            # Entry point (REPL interface)
|-- requirements.txt   # Dependencies
|-- README.md          # Documentation
|-- logging.yaml       # Logging configuration
```

## **Design Patterns Implemented**
This project incorporates multiple design patterns to ensure modularity, scalability, and maintainability.

### **1. Command Pattern**
- Encapsulates operations as objects for a uniform interface.
- Implemented in [`base.py`](app/commands/base.py) .

### **2. Facade Pattern**
- Simplifies Pandas operations by providing a clean interface.
- Implemented in [`calculator.py`](app/calculator.py) for abstracting complex data operations.

### **3. Singleton Pattern**
- Ensures only one instance of the history manager is used.
- Implemented in [`history_manager.py`](app/history_manager.py).

### **4. Strategy Pattern**
- Allows different calculation strategies (e.g., different precision levels for floating-point arithmetic).
- Implemented in [`calculator.py`](app/calculator.py).

## **Configuration via Environment Variables**
The application allows dynamic configuration through environment variables, improving flexibility.

- **Defined in [`main.py`](main.py):**
```python
import os
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', './logs/calculator.log')
HISTORY_FILE = os.getenv('HISTORY_FILE', 'history.csv')
```
- **Usage Example:**
```bash
export LOG_LEVEL=DEBUG
export LOG_FILE=./logs/debug.log
python main.py
```

## **Logging System**
Logging follows best practices with different severity levels and configurable output.

- **Defined in [`logging.yaml`](logging.yaml).**
- Logs include:
  - **INFO** for general operations.
  - **WARNING** for unexpected scenarios.
  - **ERROR** for critical failures.
- **Example Log Output:**
```
2025-03-10 12:34:56,789 - INFO - Executing command: add 3 4
2025-03-10 12:34:56,791 - ERROR - Division by zero attempted.
```

## **Error Handling: LBYL vs. EAFP**
This project uses both LBYL (Look Before You Leap) and EAFP (Easier to Ask for Forgiveness than Permission) paradigms.

### **LBYL Example (Checking before execution)**
```python
# From (app/calculator.py)
def divide(self, a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
```
### **EAFP Example (Handling exceptions after execution)**
```python
# From app/plugin/csv/csv_plugin.py
try:
    data = pd.read_csv(filename)
    history_manager.set_history(data)
    logger.info("History imported from %s", filename)
    return f"History imported from {filename}"
except OSError as err:
    logger.error("Failed to import CSV: %s", str(err))
    return f"Error importing CSV: {str(err)}"
```

## **Installation & Usage**
### **1. Clone the Repository**
```bash
git clone https://github.com/sarvaniyl/calculator.git
cd calculator
```
### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```
### **3. Run the Application**
```bash
python main.py
```

## **Available Commands**
| Command      | Description                         | Example Usage         |
|-------------|------------------------------------|----------------------|
| `add`       | Adds two numbers                  | `add 5 3` → 8       |
| `subtract`  | Subtracts one number from another | `subtract 10 2` → 8 |
| `multiply`  | Multiplies two numbers            | `multiply 4 5` → 20 |
| `divide`    | Divides one number by another     | `divide 9 3` → 3    |
| `history`   | Shows past calculations          | `history`          |
| `export_csv`| Saves history to CSV file        | `export_csv history.csv` |
| `import_csv`| Loads history from CSV file      | `import_csv history.csv` |
| `clear`     | Clears history                   | `clear`            |
| `delete`    | Deletes specific record          | `delete 2`         |
| `quit`      | Exits the calculator             | `quit`             |

## **Testing & CI/CD**
### **Run Tests**
```bash
pytest tests/
```
- Minimum **90% test coverage** required.
- GitHub Actions ensure all commits pass tests before merging.

## **Plugin Development**
Extend functionality by adding new plugins.
1. Create a new file under `plugins/`.
2. Implement the `Command` interface.
3. Register the command in the system.

Example Plugin:
```python
from app.commands.base import Command

class CubeCommand(Command):
    name = "cube"
    help = "Returns the cube of a number"

    def execute(self, args):
        number = float(args[0])
        return f"Cube of {number} is {number ** 3}"
```



