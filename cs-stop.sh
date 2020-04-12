#!/bin/bash

set -u
set -e

# Load environment variables from file
set -o allexport
source environmentVar
set +o allexport

docker-compose -p compatibilityservice down

set +e
set +u