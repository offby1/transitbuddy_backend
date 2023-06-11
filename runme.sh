#!/bin/sh

here=$(cd "$(dirname $0)" && pwd)
set -x

cd "${here}"

./.venv/bin/python3 flask_controller.py
