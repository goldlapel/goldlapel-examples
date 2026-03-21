<?php
require __DIR__ . '/vendor/autoload.php';

use GoldLapel\GoldLapel;

$url = GoldLapel::start('postgres://gl:gl@localhost:5432/todos');

$parts = parse_url($url);
$dsn = sprintf('pgsql:host=%s;port=%d;dbname=%s', $parts['host'], $parts['port'], ltrim($parts['path'], '/'));
$pdo = new PDO($dsn, $parts['user'], $parts['pass']);

$pdo->exec('CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)');
$pdo->prepare('INSERT INTO todos (title) VALUES (?)')->execute(['Try Gold Lapel']);
$pdo->prepare('INSERT INTO todos (title, done) VALUES (?, ?)')->execute(['Read the docs', true]);

foreach ($pdo->query('SELECT id, title, done FROM todos ORDER BY id', PDO::FETCH_ASSOC) as $row) {
    echo json_encode($row) . "\n";
}

GoldLapel::stop();
