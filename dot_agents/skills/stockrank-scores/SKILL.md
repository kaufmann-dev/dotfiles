---
name: stockrank-scores
description: Execute Stockrank score work folders by dispatching one agent per ticker and validating results.toml outputs. Use when Codex is in a Stockrank scores work folder for one mode and harness and the user asks to run or complete score execution for that harness.
---

# Stockrank Scores

Use this skill from a `runs/<id>/scores/work/<mode>/<harness>/` folder.

1. Validate the current directory contains ticker subfolders and each ticker subfolder contains `task.txt`.
2. Parse the expected mode and harness from the current path. The parent folder name is the mode and the current folder name is the harness.
3. Ask the user to confirm that this session is running in the expected harness. Abort if they do not confirm.
4. Run one subagent per ticker folder. Use parallel batches of 5 to 10 ticker folders at a time.
5. Each subagent must follow only its ticker folder's `task.txt`, read that ticker's `data/`, and write that ticker's `results.toml`.
6. After the first pass, verify every ticker folder has a parseable `results.toml` with `ticker`, `score`, `confidence`, and `summary`.
7. Retry missing or invalid ticker results once, again by assigning only that ticker folder's `task.txt`.
8. Report the completed ticker count and list any failed tickers.

Do not score anything from these instructions. The scoring instructions live only in each rendered `task.txt`.
