import pytest
from app.repl import REPL
from app.calculator import Calculator
from app.commands.arithmetic import AddCommand, SubtractCommand
from app.commands.base import Command

# filepath: d:\Projects\midterm-2024-calc\tests\test.py

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