# Tor multi-instance config

Run multiple Tor instances in parallel, each with its own SOCKS proxy and IP address. Useful when scraping at scale — if a target site has low request limits per IP, you can spread traffic across many Tor circuits to avoid rate limiting.

Each instance gets its own SOCKS port, control port, and data directory. The `rotate-tor.sh` script continuously requests new circuits so your IPs keep changing.

## Setup

1. Edit `shared.sh` to set your password and number of instances
2. Generate the hashed password: `./generate-hash.sh`
3. Generate torrc files: `./tor-config.sh`
4. Start all instances: `./run-tor.sh`
5. Rotate IPs continuously: `./rotate-tor.sh`
