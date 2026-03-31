from goldlapel_sqlalchemy import create_engine, stop
from sqlalchemy import text

engine = create_engine("postgresql+psycopg://gl:gl@localhost:5432/todos")

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)"))
    conn.execute(text("INSERT INTO todos (title) VALUES (:t)"), {"t": "Try Gold Lapel"})
    conn.execute(text("INSERT INTO todos (title, done) VALUES (:t, :d)"), {"t": "Read the docs", "d": True})
    conn.commit()
    for row in conn.execute(text("SELECT id, title, done FROM todos ORDER BY id")):
        print(row)

engine.dispose()
stop()
