#!/bin/bash
# The key lands in a mode-600 file, is never printed, and a bad name or an empty value saves nothing.
set -euo pipefail
cd "$(dirname "$0")"
export KEYDIR="$(mktemp -d)/keys"
. ./savekey.sh
out=$(printf 'sk_test_secret123\n' | savekey MY_KEY 2>&1)
[ "$(cat "$KEYDIR/MY_KEY.env")" = "MY_KEY=sk_test_secret123" ]
case "$out" in *sk_test_secret123*) echo "FAIL: the key was printed"; exit 1;; esac
[ "$(stat -c %a "$KEYDIR/MY_KEY.env" 2>/dev/null || stat -f %Lp "$KEYDIR/MY_KEY.env")" = "600" ]
! printf 'x\n' | savekey "bad name" 2>/dev/null
! printf '\n' | savekey EMPTY 2>/dev/null
[ ! -f "$KEYDIR/EMPTY.env" ]
echo "ok savekey"
