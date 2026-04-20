#!/usr/bin/env python3
"""Daily message generator - shows how today is going.

Examples:
    python today.py --message    # Show today's message
    python today.py --random    # Show random message
    python today.py --list    # List all messages
"""

__all__ = ["get_daily_message", "get_random_message", "get_message_count",
           "get_message_by_index", "MESSAGES", "VERSION"]

from datetime import datetime
from typing import Optional, List

import random
from random import Random
import json
import sys
import argparse

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

def get_message_by_index(index: int) -> Optional[str]:
    """Return message at given index, or None if out of range."""
    if 0 <= index < len(MESSAGES):
        return MESSAGES[index]
    return None

def get_random_message() -> str:
    """Return a random message (not seeded by date)."""
    return random.choice(MESSAGES)

def get_daily_message(seed: Optional[int] = None, date: Optional[datetime] = None) -> str:
    """Get a message based on date for consistency."""
    if date is None:
        date = datetime.now()
    if seed is None:
        seed = date.year * 10000 + date.month * 100 + date.day
    # Use local Random instance to avoid affecting global random state
    local_random = Random(seed)
    return local_random.choice(MESSAGES)

VERSION = "1.0.0"

def main():
    parser = argparse.ArgumentParser(description="Generate a daily message")
    parser.add_argument("-m", "--message", action="store_true", help="Show message of the day")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of messages to show")
    parser.add_argument("-r", "--random", action="store_true", help="Get a random message (not seeded by date)")
    parser.add_argument("-d", "--date", type=str, help="Get message for date (YYYY-MM-DD)")
    parser.add_argument("-t", "--tomorrow", action="store_true", help="Get message for tomorrow")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    parser.add_argument("-l", "--list", action="store_true", help="List all available messages")
    parser.add_argument("-o", "--output", type=str, help="Save message to file")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output (use with -o/--output)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show extra info (seed, date)")
    parser.add_argument("-s", "--seed", type=int, help="Custom seed for message (overrides date-based seeding)")
    parser.add_argument("-i", "--index", type=int, help="Get message by index (0-based)")
    args = parser.parse_args()
    
    if args.list:
        count = args.count if args.count > 1 else len(MESSAGES)
        for i, msg in enumerate(MESSAGES[:count], 1):
            print(f"{i}. {msg}")
        return

    if args.version:
        print(f"how-is-today {VERSION}")
        return

    if args.index is not None:
        msg = get_message_by_index(args.index)
        if msg is None:
            print(f"Error: Index {args.index} out of range (0-{len(MESSAGES)-1})", file=sys.stderr)
            sys.exit(1)
        print(msg)
        return

    quiet = args.quiet

    target_date = None
    if args.tomorrow:
        from datetime import timedelta
        target_date = datetime.now() + timedelta(days=1)
    elif args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    custom_seed = args.seed if args.seed else None
    messages = []
    if args.random:
        messages = [random.choice(MESSAGES) for _ in range(args.count)]
    elif args.message or args.count > 1:
        messages = [get_daily_message(seed=(custom_seed + i) if custom_seed else i, date=target_date) for i in range(args.count)]
    else:
        messages = [get_daily_message(seed=custom_seed, date=target_date)]
    
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
        print(json.dumps(output))
    else:
        for msg in messages:
            print(msg)

    if args.verbose and not args.json:
        seed = custom_seed if custom_seed else (target_date.year * 10000 + target_date.month * 100 + target_date.day) if target_date else int(datetime.now().strftime("%Y%m%d"))
        print(f"Seed: {seed}", file=sys.stderr)
        print(f"Date: {(target_date or datetime.now()).strftime("%Y-%m-%d")}", file=sys.stderr)

if __name__ == "__main__":
    main()
