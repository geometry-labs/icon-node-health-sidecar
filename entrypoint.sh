#! /usr/bin/env bash

if [ "$1" = "worker" ]; then
  echo "Migrating backend..."
  cd icon_governance
  alembic upgrade head
  echo "Starting worker..."
  python main_worker.py "$2"
elif [ "$1" = "cron" ]; then
  echo "Migrating backend..."
  cd icon_governance
  alembic upgrade head
  echo "Starting cron..."
  python worker/cron/$2.py
elif [ "$1" = "api" ]; then
  echo "Starting API..."
  python icon_governance/main_api.py
else
  echo "No args specified - exiting..."
fi
