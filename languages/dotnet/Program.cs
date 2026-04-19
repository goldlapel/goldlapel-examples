// dotnet add package GoldLapel
using Goldlapel;
using Npgsql;

await using var gl = await GoldLapel.StartAsync(
    "postgres://gl:gl@localhost:5432/todos");

await using var conn = new NpgsqlConnection(gl.Url);
await conn.OpenAsync();

await new NpgsqlCommand(
    "CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)",
    conn).ExecuteNonQueryAsync();

var insert1 = new NpgsqlCommand("INSERT INTO todos (title) VALUES ($1)", conn);
insert1.Parameters.AddWithValue("Try Gold Lapel");
await insert1.ExecuteNonQueryAsync();

var insert2 = new NpgsqlCommand("INSERT INTO todos (title, done) VALUES ($1, $2)", conn);
insert2.Parameters.AddWithValue("Read the docs");
insert2.Parameters.AddWithValue(true);
await insert2.ExecuteNonQueryAsync();

await using var reader = await new NpgsqlCommand(
    "SELECT id, title, done FROM todos ORDER BY id", conn).ExecuteReaderAsync();
while (await reader.ReadAsync())
    Console.WriteLine($"{{id: {reader.GetInt32(0)}, title: {reader.GetString(1)}, done: {reader.GetBoolean(2)}}}");

// Wrapper methods also work directly on the GoldLapel instance.
await gl.DocInsertAsync("events", "{\"type\":\"demo.ran\"}");
var events = await gl.DocFindAsync("events", "{\"type\":\"demo.ran\"}");
Console.WriteLine($"events: {events}");

// `await using` auto-stops the proxy at scope end.
