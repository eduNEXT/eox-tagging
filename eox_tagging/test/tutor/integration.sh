#!/bin/bash

# This script installs the package in the edxapp environment, installs test requirements from Open edX and runs the tests using the Tutor settings
echo "Install eox-core(requirement)"
pip install eox-core

echo "Install package"
pip install -e /openedx/eox-tagging

echo "Install test-requirements"
make test-requirements

echo "Run tests"
pytest -s --ds=lms.envs.tutor.test /openedx/eox-tagging/eox_tagging/test/tutor
