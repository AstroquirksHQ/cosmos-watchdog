#!/bin/bash
set -e

export ENV=TEST

if [ -z "$1" ]
then
    pytest tests/integration
else
    pytest tests/integration -k "$1"
fi