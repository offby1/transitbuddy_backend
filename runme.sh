#!/bin/sh

here=$(cd "$(dirname $0)" && pwd)
set -x

cd "${here}"

if ! [ -x $here/.venv/bin/flask ]
then
   poetry install
fi

./.venv/bin/python3 transitbuddy_backend/flask_controller.py &

sleep 1

set -e
# A couple of smoke tests
curl --silent http://127.0.0.1:8000/stationlist | grep Astoria
curl --silent http://127.0.0.1:8000/train/l
wait
