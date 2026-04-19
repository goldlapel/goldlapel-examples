# Gold Lapel Examples

Example applications demonstrating [Gold Lapel](https://goldlapel.com), a self-optimizing Postgres proxy.

Each example is a standalone app you can clone and run. Follow the README in each directory to get started.

## Platforms

Install GL as a standalone binary or container.

| Example | Description |
|---------|-------------|
| [platforms/docker](platforms/docker/) | GL + Postgres as Docker containers |
| [platforms/linux](platforms/linux/) | CLI binary with a FastAPI todo app |
| [platforms/macos](platforms/macos/) | Homebrew install |
| [platforms/windows](platforms/windows/) | PowerShell install |

## Languages

Use the GL wrapper package for your language.

| Example | Install |
|---------|---------|
| [languages/python](languages/python/) | `pip install goldlapel` |
| [languages/javascript](languages/javascript/) | `npm install goldlapel` |
| [languages/ruby](languages/ruby/) | `gem install goldlapel` |
| [languages/go](languages/go/) | `go get github.com/goldlapel/goldlapel-go` |
| [languages/java](languages/java/) | `com.goldlapel:goldlapel` (Maven) |
| [languages/php](languages/php/) | `composer require goldlapel/goldlapel` |
| [languages/dotnet](languages/dotnet/) | `dotnet add package GoldLapel` |

## Frameworks

Zero-config framework plugins.

| Example | Integration |
|---------|-------------|
| [frameworks/django](frameworks/django/) | Swap `ENGINE` to `django_goldlapel` |
| [frameworks/rails](frameworks/rails/) | Add `gem "goldlapel"` |
| [frameworks/laravel](frameworks/laravel/) | Auto-discovered service provider |
| [frameworks/spring-boot](frameworks/spring-boot/) | Add the starter dependency |

## ORMs

ORM-level plugins that intercept the connection layer.

| Example | Integration |
|---------|-------------|
| [orms/sqlalchemy](orms/sqlalchemy/) | `from goldlapel.sqlalchemy import create_engine` |
| [orms/prisma](orms/prisma/) | `withGoldLapel()` wraps PrismaClient |
| [orms/drizzle](orms/drizzle/) | `drizzle()` from `@goldlapel/drizzle` |

## Features

### Data Structures, Search & Streams

| Example | What it shows |
|---------|---------------|
| [features/data-structures](features/data-structures/) | 21 Redis-style data structure methods — counters, hashes, sorted sets, queues, pub/sub, geospatial |
| [features/search](features/search/) | 13 Elasticsearch-parity search methods — full-text, fuzzy, phonetic, vector, autocomplete, aggregations, percolator, relevance tuning |
| [features/streams](features/streams/) | 5 stream methods — append-only logs with consumer groups, acknowledgment, and claim |

### SQL Optimizations

| Example | What it shows |
|---------|---------------|
| [features/sql-optimizations](features/sql-optimizations/) | All optimization strategies in one script — matviews, indexes, caching, N+1 detection, and more |

### Infrastructure

| Example | What it shows |
|---------|---------------|
| [features/infrastructure/connection-pooling](features/infrastructure/connection-pooling/) | Session vs transaction pool modes |
| [features/infrastructure/read-replicas](features/infrastructure/read-replicas/) | Automatic read routing with read-after-write protection |
| [features/infrastructure/failover](features/infrastructure/failover/) | Automatic failover from primary to standby |

### Operations

| Example | What it shows |
|---------|---------------|
| [features/operations/hot-reload](features/operations/hot-reload/) | Edit config at runtime without restart |
| [features/operations/skip-annotation](features/operations/skip-annotation/) | Opt out queries with `/* goldlapel:skip */` |
| [features/operations/dashboard-api](features/operations/dashboard-api/) | Programmatic access to stats, audit, and export APIs |
