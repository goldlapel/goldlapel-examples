# Gold Lapel — N+1 Query Detection

GL detects N+1 query patterns — the same query firing repeatedly in rapid succession — and warns you before they become a production problem.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the demo:
   ```bash
   python app.py
   ```

## What to look for

The classic N+1 problem: you fetch a list of IDs, then loop and query each one individually. This fires N separate queries when a single query would do.

The app first demonstrates the anti-pattern — fetching all customer IDs, then querying each customer one at a time in a tight loop. GL watches for this pattern: when the same parameterized query fires more than 5 times within a 2-second window, it flags it as an N+1.

Then the app shows the fix — a single `SELECT ... WHERE id IN (...)` that gets all the data in one round-trip.

Check GL logs for the `N+1 query pattern detected` warning, and visit the dashboard at http://localhost:7933 to see the flagged pattern.
