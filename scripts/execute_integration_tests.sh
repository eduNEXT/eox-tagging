#!/bin/bash

echo "Install requirements"
make test_requirements

echo "Run tests"
pytest -rPf ./eox_tagging/test/integration --ignore=test_api_integration.py
