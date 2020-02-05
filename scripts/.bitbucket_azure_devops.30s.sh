#!/usr/bin/env bash

# <bitbar.title>Bitbucket PR</bitbar.title>
# <bitbar.desc>Shows the status of PRs in a Bitbucket instance</bitbar.desc>
# <bitbar.author>Robin Trietsch</bitbar.author>
# <bitbar.author.github>trietsch</bitbar.author.github>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://gitlab.com/trietsch/bitbar</bitbar.abouturl>

# Settings can be found in the ../config/bitbucket_azure_devops-config.ini file
# If it doesn't exist, copy the template file and fill out the details
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

"./python/wrapper.sh" "bitbucket_azure_devops"
