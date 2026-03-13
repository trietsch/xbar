# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a collection of [SwiftBar](https://github.com/swiftbar/SwiftBar) plugins for macOS that display developer tool status (pull requests, CI pipelines, on-call schedule) in the menu bar. Scripts are shell wrappers that invoke Python modules via `uv`.

## Commands

```bash
# Install dependencies
uv sync

# Run a module directly (from repo root)
cd plugins && uv run --project .. python -m pull_requests
cd plugins && uv run --project .. python -m gitlab_ci
cd plugins && uv run --project .. python -m motd
```

Scripts in `scripts/` are the actual xbar plugin files. Copy a template from `scripts/template/` (removing `.template`) to `scripts/` to enable it.

## Architecture

### Module layout (`plugins/`)

- **`common/`** — Shared infrastructure:
  - `config.py` — `AppConfigReader` reads TOML config; `set_config_source()` overrides which config file/section a module reads from; logging setup
  - `util.py` — `get_config_file()` resolves config paths, string helpers, time utilities
  - `icons.py` — Base64-encoded icons for menu bar items
  - `notification.py` — macOS notification support

- **`pull_requests/`** — Generic PR aggregation and xbar menu rendering:
  - `domain.py` — `PullRequest`, `PullRequestsOverview`, `PullRequestStatus`, `PullRequestSort` dataclasses/enums used by all PR modules
  - `menu.py` — `print_xbar_pull_request_menu()` — renders the xbar output
  - `__main__.py` — Entry point: loads enabled modules from config, fetches PRs concurrently, merges results

- **`azure_devops/`**, **`gitlab_mrs/`**, **`bitbucket/`** — Per-source PR integrations. Each exposes a function that returns a `PullRequestsOverview` and module-specific `Config`/`Icons` classes.

- **`gitlab_ci/`** — GitLab CI pipeline status (separate from PRs)

- **`motd/`** — "Man of the Day" schedule from iCalendar feed

- **`bitbucket_azure_devops/`** — Legacy combined script (superseded by `pull_requests` module)

### Configuration

Config files live in `config/<module>-config.toml` (gitignored). Templates are in `config/template/`.

The primary config is `config/pull_requests-config.toml`:
- `[preferences]` — `enabled_pr_modules` list selects which sources to activate (`azure_devops`, `gitlab_mrs`, `bitbucket`)
- `[azure_devops]`, `[gitlab_mrs]`, `[bitbucket]` — per-source settings

`AppConfigReader.read(module_name)` looks up `config/<module_name>-config.toml` by default, but `set_config_source()` allows a module to read from a different file and section (used by `pull_requests/__main__.py` to redirect each sub-module to read from `pull_requests-config.toml`).

Cache files are stored in `~/Library/Caches/dev.trietsch.xbar/` (macOS) or `~/.cache/dev.trietsch.xbar/` (Linux). Logs go to `~/Library/Application Support/dev.trietsch.xbar/`.