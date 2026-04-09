#!/usr/bin/env python3
"""Daily message generator - shows how today is going."""

import random
import json
from datetime import datetime
import argparse

MESSAGES = [
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
]

def get_daily_message(seed=None):
    """Get a message based on today's date for consistency."""
    today = datetime.now()
    if seed is None:
        seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    return random.choice(MESSAGES)

def main():
    parser = argparse.ArgumentParser(description="Generate a daily message")
    parser.add_argument("-m", "--message", action="store_true", help="Show message of the day")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of messages to show")
    parser.add_argument("-r", "--random", action="store_true", help="Get a random message (not seeded by date)")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    if args.random:
        message = random.choice(MESSAGES)
    else:
        message = get_daily_message()
    
    if args.json:
        output = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "message": message,
            "message_index": MESSAGES.index(message)
        }
        print(json.dumps(output))
    elif args.message or args.count > 1:
        for i in range(args.count):
            print(get_daily_message(seed=i))
    else:
        print(message)

if __name__ == "__main__":
    main()
