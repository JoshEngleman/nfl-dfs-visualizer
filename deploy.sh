#!/bin/bash
# Simple deployment wrapper using uv
# Usage: ./deploy.sh [all|website|headshots]

# Use the Python from the uv-managed venv
.venv/bin/python src/deploy.py "$@"
