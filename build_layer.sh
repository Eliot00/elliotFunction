#!/bin/bash
set -eo pipefail
echo "Install dependencies"
rm -rf ./shared
pip3 install --target ./shared/python -r requirements.txt
echo "Start build"
time sam build --use-container