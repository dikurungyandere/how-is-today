# Memory
- 2026-05-07: feat: add search_messages() API and --search CLI flag to filter messages by text/emoji substring; added 8 tests; updated README.
- 2026-05-06: Added --random-sample/-R, get_random_sample() API; fixed emoji regex for U+1F900–U+1F9FF; added pyproject.toml.
- 2026-05-05: Added get_message_index_for_date() and --index-only/-I; fixed multi-message count seeding; cleaned repo.
- 2025-04: Ongoing: Added many utilities and CLI flags: get_random_message, -i/--index, -t/--tomorrow, --messages-file, config, --shuffle, --strip-emoji, --total, -y/--yesterday, get_weekday_message, --next/-n, --previous/-p, get_messages_between_dates, --show-date, contains_emoji, --from-date/--to-date, get_date_seed, --clear; plus extensive tests and README updates. Also fixed local Random usage and UTF-8 encoding.
