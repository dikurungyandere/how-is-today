# how-is-today

A daily message generator that provides motivational messages for each day.

## Installation

```bash
pip install -e .
```

## Usage

```bash
python today.py --message    # Show today's message
python today.py --random    # Show random message
python today.py --list      # List all messages
python today.py --list --json  # Output all messages as JSON array
python today.py -i 5        # Get message by index
python today.py -t         # Get message for tomorrow
python today.py --previous 3  # Get messages for the previous 3 days
python today.py --next 7   # Get messages for the next 7 days
python today.py -d 2025-01-01  # Get message for specific date
python today.py --json      # Output as JSON
python today.py -f msgs.txt # Load custom messages from file
python today.py --show-date --next 3   # Show messages for the next 3 days with dates
python today.py --show-date -m  # Show today's message with date
```

## Python API

```python
from today import (get_daily_message, get_random_message, get_message_count,
                   get_message_by_index, get_shuffled_messages, get_date_seed,
                   get_weekday_message, get_tomorrow_message, get_yesterday_message,
                   get_next_n_messages, get_previous_n_messages, get_messages_between_dates,
                   strip_emoji, load_messages_from_file, load_config)

# Get a daily message (deterministic by date)
print(get_daily_message())

# Get a random message (non-deterministic)
print(get_random_message())

# Get total number of messages
print(get_message_count())

# Get message by index (0-based)
print(get_message_by_index(5))

# Get a shuffled list (deterministic by date/seed)
print(get_shuffled_messages())
print(get_shuffled_messages(seed=42, count=5))

# Get message for a specific weekday (0=Monday, 6=Sunday)
print(get_weekday_message(0))  # Monday's message

# Get messages for relative dates
print(get_tomorrow_message())
print(get_yesterday_message())

# Get messages for a range of days
print(get_next_n_messages(3))      # Next 3 days starting today
print(get_previous_n_messages(3))  # Previous 3 days ending yesterday

# NEW: Get messages for an explicit date range
from datetime import datetime
start = datetime(2023, 1, 1)
end = datetime(2023, 1, 10)
print(get_messages_between_dates(start, end))
print(get_messages_between_dates(start, end, count=5))  # Limit to 5

# Strip emojis from messages
print(strip_emoji("Today is great! 🌟"))

# Load custom messages from file
custom = load_messages_from_file("my_messages.txt")

# Load configuration
config = load_config()
```

## Output

The message changes daily based on the date, providing consistent output for the same day.

---

Generated with ❤️ for motivation