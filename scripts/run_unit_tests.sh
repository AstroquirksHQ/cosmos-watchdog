#!/bin/bash

set -e

export ENV=TEST
pytest tests/unit/
