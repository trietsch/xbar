#!/usr/bin/env bash

# <bitbar.title>Man of the Day</bitbar.title>
# <bitbar.desc>Shows today's on-call person from an iCalendar feed</bitbar.desc>
# <bitbar.author>Robin Trietsch</bitbar.author>
# <bitbar.author.github>trietsch</bitbar.author.github>
# <bitbar.dependencies>uv</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/trietsch/xbar</bitbar.abouturl>

export PATH="$HOME/.local/bin:/usr/local/bin:$PATH"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

[ ! -d "$DIR/.venv" ] && uv sync --project "$DIR"

cd "$DIR/plugins"
exec "$DIR/.venv/bin/python" -m motd