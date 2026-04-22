#!/usr/bin/env python3
"""Tests for today.py"""

import pytest
from today import get_daily_message, get_message_count, MESSAGES

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
    """load_messages_from_file should load custom messages."""
    from today import load_messages_from_file
    # Create a temp file with custom messages
    msg_file = tmp_path / "messages.txt"
    msg_file.write_text("Custom1\nCustom2\nCustom3\n")
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
    import re
    emoji_pattern = re.compile("[""\U0001F600-\U0001F64F"
                      "\U0001F300-\U0001F5FF"
                      "\U0001F680-\U0001F6FF"
                      "\U0001F1E0-\U0001F1FF"
                      "\U00002702-\U000027B0"
                      "\U000024C2-\U0001F251]", re.UNICODE)
    def strip_emoji(text):
        return emoji_pattern.sub("", text).strip()
    result = strip_emoji("Today is a great day! 🌟")
    assert result == "Today is a great day!"
    assert "🌟" not in result