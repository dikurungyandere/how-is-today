#!/usr/bin/env python3
"""Tests for today.py"""

import pytest
import json
from today import get_daily_message, get_message_count, MESSAGES, strip_emoji

def test_get_daily_message_returns_string():
    """get_daily_message should return a string from MESSAGES."""
    result = get_daily_message()
    assert isinstance(result, str)
    assert result in MESSAGES

def test_get_daily_message_with_seed():
    """Same seed should return same message."""
    result1 = get_daily_message(seed=42)
    result2 = get_daily_message(seed=42)
    assert result1 == result2

def test_different_seeds_different_messages():
    """Different seeds may return different messages."""
    results = set(get_daily_message(seed=i) for i in range(100))
    assert len(results) > 1

def test_messages_are_non_empty():
    """All messages should be non-empty strings."""
    for msg in MESSAGES:
        assert len(msg) > 0

def test_get_message_count():
    """get_message_count should return correct count."""
    assert get_message_count() == len(MESSAGES)

def test_get_message_by_index():
    """get_message_by_index should return correct message or None."""
    from today import get_message_by_index
    assert get_message_by_index(0) == MESSAGES[0]
    assert get_message_by_index(len(MESSAGES)-1) == MESSAGES[-1]
    assert get_message_by_index(-1) is None
    assert get_message_by_index(999) is None

def test_get_random_message():
    """get_random_message should return a message from MESSAGES."""
    from today import get_random_message
    result = get_random_message()
    assert result in MESSAGES

def test_cli_index_option():
    """CLI should support -i/--index to get message by index."""
    import subprocess
    result = subprocess.run(["python", "today.py", "-i", "0"], capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stdout.strip() == MESSAGES[0]

def test_cli_import():
    """CLI module should be importable without errors."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("today", "today.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "main")

def test_random_state_preserved():
    """get_daily_message should return consistent results."""
    from today import get_daily_message
    # Same inputs should give same outputs
    result1 = get_daily_message(seed=42)
    result2 = get_daily_message(seed=42)
    assert result1 == result2, "Same seed should return same message"

def test_load_messages_from_file(tmp_path):
    """load_messages_from_file should load custom messages, ignoring empty lines and comments."""
    from today import load_messages_from_file
    # Create a temp file with custom messages, empty lines, and comments
    msg_file = tmp_path / "messages.txt"
    msg_file.write_text("# This is a comment\nCustom1\n\nCustom2\n# Another comment\nCustom3\n")
    messages = load_messages_from_file(str(msg_file))
    assert messages == ["Custom1", "Custom2", "Custom3"]

def test_load_messages_from_nonexistent_file():
    """load_messages_from_file should return None for missing file."""
    from today import load_messages_from_file
    result = load_messages_from_file("/nonexistent/file.txt")
    assert result is None

def test_load_config_returns_dict():
    """load_config should return a dict."""
    from today import load_config
    config = load_config()
    assert isinstance(config, dict)

def test_load_config_loads_file(tmp_path, monkeypatch):
    """load_config should load config from file."""
    from today import load_config
    # Set up a temporary directory as HOME
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    # Create a config file in the first expected location: ~/.config/how-is-today.json
    config_dir = home / ".config"
    config_dir.mkdir()
    config_file = config_dir / "how-is-today.json"
    config_content = {"key": "value", "number": 42}
    config_file.write_text(json.dumps(config_content))
    # Now call load_config and check the result
    result = load_config()
    assert result == config_content

def test_get_shuffled_messages():
    """get_shuffled_messages should return shuffled list."""
    from today import get_shuffled_messages, MESSAGES
    result = get_shuffled_messages(seed=123)
    assert isinstance(result, list)
    assert len(result) == len(MESSAGES)
    assert set(result) == set(MESSAGES)

def test_get_shuffled_messages_with_count():
    """get_shuffled_messages with count should limit results."""
    from today import get_shuffled_messages
    result = get_shuffled_messages(seed=42, count=5)
    assert len(result) == 5

def test_strip_emoji():
    """strip_emoji should remove emojis from text."""
    from today import strip_emoji
    assert strip_emoji("Today is a great day! 🌟") == "Today is a great day!"
    assert strip_emoji("") == ""
    assert strip_emoji("🌟") == ""
    assert strip_emoji("Hello 🌍 World 0") == "Hello  World 0"  # Zero is not emoji
    assert strip_emoji("  Leading space 🌟 and trailing  ") == "Leading space  and trailing"


def test_cli_version_option():
    """CLI should return version string with --version."""
    import subprocess
    result = subprocess.run(["python", "today.py", "--version"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "how-is-today 1.0.0" in result.stdout

def test_cli_list_with_count():
    """CLI --list with --count should output specified number of messages."""
    import subprocess
    result = subprocess.run(["python", "today.py", "--list", "--count", "3"], capture_output=True, text=True)
    assert result.returncode == 0
    lines = [line.strip() for line in result.stdout.split("\n") if line.strip()]
    assert len(lines) == 3
    for i, line in enumerate(lines, 1):
        assert line.startswith(f"{i}. ")
def test_cli_strip_emoji_option():
    """CLI should support -e/--strip-emoji to remove emojis from output."""
    import subprocess
    result = subprocess.run(["python", "today.py", "-m", "-e"], capture_output=True, text=True)
    assert result.returncode == 0
    output = result.stdout.strip()
    # Should contain a message without emojis
    assert "🌟" not in output
    assert "💪" not in output
    assert "✨" not in output
    # Should still contain text
    assert len(output) > 0

def test_cli_output_flag():
    """CLI should support -o/--output to write message to file."""
    import subprocess
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='\.txt') as f:
        temp_path = f.name
    try:
        # Test without --quiet: should write to file and print confirmation to stderr
        result = subprocess.run(["python", "today.py", "-m", "-o", temp_path], capture_output=True, text=True)
        assert result.returncode == 0
        assert f"Saved to {temp_path}" in result.stderr
        # Check file content
        with open(temp_path, 'r') as f:
            content = f.read().strip()
        assert content in MESSAGES  # Should be one of the messages
        # Test with --quiet: should write to file and no stdout/stderr
        result2 = subprocess.run(["python", "today.py", "-m", "-o", temp_path, "-q"], capture_output=True, text=True)
        assert result2.returncode == 0
        assert result2.stdout == ""
        assert result2.stderr == ""
        with open(temp_path, 'r') as f:
            content2 = f.read().strip()
        assert content2 in MESSAGES
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
def test_cli_total_flag():
    """CLI should support --total to show total number of messages."""
    import subprocess
    from today import get_message_count
    result = subprocess.run(["python", "today.py", "--total"], capture_output=True, text=True)
    assert result.returncode == 0
    expected = str(get_message_count())
    assert result.stdout.strip() == expected



def test_cli_shuffle_option():
    """CLI should support --shuffle option for deterministic shuffling."""
    import subprocess
    result = subprocess.run(["python", "today.py", "--shuffle", "--count", "3"], capture_output=True, text=True)
    assert result.returncode == 0
    lines = [line.strip() for line in result.stdout.split("\n") if line.strip()]
    assert len(lines) == 3
    # Should be shuffled messages (deterministic based on date)
    # Just check that we got 3 lines and they're from our messages
    from today import MESSAGES
    for line in lines:
        assert line in MESSAGES


def test_get_date_seed():
    """get_date_seed should return correct seed based on date."""
    from today import get_date_seed
    from datetime import datetime

    # Test with specific date
    test_date = datetime(2023, 5, 15)
    expected_seed = 2023 * 10000 + 5 * 100 + 15  # 20230515
    assert get_date_seed(test_date) == expected_seed

    # Test with None (should use current date)
    # We can't test exact value since it depends on when it's run,
    # but we can test that it returns an integer
    seed = get_date_seed(None)
    assert isinstance(seed, int)
    # Seed should be reasonable for current year (assuming we're in 2020s)
    assert 20200101 <= seed <= 20301231


def test_get_weekday_message():
    """get_weekday_message should return correct message for each weekday."""
    from today import get_weekday_message, MESSAGES
    
    # Test all weekdays (0=Monday to 6=Sunday)
    for weekday in range(7):
        result = get_weekday_message(weekday)
        assert isinstance(result, str)
        assert result in MESSAGES
        
    # Test deterministic behavior - same weekday should return same message
    monday_msg_1 = get_weekday_message(0)
    monday_msg_2 = get_weekday_message(0)
    assert monday_msg_1 == monday_msg_2
    
    # Different weekdays should return different messages (with high probability)
    messages = [get_weekday_message(i) for i in range(7)]
    # At least some should be different (though theoretically they could collide)
    assert len(set(messages)) > 1  # Very unlikely all 7 are the same
    
    # Test error handling
    try:
        get_weekday_message(-1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected
        
    try:
        get_weekday_message(7)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected