#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"

echo "Starting..."

if [ ! -d "data/inbox" ]; then

  echo "Error: data/inbox directory not found"

  exit 1

fi

PYTHONPATH=src python3 -m mail_processor.main

echo "Mail processor finished."
