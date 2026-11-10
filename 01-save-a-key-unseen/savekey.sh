# savekey: put an API key in a locked file without it ever appearing on screen, in chat or in shell history.
# Works in bash and zsh. Source this file, then:   savekey STRIPE_API_KEY
# Copy the file to a server unopened:              savekey_send STRIPE_API_KEY user@server /etc/myapp/
KEYDIR="${KEYDIR:-$HOME/.keys}"

savekey() {
  local name="$1" value
  case "$name" in ''|*[!A-Z0-9_]*) echo "usage: savekey NAME (capitals, digits, underscores)" >&2; return 2;; esac
  mkdir -p "$KEYDIR" && chmod 700 "$KEYDIR"
  printf '%s: ' "$name" >&2
  IFS= read -rs value; echo >&2                      # -s: nothing echoes; the value never reaches history
  [ -n "$value" ] || { echo "nothing saved" >&2; return 1; }
  ( umask 077; printf '%s=%s\n' "$name" "$value" > "$KEYDIR/$name.env" )
  value=""
  echo "saved $KEYDIR/$name.env ($(wc -c < "$KEYDIR/$name.env" | tr -d ' ') bytes, mode 600)" >&2
}

savekey_send() {
  local name="$1" dest="$2" dir="${3:-}"
  [ -f "$KEYDIR/$name.env" ] || { echo "no $KEYDIR/$name.env" >&2; return 1; }
  scp -q "$KEYDIR/$name.env" "$dest:$dir" && echo "copied $name.env to $dest:$dir unopened" >&2
}
