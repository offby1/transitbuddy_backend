#!/bin/sh

here=$(cd "$(dirname $0)" && pwd)
set -x

cd "${here}"

if ! [ -x $here/.venv/bin/flask ]
then
   poetry install
fi

./.venv/bin/python3 transitbuddy_backend/flask_controller.py
