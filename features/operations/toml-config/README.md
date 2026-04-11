# TOML Configuration

Gold Lapel supports a hierarchical TOML config file as an alternative to CLI flags and environment variables. Place a `goldlapel.toml` in your working directory or specify with `--config path/to/config.toml`.

## Example Config

See `goldlapel.toml` in this directory for a fully annotated example covering all configuration sections.

## Precedence

1. CLI flags (highest)
2. Environment variables
3. TOML config file
4. Built-in defaults (lowest)

## Live Reload

Most settings are hot-reloaded when the config file changes — no restart needed. GL watches the file and applies changes automatically.

## Usage

```bash
# Start GL with this config
goldlapel --config goldlapel.toml --upstream postgres://localhost:5432/mydb

# Or place goldlapel.toml in the working directory (auto-detected)
goldlapel --upstream postgres://localhost:5432/mydb
```
