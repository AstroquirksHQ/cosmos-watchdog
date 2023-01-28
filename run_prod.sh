#!/usr/bin/env bash

set -exo pipefail

# shellcheck disable=SC2046
exec uwsgi -H $(pipenv --venv) --ini uwsgi.ini