#!/usr/bin/env bash

source venv/bin/activate
FLASK_APP=server.py FLASK_ENV=production python3 -m flask run --host=0.0.0.0