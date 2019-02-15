#!/bin/bash

deactivate || true
rm -rf *.egg-info __pycache__/ venv || true

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel
pip install --editable .
eval "$(_MYCLI_COMPLETE=source mycli)"
