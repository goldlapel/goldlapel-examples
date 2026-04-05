import goldlapel

UPSTREAM = "postgres://gl:gl@localhost:5432/todos"

conn = goldlapel.start(UPSTREAM)


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# --- Schema setup ---

conn.execute("DROP TABLE IF EXISTS articles CASCADE")
conn.execute("""
    CREATE TABLE articles (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        author TEXT NOT NULL
    )
""")

articles = [
    ("PostgreSQL Performance Tuning", "Query optimization is essential for database performance. Indexing strategies, connection pooling, and materialized views can dramatically reduce response times.", "Alice Chen"),
    ("Getting Started with Django", "Django is a high-level Python web framework that encourages rapid development. It includes an ORM, template engine, and admin interface out of the box.", "Bob Smith"),
    ("Understanding Database Indexes", "B-tree indexes are the most common type in PostgreSQL. They work well for equality and range queries on columns that are frequently filtered.", "Carol Johnson"),
    ("Building APIs with FastAPI", "FastAPI is a modern Python framework for building APIs. It uses type hints for validation and generates OpenAPI documentation automatically.", "David Lee"),
    ("PostgreSQL Full-Text Search", "PostgreSQL includes powerful full-text search capabilities. The tsvector type stores preprocessed documents, and tsquery represents search queries with boolean operators.", "Alice Chen"),
    ("React State Management", "Managing state in React applications can be done with useState, useReducer, Context API, or external libraries like Redux and Zustand.", "Eve Williams"),
    ("Caching Strategies for Web Apps", "Effective caching reduces database load and improves response times. Consider in-memory caches, CDN caching, and query result caching for optimal performance.", "Frank Brown"),
    ("Machine Learning with Python", "Python dominates machine learning with libraries like scikit-learn, TensorFlow, and PyTorch. Data preprocessing with pandas and numpy is a critical first step.", "Grace Kim"),
    ("PostgreSQL Connection Pooling", "Connection pooling reuses database connections across requests, preventing the overhead of establishing new connections for each query. PgBouncer is a popular choice.", "Bob Smith"),
    ("Kubernetes Deployment Patterns", "Kubernetes orchestrates containerized applications. Common patterns include blue-green deployments, canary releases, and rolling updates for zero-downtime deployments.", "Henry Davis"),
]

for title, body, author in articles:
    conn.execute(
        "INSERT INTO articles (title, body, author) VALUES (%s, %s, %s)",
        (title, body, author),
    )
conn.commit()
print("Created articles table with 10 rows.\n")


# ─────────────────────────────────────────────────────────────
# 1. FULL-TEXT SEARCH
# ─────────────────────────────────────────────────────────────
section("1. Full-Text Search — search()")

results = goldlapel.search(conn, "articles", "body", "database performance")
print(f"  search('articles', 'body', 'database performance') → {len(results)} results:")
for r in results:
    print(f"    [{r['_score']:.4f}] {r['title']}")

print()
results = goldlapel.search(conn, "articles", ["title", "body"], "PostgreSQL", highlight=True)
print(f"  multi-column search with highlights → {len(results)} results:")
for r in results:
    highlight = r.get("_highlight", "")[:80]
    print(f"    [{r['_score']:.4f}] {r['title']}")
    if highlight:
        print(f"             {highlight}...")


# ─────────────────────────────────────────────────────────────
# 2. FUZZY SEARCH
# ─────────────────────────────────────────────────────────────
section("2. Fuzzy Search — search_fuzzy()")

results = goldlapel.search_fuzzy(conn, "articles", "author", "Alic", threshold=0.2)
print(f"  search_fuzzy('articles', 'author', 'Alic') → {len(results)} results:")
for r in results:
    print(f"    [{r['_score']:.2f}] {r['author']} — {r['title']}")


# ─────────────────────────────────────────────────────────────
# 3. PHONETIC SEARCH
# ─────────────────────────────────────────────────────────────
section("3. Phonetic Search — search_phonetic()")

results = goldlapel.search_phonetic(conn, "articles", "author", "Smyth")
print(f"  search_phonetic('articles', 'author', 'Smyth') → {len(results)} results:")
for r in results:
    print(f"    [{r['_score']:.2f}] {r['author']} — {r['title']}")
print("  'Smyth' matches 'Smith' via soundex phonetic matching.")


# ─────────────────────────────────────────────────────────────
# 4. AUTOCOMPLETE
# ─────────────────────────────────────────────────────────────
section("4. Autocomplete — suggest()")

results = goldlapel.suggest(conn, "articles", "title", "Post")
print(f"  suggest('articles', 'title', 'Post') → {len(results)} results:")
for r in results:
    print(f"    [{r['_score']:.2f}] {r['title']}")


# ─────────────────────────────────────────────────────────────
# 5. VECTOR SIMILARITY (semantic search)
# ─────────────────────────────────────────────────────────────
section("5. Vector Similarity — similar()")

print("  Vector search requires embeddings from an AI model (OpenAI, Cohere, etc.).")
print("  Gold Lapel indexes the vectors — your application generates them.\n")
print("  Example (pseudo-code):")
print("    embedding = openai.embed('database optimization')")
print("    results = goldlapel.similar(conn, 'articles', 'embedding', embedding)")
print("\n  Skipping live demo — requires a vector column with real embeddings.")
print("  See docs/extensions for pgvector setup instructions.")


# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────
section("Summary")
print("  5 search methods demonstrated:")
print("    search()          — full-text search with ranking and highlighting")
print("    search_fuzzy()    — typo-tolerant matching ('Alic' → 'Alice')")
print("    search_phonetic() — sound-alike matching ('Smyth' → 'Smith')")
print("    suggest()         — autocomplete/typeahead ('Post' → 'PostgreSQL...')")
print("    similar()         — vector similarity (requires embeddings)")
print("\n  No Elasticsearch. No Solr. No sync pipeline.")
print("  Just PostgreSQL.")

conn.close()
goldlapel.stop()
