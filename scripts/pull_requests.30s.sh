#!/usr/bin/env bash

# <bitbar.title>Pull Requests</bitbar.title>
# <bitbar.desc>Shows open pull requests and your review status</bitbar.desc>
# <bitbar.author>Robin Trietsch</bitbar.author>
# <bitbar.author.github>trietsch</bitbar.author.github>
# <bitbar.dependencies>uv</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/trietsch/xbar</bitbar.abouturl>

export PATH="$HOME/.local/bin:/usr/local/bin:$PATH"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

[ ! -d "$DIR/.venv" ] && uv sync --project "$DIR"

cd "$DIR/src"
exec "$DIR/.venv/bin/python" -m python.pull_requests