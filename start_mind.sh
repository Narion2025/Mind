#!/usr/bin/env bash
python3 mind_bootstrap.py &
PORT=${PORT:-8000} python3 mind_bus_api.py
