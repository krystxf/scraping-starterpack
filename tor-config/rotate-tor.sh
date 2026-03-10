#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
source "$DIR/shared.sh"

while true; do
  for ((i=0; i<NUM_INSTANCES; i++)); do
    PORT=$((BASE_CONTROL_PORT + i * 10))

    echo -e "AUTHENTICATE \"$PASSWORD\"\nSIGNAL NEWNYM\nQUIT" \
      | nc 127.0.0.1 "$PORT"

    echo "Rotated identity on control port $PORT at $(date)"
  done

  sleep 2
done
