#!/bin/bash

set -e



inputs=(*.py tests/* common/* api/*)

for input in "${inputs[@]}"; do
  # run black
  black "$input"
  # stop the build if there are Python syntax errors or undefined names
  flake8 "$input" --count --select=E9,F63,F7,F82 --show-source --statistics
  # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
  flake8 "$input" --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
done

echo "✨ Files are beautiful ! ❤️"