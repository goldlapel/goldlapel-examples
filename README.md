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
| [frameworks/rails](frameworks/rails/) | Add `gem "goldlapel-rails"` |
| [frameworks/laravel](frameworks/laravel/) | Auto-discovered service provider |
| [frameworks/spring-boot](frameworks/spring-boot/) | Add the starter dependency |

## ORMs

ORM-level plugins that intercept the connection layer.

| Example | Integration |
|---------|-------------|
| [orms/sqlalchemy](orms/sqlalchemy/) | `from goldlapel_sqlalchemy import create_engine` |
| [orms/prisma](orms/prisma/) | `withGoldLapel()` wraps PrismaClient |
| [orms/drizzle](orms/drizzle/) | `drizzle()` from `goldlapel-drizzle` |

## Features

Infrastructure demos for GL's advanced features.

| Example | What it shows |
|---------|---------------|
| [features/connection-pooling](features/connection-pooling/) | Session vs transaction pool modes |
| [features/read-replicas](features/read-replicas/) | Automatic read routing with read-after-write protection |
| [features/failover](features/failover/) | Automatic failover from primary to standby |
| [features/n1-detection](features/n1-detection/) | Detect N+1 query anti-patterns |
| [features/matviews](features/matviews/) | Automatic materialized view creation |
| [features/hot-reload](features/hot-reload/) | Edit config at runtime without restart |
| [features/skip-annotation](features/skip-annotation/) | Opt out queries with `/* goldlapel:skip */` |
| [features/dashboard-api](features/dashboard-api/) | Programmatic access to stats, audit, and export APIs |
