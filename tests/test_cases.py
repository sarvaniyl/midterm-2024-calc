
# filepath: d:\Projects\midterm-2024-calc\tests\test.py
import pytest
from unittest.mock import patch, MagicMock
from app.repl import REPL
from app.calculator import Calculator
from app.commands.arithmetic import AddCommand, SubtractCommand, MultiplyCommand, DivideCommand
from app.commands.history import HistoryCommand, ClearHistoryCommand, DeleteCommand
from app.commands.system import ExitCommand, HelpCommand
from app.commands.base import Command



@pytest.fixture
def repl():
    return REPL()

def test_repl_initialization(repl):
    assert isinstance(repl.calculator, Calculator)
    assert repl.running == False
    assert len(repl._commands) > 0

def test_get_command_returns_valid_command(repl):
    command = repl.get_command('add')
    assert isinstance(command, AddCommand)
    
    command = repl.get_command('subtract')
    assert isinstance(command, SubtractCommand)

def test_get_command_returns_none_for_invalid_command(repl):
    command = repl.get_command('invalid_command')
    assert command is None

def test_get_command_list_returns_sorted_commands(repl):
    commands = repl.get_command_list()
    assert isinstance(commands, list)
    assert len(commands) > 0
    assert sorted(commands) == commands

def test_parse_input_with_command_and_args(repl):
    command_name, args = repl.parse_input('add 5 3')
    assert command_name == 'add'
    assert args == ['5', '3']

def test_parse_input_with_empty_input(repl):
    command_name, args = repl.parse_input('')
    assert command_name is None
    assert args == []

def test_parse_input_command_only(repl):
    command_name, args = repl.parse_input('help')
    assert command_name == 'help'
    assert args == []

def test_parse_input_case_insensitive(repl):
    command_name, args = repl.parse_input('ADD 5 3')
    assert command_name == 'add'
    assert args == ['5', '3']

def test_stop_repl(repl):
    repl.running = True
    repl.stop()
    assert repl.running == False
    
    


# Test command registration
def test_register_builtin_commands(repl):
    commands = repl._commands
    
    # Check if all expected command types are registered
    assert 'add' in commands
    assert 'subtract' in commands
    assert 'multiply' in commands
    assert 'divide' in commands
    assert 'history' in commands
    assert 'clear' in commands
    assert 'delete' in commands
    assert 'exit' in commands
    assert 'quit' in commands
    assert 'help' in commands
    assert 'export_csv' in commands
    assert 'import_csv' in commands
    assert 'greet' in commands
    assert 'help_plugin' in commands

# Test plugin loading
def test_load_plugin_commands(monkeypatch):
    # Mock the PluginLoader
    mock_plugin_loader = MagicMock()
    mock_plugin_loader.load_plugins.return_value = {'test_plugin': MagicMock()}
    
    # Replace the PluginLoader with our mock
    monkeypatch.setattr('app.repl.PluginLoader', lambda: mock_plugin_loader)
    
    # Create a new REPL instance with our mocked loader
    repl = REPL()
    
    # Check if the plugin command was added
    assert 'test_plugin' in repl._commands
    assert mock_plugin_loader.load_plugins.called

# Test run method
def test_run_with_valid_command(repl):
    # Mock input and command execution
    with patch('builtins.input', side_effect=['add 5 3', 'exit']), \
         patch('builtins.print') as mock_print, \
         patch.object(repl, 'get_command') as mock_get_command:
        
        # Mock command that returns a result
        mock_command = MagicMock()
        mock_command.execute.return_value = "8"
        mock_get_command.side_effect = [mock_command, ExitCommand(repl.calculator)]
        
        # Run the REPL
        repl.run()
        
        # Check if command was executed
        mock_command.execute.assert_called_once_with('5', '3')
        
        # Check if result was printed
        mock_print.assert_any_call("8")

def test_run_with_invalid_command(repl):
    # Mock input and print
    with patch('builtins.input', side_effect=['invalid_command', 'exit']), \
         patch('builtins.print') as mock_print, \
         patch.object(repl, 'get_command', side_effect=[None, ExitCommand(repl.calculator)]):
        
        # Run the REPL
        repl.run()
        
        # Check if error messages were printed
        mock_print.assert_any_call("Unknown command: invalid_command")
        mock_print.assert_any_call("Type 'help' for a list of commands")

def test_run_with_exception(repl):
    # Mock input and command execution
    with patch('builtins.input', side_effect=['add 5 3', 'exit']), \
         patch('builtins.print') as mock_print, \
         patch.object(repl, 'get_command') as mock_get_command, \
         patch('app.repl.logger.error') as mock_logger:
        
        # Create a mock command that raises an exception
        mock_command = MagicMock()
        mock_command.execute.side_effect = ValueError("Invalid arguments")
        mock_get_command.side_effect = [mock_command, ExitCommand(repl.calculator)]
        
        # Run the REPL
        repl.run()
        
        # Check if exception was logged and printed
        mock_logger.assert_called_once_with("Error in REPL: Invalid arguments")
        mock_print.assert_any_call("Error: Invalid arguments")

def test_run_with_keyboard_interrupt(repl):
    # Mock input that raises KeyboardInterrupt
    with patch('builtins.input', side_effect=KeyboardInterrupt), \
         patch('builtins.print') as mock_print:
        
        # Run the REPL
        repl.run()
        
        # Check if exit message was printed and running flag was set to False
        mock_print.assert_called_once_with("\nExiting...")
        assert repl.running == False

def test_get_command_case_insensitivity(repl):
    # Check that we can get commands regardless of case
    add_command = repl.get_command('ADD')
    subtract_command = repl.get_command('Subtract')
    multiply_command = repl.get_command('multiply')
    
    assert isinstance(add_command, AddCommand)
    assert isinstance(subtract_command, SubtractCommand)
    assert isinstance(multiply_command, MultiplyCommand)

def test_command_execution_passes_args_correctly(repl):
    # Get a command instance
    command = repl.get_command('add')
    
    # Mock the execute method
    original_execute = command.execute
    command.execute = MagicMock(return_value="8")
    
    # Parse input and execute command
    command_name, args = repl.parse_input('add 5 3')
    result = command.execute(*args)
    
    # Check if args were passed correctly
    command.execute.assert_called_once_with('5', '3')
    assert result == "8"
    
    # Restore original method
    command.execute = original_execute

def test_get_command_creates_new_instance(repl):
    # Get the same command twice
    command1 = repl.get_command('add')
    command2 = repl.get_command('add')
    
    # Verify they are different instances
    assert command1 is not command2
    assert isinstance(command1, AddCommand)
    assert isinstance(command2, AddCommand)    
    