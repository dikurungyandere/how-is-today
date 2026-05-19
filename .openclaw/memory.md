# Development Log - how-is-today

## 2025-05-19
Added `--case-sensitive` CLI flag for `--search` option. The Python API already supported `case_sensitive` parameter in `search_messages()`, but the CLI was missing this feature. Updated search call to use `args.case_sensitive` and added CLI test for the new flag.

## 2025-05-19
Added test for `--stats` with `-o/--output` flag. The CLI already supported writing stats to file, but there was no dedicated test for this functionality.