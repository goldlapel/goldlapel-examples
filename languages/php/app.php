<?php
require __DIR__ . '/vendor/autoload.php';

use GoldLapel\GoldLapel;

$conn = GoldLapel::start('postgres://gl:gl@localhost:5432/todos');

$conn->exec('CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)');
$conn->prepare('INSERT INTO todos (title) VALUES (?)')->execute(['Try Gold Lapel']);
$conn->prepare('INSERT INTO todos (title, done) VALUES (?, ?)')->execute(['Read the docs', true]);

foreach ($conn->query('SELECT id, title, done FROM todos ORDER BY id', PDO::FETCH_ASSOC) as $row) {
    echo json_encode($row) . "\n";
}

GoldLapel::stop();
