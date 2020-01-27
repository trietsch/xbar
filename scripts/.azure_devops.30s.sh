#!/usr/bin/env bash

# <bitbar.title>Azure DevOps Pull Request status</bitbar.title>
# <bitbar.desc>Shows open pull requests and your review status</bitbar.desc>
# <bitbar.author>Robin Trietsch</bitbar.author>
# <bitbar.author.github>trietsch</bitbar.author.github>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://gitlab.com/trietsch/bitbar</bitbar.abouturl>

# Settings can be found in the ../config/azure_devops-config.ini file
# If it doesn't exist, copy the template file and fill out the details

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

"./python/wrapper.sh" "azure_devops"
