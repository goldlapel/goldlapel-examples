# Gold Lapel Examples

Example applications demonstrating [Gold Lapel](https://github.com/goldlapel/goldlapel), a self-optimizing Postgres proxy.

Each example is a standalone app that connects to Postgres through the GL proxy, generating query traffic so you can see GL observe and optimize real workloads.

## Available Examples

| Example | Stack | Description |
|---------|-------|-------------|
| [python/](python/) | FastAPI + psycopg | CRUD todo app with 6 read patterns and a traffic generator script |

## Getting Started

1. Install Gold Lapel ([releases](https://github.com/goldlapel/goldlapel/releases))
2. Pick an example and follow its README
3. Run the traffic generator to feed GL query patterns
4. Check the dashboard at http://localhost:7933 to see what GL found
