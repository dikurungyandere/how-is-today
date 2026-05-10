# how-is-today

A daily message generator that provides motivational messages for each day.

## Installation

```bash
pip install -e .
```

## Usage

```bash
python today.py --message          # Show today's message
python today.py --random           # Show random message
python today.py --list             # List all messages
python today.py --list --json      # Output all messages as JSON array
python today.py -i 5               # Get message by index (0-based)
python today.py -I                 # Get message index for today (numeric identifier)
python today.py -I --date 2023-05-15  # Get index for specific date
python today.py -t                # Get message for tomorrow
python today.py --yesterday-weekday   # Get yesterday's weekday message
python today.py --tomorrow-weekday    # Get tomorrow's weekday message
python today.py --previous 3      # Get messages for the previous 3 days
python today.py --next 7          # Get messages for the next 7 days
python today.py --from-date 2023-01-01 --to-date 2023-01-10  # Get messages for a date range
python today.py -d 2025-01-01    # Get message for specific date
python today.py --json           # Output as JSON
python today.py -f msgs.txt      # Load custom messages from file
python today.py --show-date --next 3   # Show messages with dates
python today.py --show-date -m   # Show today's message with date
python today.py --search <query> # Search messages containing text or emoji
python today.py --stats          # Show statistics about messages (count, lengths, emoji info)
python today.py --total          # Show total number of messages
python today.py --emoji-count    # Show total emoji count in output messages
```

## Python API

```python
from today import (get_daily_message, get_random_message, get_random_sample, get_message_count,
                   get_message_by_index, get_shuffled_messages, get_date_seed,
                   get_weekday_message, get_tomorrow_message, get_yesterday_message,
                   get_next_n_messages, get_previous_n_messages, get_messages_between_dates,
                   get_message_index_for_date, search_messages, get_messages_statistics,
                   strip_emoji, contains_emoji, count_emojis, load_messages_from_file, load_config)

# Get a daily message (deterministic by date)
print(get_daily_message())

# Get the numeric index (0–15) for a specific day — useful for stable identifiers
print(get_message_index_for_date())  # Today's index
print(get_message_index_for_date(date=datetime(2023, 5, 15)))

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

# Get messages for an explicit date range
from datetime import datetime
start = datetime(2023, 1, 1)
end = datetime(2023, 1, 10)
print(get_messages_between_dates(start, end))
print(get_messages_between_dates(start, end, count=5))  # Limit to 5

# Search messages by text or emoji
search_messages("day")  # All messages containing "day"
search_messages("🌟")     # All messages with star emoji
search_messages("Great", case_sensitive=True)

# Get statistics about messages
from today import get_messages_statistics
stats = get_messages_statistics()
print(f"Total: {stats['total']}")
print(f"Unique emojis: {len(stats['unique_emojis'])}")
print(f"Total emoji count: {stats['total_emojis']}")

# Get a random sample of N unique messages (without replacement)
print(get_random_sample(5))

# Strip emojis from messages
print(strip_emoji("Today is great! 🌟"))

# Check if a message contains emoji
print(contains_emoji("Today is great! 🌟"))  # True

# Count emojis in a message
print(count_emojis("Today is great! 🌟"))  # 1

# Load custom messages from file
custom = load_messages_from_file("my_messages.txt")

# Load configuration
config = load_config()
```

## Output

The message changes daily based on the date, providing consistent output for the same day.

---

Generated with ❤️ for motivation