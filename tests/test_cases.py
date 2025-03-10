import pytest
from app.repl import REPL
from app.calculator import Calculator
from app.commands.arithmetic import AddCommand, SubtractCommand, MultiplyCommand, DivideCommand


@pytest.fixture
def repl():
    return REPL()


### --- EXISTING TEST CASES --- ###
def test_repl_initialization(repl):
    assert isinstance(repl.calculator, Calculator)
    assert repl.running is False
    assert len(repl.get_command_list()) > 0


def test_get_command_returns_valid_command(repl):
    assert isinstance(repl.get_command('add'), AddCommand)
    assert isinstance(repl.get_command('subtract'), SubtractCommand)
    assert isinstance(repl.get_command('multiply'), MultiplyCommand)
    assert isinstance(repl.get_command('divide'), DivideCommand)

def test_get_command_returns_none_for_invalid_command(repl):
    assert repl.get_command('invalid_command') is None


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
    assert repl.running is False


def test_register_builtin_commands(repl):
    commands = repl._commands
    expected_commands = {
        'add', 'subtract', 'multiply', 'divide', 'history', 'clear', 'delete',
        'exit', 'quit', 'help', 'export_csv', 'import_csv', 'greet', 'help_plugin'
    }
    assert all(cmd.lower() in commands for cmd in expected_commands)
    assert len(commands) >= len(expected_commands)

def test_get_command_case_insensitivity(repl):
    assert isinstance(repl.get_command('ADD'), AddCommand)
    assert isinstance(repl.get_command('Subtract'), SubtractCommand)
    assert isinstance(repl.get_command('multiply'), MultiplyCommand)


def test_get_command_creates_new_instance(repl):
    assert isinstance(repl.get_command('add'), AddCommand)
    assert isinstance(repl.get_command('add'), AddCommand)


### --- NEW TEST CASES TO INCREASE COVERAGE --- ###

def test_parse_input_extra_spaces(repl):
    command_name, args = repl.parse_input('  add    10   20  ')
    assert command_name == 'add'
    assert args == ['10', '20']


def test_parse_input_non_string_input(repl):
    with pytest.raises(AttributeError):
        repl.parse_input(None)  # Should raise an error because NoneType has no `.split()`



def test_parse_input_non_string_input(repl):
    with pytest.raises(AttributeError):
        repl.parse_input(None)  # Should raise an error because NoneType has no `.split()`
