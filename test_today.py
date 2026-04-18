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

def test_get_random_message():
    """get_random_message should return a message from MESSAGES."""
    from today import get_random_message
    result = get_random_message()
    assert result in MESSAGES

def test_cli_import():
    """CLI module should be importable without errors."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("today", "today.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "main")