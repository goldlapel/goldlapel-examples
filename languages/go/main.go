// go get github.com/goldlapel/goldlapel-go github.com/jackc/pgx/v5
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/goldlapel/goldlapel-go"
	"github.com/jackc/pgx/v5"
)

func main() {
	ctx := context.Background()

	gl, err := goldlapel.Start(ctx, "postgres://gl:gl@localhost:5432/todos")
	if err != nil {
		log.Fatal(err)
	}
	defer gl.Close()

	conn, err := pgx.Connect(ctx, gl.URL())
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close(ctx)

	_, err = conn.Exec(ctx, "CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)")
	if err != nil {
		log.Fatal(err)
	}
	if _, err := conn.Exec(ctx, "INSERT INTO todos (title) VALUES ($1)", "Try Gold Lapel"); err != nil {
		log.Fatal(err)
	}
	if _, err := conn.Exec(ctx, "INSERT INTO todos (title, done) VALUES ($1, $2)", "Read the docs", true); err != nil {
		log.Fatal(err)
	}

	rows, err := conn.Query(ctx, "SELECT id, title, done FROM todos ORDER BY id")
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()
	for rows.Next() {
		var id int
		var title string
		var done bool
		if err := rows.Scan(&id, &title, &done); err != nil {
			log.Fatal(err)
		}
		fmt.Printf("{id: %d, title: %s, done: %v}\n", id, title, done)
	}

	// Wrapper methods also work directly on the GoldLapel instance.
	if _, err := gl.DocInsert(ctx, "events", map[string]any{"type": "demo.ran"}); err != nil {
		log.Fatal(err)
	}
	hits, err := gl.DocFind(ctx, "events", map[string]any{"type": "demo.ran"})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("events: %v\n", hits)
}
