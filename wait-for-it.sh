#!/usr/bin/env bash
# Use this script to test if a given TCP host/port are available
# Source: https://github.com/vishnubob/wait-for-it

HOST="$1"
PORT="$2"
shift 2

TIMEOUT=30

echo "Waiting for $HOST:$PORT..."

for ((i=0;i<${TIMEOUT};i++)); do
  nc -z "$HOST" "$PORT" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "$HOST:$PORT is available!"
    exec "$@"
    exit 0
  fi
  sleep 1
done

echo "Timeout waiting for $HOST:$PORT"
exit 1
