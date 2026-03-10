#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
source "$DIR/shared.sh"

for ((i=0; i<NUM_INSTANCES; i++)); do
  tor -f ./tor/config/torrc.$i &
done
