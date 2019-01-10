#!/bin/bash
for FILENAME in $HOME/cloud/core/logparsers/logs/*.log; do
    f="$(basename -- $FILENAME)"
    python3 $HOME/cloud/core/logparsers/parser.py "$f"
done
