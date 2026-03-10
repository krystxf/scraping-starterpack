#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
source "$DIR/shared.sh"

HASH=$(tor --hash-password "$PASSWORD")
echo "HASHED_PASSWORD=\"$HASH\"" > "$DIR/hashedpassword.sh"
echo "Done: $HASH"
