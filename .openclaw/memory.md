# OpenClaw Memory

- 2026-04-16: Added 4 new motivational messages to MESSAGES list. Simplified quiet variable handling (removed redundant hasattr). Pushed to main.
- 2026-04-15: Added -s/--seed flag to specify custom seed via CLI. Same seed returns same message. Pushed to main.
- 2026-04-15: Added -q/--quiet flag to suppress output (useful with -o/--output), and generated_at timestamp in JSON. Pushed to main.
- 2025-04-15: Added -o/--output flag to save messages to file. Pushed to main.
- 2025-04-14: Added -l/--list flag to show all available messages. Pushed to main.
- 2025-04-11: Added -d/--date flag to get message for specific date (YYYY-MM-DD). Fixed JSON output to show target date. Pushed to main.
- 2025-04-10: Added --version flag to today.py. Pushed to main.
- 2025-04-09: Examined repository how-is-today. Improved today.py by adding seed parameter to get_daily_message() so -c/--count shows unique messages instead of repeating the same one. Pushed to main.