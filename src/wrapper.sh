#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MODULE_NAME="$1"
CONFIG_MODULE_NAME="$2"
PATH_TO_CONFIG_FILE=

if [ -z "$CONFIG_MODULE_NAME" ]; then
  PATH_TO_CONFIG_FILE="$DIR/../config/$MODULE_NAME-config.ini"
else
  PATH_TO_CONFIG_FILE="$DIR/../config/$CONFIG_MODULE_NAME-config.ini"
fi

# Get path to Python as defined in the config file of this module
PYTHON_BIN="$(awk -F '=' '{if (! ($0 ~ /^;/) && $0 ~ /python_binary/) print $2}' "$PATH_TO_CONFIG_FILE" | xargs)"

"$PYTHON_BIN" -m "python.$MODULE_NAME"
