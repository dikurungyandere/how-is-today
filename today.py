#!/usr/bin/env python3
"""Daily message generator - shows how today is going.

Examples:
    python today.py --message    # Show today's message
    python today.py --random    # Show random message
    python today.py --list    # List all messages
"""

__all__ = ["get_daily_message", "get_random_message", "get_random_sample", "get_message_count",
           "get_message_by_index", "get_shuffled_messages", "get_date_seed",
           "get_weekday_message", "get_week_messages", "get_next_week_messages", "get_business_week_messages", "get_tomorrow_message", "get_yesterday_message",
           "get_next_n_messages", "get_previous_n_messages", "get_messages_between_dates",
           "get_message_index_for_date", "search_messages", "get_messages_statistics", "MESSAGES", "VERSION",
           "strip_emoji", "contains_emoji", "count_emojis", "load_messages_from_file", "load_config"]

from datetime import datetime, timedelta
from typing import Optional, List

import random
from random import Random
import json
import sys
import argparse
import os
import pathlib
import re

MESSAGES: List[str] = [
    "Today is a great day! 🌟",
    "Keep pushing, you're doing amazing! 💪",
    "A fresh start awaits you! ✨",
    "Small steps lead to big changes! 🚀",
    "Today brings new opportunities! 🎯",
    "Believe in yourself today! 💫",
    "Adventure awaits around every corner! 🗺️",
    "Your hard work is paying off! 🌈",
    "Stay positive, good things happen! ☀️",
    "Today is what you make of it! 🎨",
    "Every moment is a fresh beginning! 🌅",
    "You are capable of amazing things! ⭐",
    "Today is full of possibilities! 🌿",
    "Make it count! 🎪",
    "Progress, not perfection! 📈",
    "You got this! 🤝",
]

def get_message_count() -> int:
    """Return the total number of available messages."""
    return len(MESSAGES)

def get_message_by_index(index: int, messages: Optional[List[str]] = None) -> Optional[str]:
    """Return message at given index, or None if out of range."""
    msg_list = messages if messages is not None else MESSAGES
    if 0 <= index < len(msg_list):
        return msg_list[index]
    return None

def load_messages_from_file(filepath: str) -> Optional[List[str]]:
    """Load custom messages from a file (one per line, ignoring empty lines and comments)."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        messages = []
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            messages.append(line)
    return messages if messages else None

def load_config() -> dict:
    """Load user config from ~/.config/how-is-today.json or equivalent."""
    config_paths = [
        pathlib.Path.home() / ".config" / "how-is-today.json",
        pathlib.Path.home() / ".how-is-today.json",
    ]
    for path in config_paths:
        if path.exists():
            try:
                with open(path) as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
    return {}

def get_random_message() -> str:
    """Return a random message (not seeded by date)."""
    return random.choice(MESSAGES)

def get_random_sample(n: int, messages: Optional[List[str]] = None) -> List[str]:
    """Return a random sample of n unique messages (without replacement).

    Args:
        n: Number of unique messages to sample.
        messages: Optional custom message list to sample from. Defaults to MESSAGES.

    Returns:
        List of n randomly selected unique messages.

    Raises:
        ValueError: If n is negative or exceeds the number of available messages.
    """
    source = messages if messages is not None else MESSAGES
    return random.sample(source, n)

def get_daily_message(seed: Optional[int] = None, date: Optional[datetime] = None) -> str:
    """Get a message based on date for consistency."""
    if date is None:
        date = datetime.now()
    if seed is None:
        seed = date.year * 10000 + date.month * 100 + date.day
    # Use local Random instance to avoid affecting global random state
    local_random = Random(seed)
    return local_random.choice(MESSAGES)

def get_shuffled_messages(seed: Optional[int] = None, date: Optional[datetime] = None, count: Optional[int] = None) -> List[str]:
    """Get all messages in shuffled order (deterministic based on seed/date).

    The same seed and date will always produce the same shuffled list, making
    the output deterministic for a given day. If no seed is provided, the seed
    is derived from the date.

    Args:
        seed: Optional seed for the random number generator. If None, uses date-based seed.
        date: Optional date to derive the seed from. If None, uses current date.
        count: Optional number of messages to return from the shuffled list. If None, returns all messages.

    Returns:
        A list of messages in shuffled order.
    """
    if date is None:
        date = datetime.now()
    if seed is None:
        seed = date.year * 10000 + date.month * 100 + date.day
    local_random = Random(seed)
    shuffled = MESSAGES.copy()
    local_random.shuffle(shuffled)
    if count is not None:
        return shuffled[:count]
    return shuffled

def get_date_seed(date: Optional[datetime] = None) -> int:
    """Get the deterministic seed for a given date (or today if None).

    Args:
        date: Optional date to derive the seed from. If None, uses current date.

    Returns:
        Integer seed based on YYYYMMDD format.
    """
    if date is None:
        date = datetime.now()
    return date.year * 10000 + date.month * 100 + date.day

def get_weekday_message(weekday: int) -> str:
    """Get the message for a given weekday (0=Monday, 6=Sunday).

    The message is deterministic for each weekday, independent of the date.

    Args:
        weekday: Integer from 0 (Monday) to 6 (Sunday).

    Returns:
        The message for the given weekday.
    """
    if not 0 <= weekday <= 6:
        raise ValueError("Weekday must be between 0 (Monday) and 6 (Sunday)")
    # Use a seed that is unique for each weekday and unlikely to conflict with date-based seeds.
    seed = 10000 + weekday  # 10000 to 10006
    return get_daily_message(seed=seed)

def get_week_messages(start_monday: Optional[datetime] = None) -> List[str]:
    """Get all 7 weekday messages for the week containing the given Monday.

    Returns messages in week order (Monday through Sunday). If no Monday is
    provided, uses the current week (starting from this week's Monday).

    Args:
        start_monday: Optional Monday date that starts the week. If None, uses
            the current week's Monday (determined from today's date).

    Returns:
        List of 7 messages, one for each weekday Mon–Sun in order.
    """
    if start_monday is None:
        # Find this week's Monday from current date
        today = datetime.now()
        days_since_monday = today.weekday()  # 0=Mon, 6=Sun
        start_monday = today - timedelta(days=days_since_monday)
    # Generate messages for Monday (0) through Sunday (6)
    return [get_weekday_message(i) for i in range(7)]

def get_next_week_messages() -> List[str]:
    """Get all 7 weekday messages for next week (Mon–Sun).

    Returns:
        List of 7 messages for the next calendar week, Monday through Sunday.
    """
    today = datetime.now()
    days_since_monday = today.weekday()
    # Next Monday is in (7 - days_since_monday) days
    next_monday = today + timedelta(days=(7 - days_since_monday))
    return get_week_messages(start_monday=next_monday)

def get_business_week_messages(start_monday: Optional[datetime] = None) -> List[str]:
    """Get the 5 weekday messages (Mon–Fri) for the week containing the given Monday.

    Returns messages in order from Monday through Friday. If no Monday is
    provided, uses the current week's Monday.

    Args:
        start_monday: Optional Monday date that starts the week. If None, uses
            the current week's Monday.

    Returns:
        List of 5 messages, one for each weekday Mon–Fri in order.
    """
    week_msgs = get_week_messages(start_monday)
    return week_msgs[:5]  # Monday (0) to Friday (4)

def get_tomorrow_message() -> str:
    """Get the message for tomorrow.

    Returns:
        The deterministic message for tomorrow based on the date.
    """
    from datetime import timedelta
    return get_daily_message(date=datetime.now() + timedelta(days=1))

def get_yesterday_message() -> str:
    """Get the message for yesterday.

    Returns:
        The deterministic message for yesterday based on the date.
    """
    from datetime import timedelta
    return get_daily_message(date=datetime.now() - timedelta(days=1))

def get_next_n_messages(n: int) -> List[str]:
    """Get messages for the next N consecutive days starting from today.

    Args:
        n: Number of consecutive days (must be non-negative).

    Returns:
        A list of deterministic daily messages for the next N days.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    from datetime import timedelta
    messages = []
    for i in range(n):
        day = datetime.now() + timedelta(days=i)
        messages.append(get_daily_message(date=day))
    return messages

def get_previous_n_messages(n: int) -> List[str]:
    """Get messages for the previous N consecutive days ending with yesterday.

    Args:
        n: Number of consecutive past days (must be non-negative).

    Returns:
        A list of deterministic daily messages for the previous N days,
        ordered from most recent to oldest (yesterday first, then going back).

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    from datetime import timedelta
    messages = []
    for i in range(1, n + 1):  # Start from 1 day ago up to n days ago
        day = datetime.now() - timedelta(days=i)
        messages.append(get_daily_message(date=day))
    return messages

def get_messages_between_dates(start_date: datetime, end_date: datetime, count: Optional[int] = None) -> List[str]:
    """Get messages for each day in a date range [start_date, end_date] (inclusive).

    Args:
        start_date: Start date (inclusive).
        end_date: End date (inclusive). Must be >= start_date.
        count: Optional maximum number of messages to return. If None, returns all days in range.

    Returns:
        A list of deterministic daily messages for each day in the range,
        ordered from start_date to end_date.

    Raises:
        ValueError: If end_date is before start_date.
    """
    if end_date < start_date:
        raise ValueError("end_date must be >= start_date")
    from datetime import timedelta
    messages = []
    current = start_date
    while current <= end_date:
        messages.append(get_daily_message(date=current))
        current += timedelta(days=1)
    if count is not None:
        return messages[:count]
    return messages

def get_message_index_for_date(date: Optional[datetime] = None, seed: Optional[int] = None) -> int:
    """Get the deterministic message index for a given date.

    This returns the numerical index (0 to len(MESSAGES)-1) that would be selected
    for the date, without returning the message itself. Useful for integrations
    that need a stable numeric identifier per day.

    Args:
        date: Optional date to derive the seed from. If None, uses current date.
        seed: Optional explicit seed. If provided, overrides date-based seeding.

    Returns:
        Integer index into the MESSAGES list.
    """
    if date is None:
        date = datetime.now()
    if seed is None:
        seed = date.year * 10000 + date.month * 100 + date.day
    local_random = Random(seed)
    return local_random.randrange(len(MESSAGES))

def search_messages(query: str, messages: Optional[List[str]] = None, case_sensitive: bool = False) -> List[str]:
    """Search messages for a substring (text or emoji).

    Args:
        query: Substring to search for (can be text or emoji).
        messages: Optional custom message list to search. Defaults to MESSAGES.
        case_sensitive: If True, match case; otherwise case-insensitive.

    Returns:
        List of messages containing the query substring.
    """
    source = messages if messages is not None else MESSAGES
    if not case_sensitive:
        query = query.lower()
        return [msg for msg in source if query in msg.lower()]
    return [msg for msg in source if query in msg]

# Emoji stripping utility
emoji_pattern = re.compile("["
                      "\U0001F600-\U0001F64F"
                      "\U0001F300-\U0001F5FF"
                      "\U0001F680-\U0001F6FF"
                      "\U0001F1E0-\U0001F1FF"
                      "\U00002702-\U000027B0"
                      "\U0001F900-\U0001F9FF"
                      "\U000024C2-\U0001F251]", re.UNICODE)

def strip_emoji(text: str) -> str:
    """Remove emojis from input text."""
    return emoji_pattern.sub("", text).strip()

def contains_emoji(text: str) -> bool:
    """Check if the text contains any emoji."""
    return bool(emoji_pattern.search(text))

def count_emojis(text: str) -> int:
    """Count the number of emoji characters in the given text."""
    return len(emoji_pattern.findall(text))

def get_messages_statistics(messages: Optional[List[str]] = None) -> dict:
    """Compute statistics for a list of messages.

    Args:
        messages: Optional custom message list. Defaults to MESSAGES.

    Returns:
        A dictionary with keys:
            - total: total message count
            - average_length: average character length (including emojis)
            - average_length_no_emoji: average length after stripping emojis
            - total_emojis: total emoji occurrences across all messages
            - unique_emojis: list of unique emoji characters found
            - emoji_counts: dict mapping each emoji to its count
            - messages_with_emoji: count of messages containing at least one emoji
            - messages_without_emoji: count of messages with no emojis
    """
    source = messages if messages is not None else MESSAGES
    total = len(source)
    total_chars = sum(len(msg) for msg in source)
    total_chars_no_emoji = sum(len(strip_emoji(msg)) for msg in source)

    emoji_counts = {}
    messages_with_emoji = 0
    messages_without_emoji = 0

    for msg in source:
        found = emoji_pattern.findall(msg)
        if found:
            messages_with_emoji += 1
            for e in found:
                emoji_counts[e] = emoji_counts.get(e, 0) + 1
        else:
            messages_without_emoji += 1

    unique_emojis = list(emoji_counts.keys())

    return {
        "total": total,
        "average_length": round(total_chars / total, 2) if total else 0,
        "average_length_no_emoji": round(total_chars_no_emoji / total, 2) if total else 0,
        "total_emojis": sum(emoji_counts.values()),
        "unique_emojis": unique_emojis,
        "emoji_counts": emoji_counts,
        "messages_with_emoji": messages_with_emoji,
        "messages_without_emoji": messages_without_emoji,
    }

VERSION = "1.0.0"

def main():
    from datetime import timedelta

    parser = argparse.ArgumentParser(description="Generate a daily message")
    parser.add_argument("-m", "--message", action="store_true", help="Show message of the day")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of messages to show")
    parser.add_argument("-r", "--random", action="store_true", help="Get a random message (not seeded by date)")
    parser.add_argument("-d", "--date", type=str, help="Get message for date (YYYY-MM-DD)")
    parser.add_argument("-t", "--tomorrow", action="store_true", help="Get message for tomorrow")
    parser.add_argument("-y", "--yesterday", action="store_true", help="Get message for yesterday")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    parser.add_argument("-l", "--list", action="store_true", help="List all available messages")
    parser.add_argument("--plain", action="store_true", help="With --list, output messages one per line without numbering")
    parser.add_argument("-o", "--output", type=str, help="Save message to file")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output (use with -o/--output)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show extra info (seed, date)")
    parser.add_argument("-s", "--seed", type=int, help="Custom seed for message (overrides date-based seeding)")
    parser.add_argument("-i", "--index", type=int, help="Get message by index (0-based)")
    parser.add_argument("--first", action="store_true", help="Get the first message (index 0)")
    parser.add_argument("--last", action="store_true", help="Get the last message (last index)")
    parser.add_argument("-f", "--messages-file", type=str, help="Load custom messages from file (one per line)")
    parser.add_argument("--config", type=str, help="Path to config file (JSON)")
    parser.add_argument("-S", "--shuffle", action="store_true", help="Shuffle messages deterministically")
    parser.add_argument("-R", "--random-sample", type=int, metavar="N", help="Get N unique random messages (without replacement)")
    parser.add_argument("--search", type=str, metavar="QUERY", help="Search messages containing text or emoji (case-insensitive substring match)")
    parser.add_argument("--stats", action="store_true", help="Show statistics about the messages (count, lengths, emoji info)")
    parser.add_argument("-w", "--weekday", type=int, help="Get message for a given weekday (0=Monday, 6=Sunday)")
    parser.add_argument("--today-weekday", action="store_true", help="Show today's weekday message (deterministic by current weekday)")
    parser.add_argument("--yesterday-weekday", action="store_true", help="Show yesterday's weekday message (based on yesterday's day of week)")
    parser.add_argument("--tomorrow-weekday", action="store_true", help="Show tomorrow's weekday message (based on tomorrow's day of week)")
    parser.add_argument("--this-week", action="store_true", help="Show all 7 weekday messages for the current week (Mon–Sun)")
    parser.add_argument("--next-week", action="store_true", help="Show all 7 weekday messages for next week (Mon–Sun)")
    parser.add_argument("--last-week", action="store_true", help="Show all 7 weekday messages for last week (Mon–Sun)")
    parser.add_argument("--business-week", action="store_true", help="Show the 5 weekday messages for the current week (Mon–Fri)")
    parser.add_argument("-e", "--strip-emoji", action="store_true", help="Remove emojis from output")
    parser.add_argument("--emoji-count", action="store_true", help="Show total emoji count across output messages")
    parser.add_argument("--total", action="store_true", help="Show total number of messages and exit")
    parser.add_argument("-C", "--clear", action="store_true", help="Clear the terminal before output")
    parser.add_argument("-n", "--next", type=int, help="Show messages for the next N days starting from the target date")
    parser.add_argument("-p", "--previous", type=int, help="Show messages for the previous N days ending with yesterday")
    parser.add_argument("--from-date", type=str, help="Start date for range (YYYY-MM-DD), use with --to-date")
    parser.add_argument("--to-date", type=str, help="End date for range (YYYY-MM-DD), use with --from-date")
    parser.add_argument("-D", "--show-date", action="store_true", help="Prefix each message with its date (YYYY-MM-DD)")
    parser.add_argument("-I", "--index-only", action="store_true", help="Print only the message index (0-based) and exit")
    parser.add_argument("--seed-only", action="store_true", help="Print only the deterministic seed for the date and exit")
    args = parser.parse_args()
    if args.clear:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    # Load config file if specified, or use default config
    config = {}
    if args.config:
        config_path = pathlib.Path(args.config)
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error: Could not load config: {e}", file=sys.stderr)
                sys.exit(1)
    else:
        config = load_config()

    # Load custom messages if file specified
    custom_messages = None
    if args.messages_file:
        custom_messages = load_messages_from_file(args.messages_file)
        if custom_messages is None:
            print(f"Error: Could not load messages from '{args.messages_file}'", file=sys.stderr)
            sys.exit(1)

    active_messages = custom_messages if custom_messages is not None else MESSAGES

    if args.stats:
        stats = get_messages_statistics(active_messages)
        # Output handling: respects --output/-o and --quiet/-q
        if args.output:
            output_str = json.dumps(stats, indent=2) if args.json else (
                f"Total messages: {stats['total']}\n"
                f"Average length: {stats['average_length']} chars (with emojis), {stats['average_length_no_emoji']} chars (without emojis)\n"
                f"Messages with emoji: {stats['messages_with_emoji']}\n"
                f"Messages without emoji: {stats['messages_without_emoji']}\n"
                f"Total emoji occurrences: {stats['total_emojis']}\n"
                f"Unique emojis: {len(stats['unique_emojis'])} {''.join(stats['unique_emojis'])}\n"
            )
            with open(args.output, "w") as f:
                f.write(output_str)
            if not args.quiet:
                print(f"Saved to {args.output}", file=sys.stderr)
        elif not args.quiet:
            if args.json:
                print(json.dumps(stats, indent=2))
            else:
                print(f"Total messages: {stats['total']}")
                print(f"Average length: {stats['average_length']} chars (with emojis), {stats['average_length_no_emoji']} chars (without emojis)")
                print(f"Messages with emoji: {stats['messages_with_emoji']}")
                print(f"Messages without emoji: {stats['messages_without_emoji']}")
                print(f"Total emoji occurrences: {stats['total_emojis']}")
                print(f"Unique emojis: {len(stats['unique_emojis'])} {''.join(stats['unique_emojis'])}")
                if args.verbose:
                    print("Emoji counts:")
                    for emoji, count in sorted(stats['emoji_counts'].items(), key=lambda x: (-x[1], x[0])):
                        print(f"  {emoji}: {count}")
        return

    if args.list:
        count = args.count if args.count > 1 else len(active_messages)
        messages_to_show = active_messages[:count]
        if args.json:
            print(json.dumps(messages_to_show))
        else:
            if args.plain:
                for msg in messages_to_show:
                    print(msg)
            else:
                for i, msg in enumerate(messages_to_show, 1):
                    print(f"{i}. {msg}")
        return

    # Parse date and seed for message generation
    target_date = None
    if args.tomorrow:
        from datetime import timedelta
        target_date = datetime.now() + timedelta(days=1)
    elif args.yesterday:
        from datetime import timedelta
        target_date = datetime.now() - timedelta(days=1)
    elif args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    custom_seed = args.seed if args.seed else None

    if args.version:
        print(f"how-is-today {VERSION}")
        return

    if args.total:
        if args.json:
            print(json.dumps(get_message_count()))
        else:
            print(get_message_count())
        return

    if args.shuffle:
        shuffled = get_shuffled_messages(seed=custom_seed, date=target_date, count=args.count)
        for msg in shuffled:
            print(strip_emoji(msg) if args.strip_emoji else msg)
        return

    if args.index is not None:
        msg = get_message_by_index(args.index, custom_messages)
        if msg is None:
            print(f"Error: Index {args.index} out of range (0-{len(active_messages)-1})", file=sys.stderr)
            sys.exit(1)
        print(strip_emoji(msg) if args.strip_emoji else msg)
        return

    if args.first:
        msg = get_message_by_index(0, custom_messages)
        print(strip_emoji(msg) if args.strip_emoji else msg)
        return

    if args.last:
        msg = get_message_by_index(len(active_messages) - 1, custom_messages)
        print(strip_emoji(msg) if args.strip_emoji else msg)
        return

    if args.index_only:
        idx = get_message_index_for_date(seed=custom_seed, date=target_date)
        print(idx)
        return

    if args.seed_only:
        seed = custom_seed if custom_seed is not None else get_date_seed(target_date)
        print(seed)
        return

    if args.next is not None:
        from datetime import timedelta
        if target_date is None:
            target_date = datetime.now()
        messages = []
        for i in range(args.next):
            day = target_date + timedelta(days=i)
            messages.append(get_daily_message(seed=custom_seed, date=day))
    elif args.previous is not None:
        from datetime import timedelta
        if target_date is None:
            target_date = datetime.now()
        messages = []
        for i in range(1, args.previous + 1):  # Start from 1 day ago
            day = target_date - timedelta(days=i)
            messages.append(get_daily_message(seed=custom_seed, date=day))
    elif args.from_date and args.to_date:
        try:
            start_date = datetime.strptime(args.from_date, "%Y-%m-%d")
            end_date = datetime.strptime(args.to_date, "%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format for --from-date/--to-date. Use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
        # For explicit date range, use count if provided and > 0, else get all days
        range_count = args.count if args.count > 1 else None
        messages = get_messages_between_dates(start_date, end_date, count=range_count)
    elif args.weekday is not None:
        try:
            msg = get_weekday_message(args.weekday)
            messages = [msg] * args.count
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.today_weekday:
        try:
            weekday = datetime.now().weekday()
            msg = get_weekday_message(weekday)
            messages = [msg] * args.count
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.yesterday_weekday:
        try:
            from datetime import timedelta
            weekday = (datetime.now() - timedelta(days=1)).weekday()
            msg = get_weekday_message(weekday)
            messages = [msg] * args.count
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.tomorrow_weekday:
        try:
            from datetime import timedelta
            weekday = (datetime.now() + timedelta(days=1)).weekday()
            msg = get_weekday_message(weekday)
            messages = [msg] * args.count
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.this_week:
        # Get the current week's Monday
        today = datetime.now()
        days_since_monday = today.weekday()
        week_monday = today - timedelta(days=days_since_monday)
        messages = get_week_messages(start_monday=week_monday)
    elif args.next_week:
        # Get next week's Monday
        today = datetime.now()
        days_since_monday = today.weekday()
        next_week_monday = today + timedelta(days=(7 - days_since_monday))
        messages = get_week_messages(start_monday=next_week_monday)
    elif args.last_week:
        # Get last week's Monday
        today = datetime.now()
        days_since_monday = today.weekday()
        last_week_monday = today - timedelta(days=days_since_monday + 7)
        messages = get_week_messages(start_monday=last_week_monday)
    elif args.business_week:
        # Get the current week's Monday
        today = datetime.now()
        days_since_monday = today.weekday()
        week_monday = today - timedelta(days=days_since_monday)
        messages = get_business_week_messages(start_monday=week_monday)
    elif args.random_sample is not None:
        try:
            messages = get_random_sample(args.random_sample, custom_messages)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.search is not None:
        messages = search_messages(args.search, custom_messages)
        if not messages:
            print(f"No messages found matching '{args.search}'", file=sys.stderr)
            sys.exit(1)
    else:
        msg_source = custom_messages if custom_messages is not None else MESSAGES
        if args.random:
            messages = [random.choice(msg_source) for _ in range(args.count)]
        elif args.message or args.count > 1:
            messages = [get_daily_message(seed=(custom_seed if custom_seed is not None else get_date_seed(target_date)) + i, date=target_date) for i in range(args.count)]
        else:
            messages = [get_daily_message(seed=custom_seed, date=target_date)]

    total_emojis = None
    if args.emoji_count:
        total_emojis = sum(count_emojis(m) for m in messages)

    if args.output:
        with open(args.output, "w") as f:
            f.write("\n".join(messages))
        if not args.quiet:
            print(f"Saved to {args.output}", file=sys.stderr)
    elif args.json:
        output = {
            "date": (target_date or datetime.now()).strftime("%Y-%m-%d"),
            "messages": messages,
            "mode": "random" if args.random else "daily",
            "message_count": len(MESSAGES)
        }
        if custom_seed is not None:
            output["seed"] = custom_seed
        output["generated_at"] = datetime.now().isoformat()
        if total_emojis is not None:
            output["total_emojis"] = total_emojis
        print(json.dumps(output))
    else:
        if args.show_date:
            # Build date strings for each message when applicable
            if args.next is not None:
                base = target_date if target_date else datetime.now()
                date_strings = [(base + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(len(messages))]
            elif args.previous is not None:
                base = target_date if target_date else datetime.now()
                date_strings = [(base - timedelta(days=i+1)).strftime("%Y-%m-%d") for i in range(len(messages))]
            elif not args.random and args.weekday is None:
                base = target_date if target_date else datetime.now()
                date_str = base.strftime("%Y-%m-%d")
                date_strings = [date_str] * len(messages)
            else:
                date_strings = None
            if date_strings:
                for ds, msg in zip(date_strings, messages):
                    output_msg = strip_emoji(msg) if args.strip_emoji else msg
                    print(f"{ds}: {output_msg}")
            else:
                for msg in messages:
                    output_msg = strip_emoji(msg) if args.strip_emoji else msg
                    print(output_msg)
        else:
            for msg in messages:
                output_msg = strip_emoji(msg) if args.strip_emoji else msg
                print(output_msg)
        if args.emoji_count:
            print(f"Total emojis: {total_emojis}")

    if args.verbose and not args.json:
        seed = custom_seed if custom_seed else (target_date.year * 10000 + target_date.month * 100 + target_date.day) if target_date else int(datetime.now().strftime("%Y%m%d"))
        print(f"Seed: {seed}", file=sys.stderr)
        print(f"Date: {(target_date or datetime.now()).strftime("%Y-%m-%d")}", file=sys.stderr)

if __name__ == "__main__":
    main()
