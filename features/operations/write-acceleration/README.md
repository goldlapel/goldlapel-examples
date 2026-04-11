# Write Acceleration

Gold Lapel includes several write optimizations that speed up INSERT, UPDATE, and DELETE operations transparently.

## Async Commit

Eliminates WAL fsync wait per write (~1-2ms savings). Commits are acknowledged immediately; WAL flushes asynchronously with a ~10ms durability window (matches MongoDB's default `w:1`).

```bash
goldlapel --enable-async-commit
# or
GOLDLAPEL_ENABLE_ASYNC_COMMIT=true
```

**Expected speedup**: 2-5x for single writes.

## COPY Bulk Insert

Multi-row `INSERT INTO table (data) VALUES ($1::jsonb), ($2::jsonb), ...` statements are automatically rewritten to PostgreSQL COPY protocol when the row count exceeds the threshold.

```bash
goldlapel --copy-threshold 50  # default: rewrite at 50+ rows
```

**Expected speedup**: 1.3-1.7x on indexed tables, near-parity with MongoDB on typical doc store tables.

## Parallel COPY

For massive bulk loads (10K+ rows), GL splits the data across multiple parallel COPY streams on separate connections.

```bash
goldlapel --parallel-copy-threshold 10000  # default
goldlapel --parallel-copy-streams 4         # default, increase for fast storage
```

**Expected speedup**: 3-4x for 50K+ row loads.

## Adaptive Threshold

The COPY threshold self-tunes from real traffic. GL measures the actual latency of INSERT vs COPY and adjusts the crossover point automatically. Cold start uses the configured `--copy-threshold` value.

## Unlogged Tables

For ephemeral data (TTL collections, capped collections, session stores), create the collection as UNLOGGED to skip WAL entirely:

```python
import goldlapel
gl = goldlapel.connect("localhost", 7932)
gl.doc_create_collection("sessions", unlogged=True)
# 3-5x write speedup — data lost on crash (acceptable for sessions)
```

## Benchmark Results (GL vs MongoDB)

| Operation | MongoDB | GL | Gap |
|-----------|--------:|---:|-----|
| insert_one | 600us | 648us | Near parity |
| update_one | 495us | 676us | 1.4x |
| delete_one | 1.15ms | 2.15ms | 1.9x |

All write optimizations compound — async commit + COPY + parse dedup together close the MongoDB write gap from 3-4x to 1.1-1.9x.
