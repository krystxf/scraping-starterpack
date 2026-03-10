#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
source "$DIR/shared.sh"

mkdir -p ./tor/data ./tor/config

for ((i=0; i<NUM_INSTANCES; i++)); do
  socks_port=$((BASE_SOCKS_PORT + i * 10))
  control_port=$((BASE_CONTROL_PORT + i * 10))
  data_dir="tor/data/tor$i"

  mkdir -p "$data_dir"

  cat > "tor/config/torrc.$i" <<EOF
SocksPort $socks_port
ControlPort $control_port
HashedControlPassword $HASHED_PASSWORD
DataDirectory $data_dir
EOF
done
