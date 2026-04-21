# goldlapel-examples

Runnable example apps for [Gold Lapel](https://goldlapel.com). Each example is a standalone app — `cd` into the directory and follow its own README.

Product site: https://goldlapel.com · Docs: https://goldlapel.com/docs

## Run

Every example has its own README with install + run steps. Pick one that matches your stack and follow it.

## Repo structure

- `platforms/` — standalone-binary installs (`docker/`, `linux/`, `macos/`, `windows/`)
- `languages/` — wrapper package usage (`python/`, `javascript/`, `ruby/`, `go/`, `java/`, `php/`, `dotnet/`)
- `orms/` — ORM integrations (`sqlalchemy/`, `prisma/`, `drizzle/`)
- `frameworks/` — framework integrations (`django/`, `rails/`, `laravel/`, `spring-boot/`)
- `features/` — standalone feature demos:
  - `data-structures/` — Redis-style counters, hashes, sorted sets, queues, pub/sub, geo
  - `search/` — full-text, fuzzy, phonetic, vector, percolator
  - `streams/` — append-only logs with consumer groups
  - `sql-optimizations/` — matviews, indexes, caching, N+1 detection
  - `infrastructure/` — pooling, read-replicas, failover
  - `operations/` — hot-reload, skip annotation, dashboard API

## Related docs

- Full feature docs: https://goldlapel.com/docs
- Per-language guides: https://goldlapel.com/docs/python, `/docs/javascript`, etc.

## License

MIT. See `LICENSE`.
