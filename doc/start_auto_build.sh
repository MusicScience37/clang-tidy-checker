#!/bin/bash

set -e

cd $(dirname $0)
poetry run sphinx-autobuild source build --port 6731
