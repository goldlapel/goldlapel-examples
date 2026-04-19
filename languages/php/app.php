<?php
// composer require goldlapel/goldlapel
require __DIR__ . '/vendor/autoload.php';

use Goldlapel\GoldLapel;

$gl = GoldLapel::start('postgres://gl:gl@localhost:5432/todos', [
    'port' => 7932,
]);

// Build a PDO against the proxy — pdoDsn() + pdoCredentials() handle the
// URL -> `pgsql:host=...` translation.
[$user, $pass] = $gl->pdoCredentials();
$pdo = new PDO($gl->pdoDsn(), $user, $pass);

$pdo->exec('CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)');
$pdo->prepare('INSERT INTO todos (title) VALUES (?)')->execute(['Try Gold Lapel']);
$pdo->prepare('INSERT INTO todos (title, done) VALUES (?, ?)')->execute(['Read the docs', true]);

foreach ($pdo->query('SELECT id, title, done FROM todos ORDER BY id', PDO::FETCH_ASSOC) as $row) {
    echo json_encode($row) . "\n";
}

// Wrapper methods also work directly on the GoldLapel instance.
$gl->docInsert('events', ['type' => 'demo.ran']);
echo 'events: ' . json_encode($gl->docFind('events', ['type' => 'demo.ran'])) . "\n";

$gl->stop();
