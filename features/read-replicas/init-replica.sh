#!/bin/bash
set -e

until pg_isready -h primary -U gl; do
  echo "Waiting for primary..."
  sleep 1
done

# pg_isready returns success as soon as the server accepts connections, but
# the primary's init script may still be creating roles (e.g. the gl user).
# Give it a moment so pg_basebackup can authenticate.
sleep 2

pg_basebackup -h primary -U gl -D /var/lib/postgresql/data -Fp -Xs -R
exec postgres -c hot_standby=on
