#!/bin/bash
# Generate traffic against the todo app so GL can observe query patterns.
# Run after starting Postgres, GL, and the app.

BASE="http://localhost:8000"

echo "=== Creating todos ==="
for i in $(seq 1 20); do
    curl -s -X POST "$BASE/todos?title=Todo+$i&description=Description+for+item+$i&priority=$((RANDOM % 5))" > /dev/null
done
echo "Created 20 todos"

echo ""
echo "=== Reading (generating patterns for GL) ==="
for i in $(seq 1 30); do
    curl -s "$BASE/todos" > /dev/null
    curl -s "$BASE/todos/pending" > /dev/null
    curl -s "$BASE/todos/completed" > /dev/null
    curl -s "$BASE/todos/stats" > /dev/null
    curl -s "$BASE/todos/$((RANDOM % 20 + 1))" > /dev/null
    curl -s "$BASE/todos/search?q=Todo" > /dev/null
done
echo "Sent 180 read requests (30 rounds x 6 endpoints)"

echo ""
echo "=== Completing some todos ==="
for i in 1 3 5 7 9 11 13 15; do
    curl -s -X PUT "$BASE/todos/$i?completed=true" > /dev/null
done
echo "Completed 8 todos"

echo ""
echo "=== More reads (post-write, GL should see invalidation) ==="
for i in $(seq 1 20); do
    curl -s "$BASE/todos" > /dev/null
    curl -s "$BASE/todos/pending" > /dev/null
    curl -s "$BASE/todos/completed" > /dev/null
    curl -s "$BASE/todos/stats" > /dev/null
done
echo "Sent 80 more read requests"

echo ""
echo "=== Done ==="
echo "Total: 20 writes + 260 reads"
echo ""
echo "Now check GL status:"
echo "  goldlapel status --upstream postgres://gl:gl@localhost:5432/todos"
echo ""
echo "Or open the dashboard:"
echo "  http://localhost:7933"
