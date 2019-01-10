#!/bin/bash
for FILENAME in $HOME/core/logparsers/logs/*.log; do
    f="$(basename -- $FILENAME)"
    python3 $HOME/core/logparsers/parser.py "$f"
done