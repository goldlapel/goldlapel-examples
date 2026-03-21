<?php

return [
    'default' => env('DB_CONNECTION', 'pgsql'),

    'connections' => [
        'pgsql' => [
            'driver' => 'pgsql',
            'host' => env('DB_HOST', 'localhost'),
            'port' => env('DB_PORT', '5432'),
            'database' => env('DB_DATABASE', 'todos'),
            'username' => env('DB_USERNAME', 'gl'),
            'password' => env('DB_PASSWORD', 'gl'),
            'charset' => 'utf8',
            'prefix' => '',
            'schema' => 'public',
        ],
    ],

    'migrations' => 'migrations',

    'goldlapel' => [
        'enabled' => true,
    ],
];
