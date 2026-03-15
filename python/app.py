import os
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI, HTTPException

DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://gl:gl@localhost:7932/todos")


def get_conn():
    return psycopg.connect(DATABASE_URL)


@asynccontextmanager
async def lifespan(app):
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                completed BOOLEAN DEFAULT FALSE,
                priority INTEGER DEFAULT 0,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        conn.commit()
    yield


app = FastAPI(title="Todo App (Gold Lapel Example)", lifespan=lifespan)


# --- Reads (these are the patterns GL will optimize) ---

@app.get("/todos")
def list_todos():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title, description, completed, priority, created_at FROM todos ORDER BY created_at DESC"
        ).fetchall()
    return [dict(zip(["id", "title", "description", "completed", "priority", "created_at"], r)) for r in rows]


@app.get("/todos/pending")
def list_pending():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title, description, completed, priority, created_at FROM todos WHERE completed = FALSE ORDER BY priority DESC, created_at DESC"
        ).fetchall()
    return [dict(zip(["id", "title", "description", "completed", "priority", "created_at"], r)) for r in rows]


@app.get("/todos/completed")
def list_completed():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title, description, completed, priority, created_at FROM todos WHERE completed = TRUE ORDER BY created_at DESC"
        ).fetchall()
    return [dict(zip(["id", "title", "description", "completed", "priority", "created_at"], r)) for r in rows]


@app.get("/todos/search")
def search_todos(q: str):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title, description, completed, priority, created_at FROM todos WHERE title ILIKE %s ORDER BY created_at DESC",
            (f"%{q}%",),
        ).fetchall()
    return [dict(zip(["id", "title", "description", "completed", "priority", "created_at"], r)) for r in rows]


@app.get("/todos/stats")
def todo_stats():
    with get_conn() as conn:
        row = conn.execute("""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE completed) AS done,
                COUNT(*) FILTER (WHERE NOT completed) AS pending,
                AVG(priority) AS avg_priority
            FROM todos
        """).fetchone()
    return {"total": row[0], "done": row[1], "pending": row[2], "avg_priority": float(row[3] or 0)}


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, title, description, completed, priority, created_at FROM todos WHERE id = %s",
            (todo_id,),
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Todo not found")
    return dict(zip(["id", "title", "description", "completed", "priority", "created_at"], row))


# --- Writes (pass through GL untouched) ---

@app.post("/todos", status_code=201)
def create_todo(title: str, description: str = "", priority: int = 0):
    with get_conn() as conn:
        row = conn.execute(
            "INSERT INTO todos (title, description, priority) VALUES (%s, %s, %s) RETURNING id",
            (title, description, priority),
        ).fetchone()
        conn.commit()
    return {"id": row[0]}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, title: str = None, description: str = None, completed: bool = None, priority: int = None):
    sets, vals = [], []
    if title is not None:
        sets.append("title = %s")
        vals.append(title)
    if description is not None:
        sets.append("description = %s")
        vals.append(description)
    if completed is not None:
        sets.append("completed = %s")
        vals.append(completed)
    if priority is not None:
        sets.append("priority = %s")
        vals.append(priority)
    if not sets:
        raise HTTPException(status_code=400, detail="Nothing to update")
    vals.append(todo_id)
    with get_conn() as conn:
        cur = conn.execute(f"UPDATE todos SET {', '.join(sets)} WHERE id = %s", vals)
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"ok": True}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"ok": True}
