package main

import (
	"context"
	"fmt"
	"log"

	"github.com/goldlapel/goldlapel-go"
	"github.com/jackc/pgx/v5"
)

func main() {
	url, err := goldlapel.Start("postgres://gl:gl@localhost:5432/todos")
	if err != nil {
		log.Fatal(err)
	}
	defer goldlapel.Stop()

	ctx := context.Background()
	conn, err := pgx.Connect(ctx, url)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close(ctx)

	_, err = conn.Exec(ctx, "CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)")
	if err != nil {
		log.Fatal(err)
	}
	_, err = conn.Exec(ctx, "INSERT INTO todos (title) VALUES ($1)", "Try Gold Lapel")
	if err != nil {
		log.Fatal(err)
	}
	_, err = conn.Exec(ctx, "INSERT INTO todos (title, done) VALUES ($1, $2)", "Read the docs", true)
	if err != nil {
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
}
