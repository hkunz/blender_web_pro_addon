#!/bin/zsh

source /path/to/exit-codes.sh
source /path/to/utils.sh

if [ some_condition ]; then
    exit $SUCCESS
else
    exit $ERROR_GENERIC
fi
