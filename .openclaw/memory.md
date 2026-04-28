# Memory

- 2026-04-28: Add --total flag to show total number of messages and exit
- 2026-04-28: Added -y/--yesterday flag to get message for previous day
- 2026-04-27: Improved load_messages_from_file to ignore empty lines and comments, updated test.
- 2025-04-18: Added get_random_message() utility function and test.
- 2025-04-19: Added __all__ exports and improved module docstring.
- 2025-04-19: Added -i/--index CLI option to get message by index + test.
- 2025-04-20: Added -t/--tomorrow flag to get message for next day.
- 2025-04-20: Fixed get_daily_message to use local Random - avoids corrupting global random state.
- 2025-04-21: Added --messages-file/-f option to load custom messages from file.
- 2025-04-21: Improved README with usage examples, installation instructions, and Python API docs.
- 2025-04-22: Added config file support (load_config, --config CLI option)
- 2025-04-23: Added --shuffle/-S option for deterministic message shuffling
- 2025-04-23: Added tests for get_shuffled_messages (basic + count limit)
- 2025-04-24: Added --strip-emoji/-e option to remove emojis from output
- 2025-04-25: Added test for CLI --strip-emoji option
- 2026-04-23: Added test for --version CLI option
- 2026-04-24: Refactored emoji stripping to module level, fixed MESSAGES syntax error
- 2026-04-24: Added test for --list --count CLI option
- 2026-04-26: Added strip_emoji function to public API and test CLI --strip-emoji option
- 2026-04-26: Improved test_strip_emoji function with comprehensive edge cases
- 2026-04-26: Added test for load_config loading from file
- 2026-04-27: Exported load_messages_from_file and load_config functions in __all__
- 2026-04-27: Added test for CLI output flag functionality
- 2026-04-27: Added test for CLI output flag functionality
- 2026-04-28: Added test for CLI --total flag to show total number of messages
Task completed: Added test for CLI --total flag
Added test for CLI --total flag to show total number of messages
Task completed: Added test for CLI --total flag to show total number of messages
