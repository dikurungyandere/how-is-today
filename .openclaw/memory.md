# Memory

- 2025-04-18: Added get_random_message() utility function and test.
- 2025-04-19: Added __all__ exports and improved module docstring.
- 2025-04-19: Added -i/--index CLI option to get message by index + test.
- 2025-04-20: Added -t/--tomorrow flag to get message for next day.
- 2025-04-20: Fixed get_daily_message to use local Random - avoids corrupting global random state.
- 2025-04-21: Added --messages-file/-f option to load custom messages from file.
- 2025-04-21: Improved README with usage examples, installation instructions, and Python API docs.
- 2025-04-22: Added config file support (load_config, --config CLI option)
- 2025-04-23: Added --shuffle/-S option for deterministic message shuffling