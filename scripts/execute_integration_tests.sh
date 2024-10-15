#!/bin/bash

echo "Install test-requirements"
make install-dev-dependencies

echo "Run tests"
pytest -rPf ./eox_tagging/test/integration --ignore=test_api_integration.py
