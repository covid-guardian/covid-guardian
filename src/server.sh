#!/usr/bin/env bash

source venv/bin/activate
FLASK_APP=server.py FLASK_ENV=development python -m flask run