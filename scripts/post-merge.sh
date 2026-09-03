#!/usr/bin/env bash
set -euo pipefail

python -m pip install --disable-pip-version-check --no-input --break-system-packages -r requirements.txt
python -m compileall -q app.py
python scripts/check_translations.py
