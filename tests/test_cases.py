"""Test module for the REPL calculator application."""
import pytest
from app.repl import REPL
from app.calculator import Calculator
from app.commands.arithmetic import AddCommand, SubtractCommand, MultiplyCommand, DivideCommand
from app.history_manager import HistoryManager
import pandas as pd

@pytest.fixture(name='repl')
def fixture_repl():
    """Fixture that provides a REPL instance for testing."""
    return REPL()


def test_repl_initialization(repl):
    """Test that REPL is properly initialized with calculator and commands."""
    assert isinstance(repl.calculator, Calculator)
    assert repl.running is False
    assert len(repl.get_command_list()) > 0


def test_get_command_returns_valid_command(repl):
    """Test that get_command returns correct command instances for valid inputs."""
    assert isinstance(repl.get_command('add'), AddCommand)
    assert isinstance(repl.get_command('subtract'), SubtractCommand)
    assert isinstance(repl.get_command('multiply'), MultiplyCommand)
    assert isinstance(repl.get_command('divide'), DivideCommand)


def test_get_command_returns_none_for_invalid_command(repl):
    """Test that get_command returns None for invalid command names."""
    assert repl.get_command('invalid_command') is None


def test_get_command_list_returns_sorted_commands(repl):
    """Test that get_command_list returns a sorted list of commands."""
    commands = repl.get_command_list()
    assert isinstance(commands, list)
    assert len(commands) > 0
    assert sorted(commands) == commands


def test_parse_input_with_command_and_args(repl):
    """Test parsing input with both command and arguments."""
    command_name, args = repl.parse_input('add 5 3')
    assert command_name == 'add'
    assert args == ['5', '3']


def test_parse_input_with_empty_input(repl):
    """Test parsing empty input string."""
    command_name, args = repl.parse_input('')
    assert command_name is None
    assert args == []


def test_parse_input_command_only(repl):
    """Test parsing input with command but no arguments."""
    command_name, args = repl.parse_input('help')
    assert command_name == 'help'
    assert args == []


def test_parse_input_case_insensitive(repl):
    """Test that input parsing is case insensitive."""
    command_name, args = repl.parse_input('ADD 5 3')
    assert command_name == 'add'
    assert args == ['5', '3']


def test_stop_repl(repl):
    """Test that stop method correctly sets running to False."""
    repl.running = True
    repl.stop()
    assert repl.running is False


def test_register_builtin_commands(repl):
    """Test that all expected built-in commands are registered."""
    commands = repl._commands  # Use public property if available, or rename _commands to commands
    expected_commands = {
        'add', 'subtract', 'multiply', 'divide', 'history', 'clear', 'delete',
        'exit', 'quit', 'help', 'export_csv', 'import_csv'
    }
    assert all(cmd.lower() in commands for cmd in expected_commands)
    assert len(commands) >= len(expected_commands)


def test_get_command_case_insensitivity(repl):
    """Test that get_command works with different case variations."""
    assert isinstance(repl.get_command('ADD'), AddCommand)
    assert isinstance(repl.get_command('Subtract'), SubtractCommand)
    assert isinstance(repl.get_command('multiply'), MultiplyCommand)


def test_get_command_creates_new_instance(repl):
    """Test that get_command creates new command instances."""
    assert isinstance(repl.get_command('add'), AddCommand)
    assert isinstance(repl.get_command('add'), AddCommand)


def test_parse_input_extra_spaces(repl):
    """Test parsing input with extra whitespace."""
    command_name, args = repl.parse_input('  add    10   20  ')
    assert command_name == 'add'
    assert args == ['10', '20']


def test_parse_input_none(repl):
    """Test that parsing None input raises AttributeError."""
    with pytest.raises(AttributeError):
        repl.parse_input(None)
@pytest.fixture(name='history_manager')
def fixture_history_manager():
    """Fixture that provides a fresh instance of HistoryManager for testing."""
    HistoryManager._instance = None  # Reset singleton instance before each test
    return HistoryManager()


def test_history_manager_initialization(history_manager):
    """Test that HistoryManager initializes with an empty history DataFrame."""
    assert isinstance(history_manager._history, pd.DataFrame)
    assert history_manager._history.empty
    assert list(history_manager._history.columns) == ['operation', 'expression', 'result']


def test_add_entry(history_manager):
    """Test adding an entry to history."""
    history_manager.add_entry('add', '2 + 3', 5)
    assert len(history_manager._history) == 1
    assert history_manager._history.iloc[0].to_dict() == {
        'operation': 'add', 'expression': '2 + 3', 'result': '5'
    }


def test_get_history(history_manager):
    """Test retrieving the history DataFrame."""
    history_manager.add_entry('subtract', '10 - 5', 5)
    history_df = history_manager.get_history()
    assert isinstance(history_df, pd.DataFrame)
    assert len(history_df) == 1
    assert history_df.iloc[0]['operation'] == 'subtract'


def test_delete_entry(history_manager):
    """Test deleting an entry from history."""
    history_manager.add_entry('multiply', '2 * 3', 6)
    assert len(history_manager._history) == 1
    assert history_manager.delete_entry(0) is True
    assert len(history_manager._history) == 0
    assert history_manager.delete_entry(0) is False  # Deleting non-existent entry


def test_clear_history(history_manager):
    """Test clearing the history."""
    history_manager.add_entry('divide', '10 / 2', 5)
    history_manager.clear_history()
    assert history_manager._history.empty


def test_save_and_load_history(history_manager, tmp_path):
    """Test saving and loading history from a CSV file."""
    file_path = tmp_path / 'history.csv'
    history_manager.add_entry('power', '2 ** 3', 8)
    assert history_manager.save_history(str(file_path)) is True
    
    new_history_manager = HistoryManager()
    assert new_history_manager.load_history(str(file_path)) is True
    assert len(new_history_manager._history) == 1
    assert new_history_manager._history.iloc[0]['operation'] == 'power'


def test_invalid_load_history(history_manager, tmp_path):
    """Test loading a non-existent or invalid history file."""
    file_path = tmp_path / 'non_existent.csv'
    assert history_manager.load_history(str(file_path)) is False
