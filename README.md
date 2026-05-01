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
python today.py -d 2025-01-01  # Get message for specific date
python today.py --json      # Output as JSON
python today.py -f msgs.txt # Load custom messages from file
```

## Python API

```python
from today import get_daily_message, get_random_message, get_message_count

print(get_daily_message())     # Message for today
print(get_random_message())  # Random message
print(get_message_count())    # Total messages (16)
```

## Output

The message changes daily based on the date, providing consistent output for the same day.

---

Generated with ❤️ for motivation