using Npgsql;

var glUrl = GoldLapel.GoldLapel.Start("postgres://gl:gl@localhost:5432/todos");

var uri = new Uri(glUrl);
var userInfo = uri.UserInfo.Split(':');
var connStr = $"Host={uri.Host};Port={uri.Port};Database={uri.AbsolutePath.TrimStart('/')};Username={userInfo[0]};Password={userInfo[1]}";

await using var conn = new NpgsqlConnection(connStr);
await conn.OpenAsync();

await new NpgsqlCommand("CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)", conn).ExecuteNonQueryAsync();

var insert1 = new NpgsqlCommand("INSERT INTO todos (title) VALUES ($1)", conn);
insert1.Parameters.AddWithValue("Try Gold Lapel");
await insert1.ExecuteNonQueryAsync();

var insert2 = new NpgsqlCommand("INSERT INTO todos (title, done) VALUES ($1, $2)", conn);
insert2.Parameters.AddWithValue("Read the docs");
insert2.Parameters.AddWithValue(true);
await insert2.ExecuteNonQueryAsync();

await using var reader = await new NpgsqlCommand("SELECT id, title, done FROM todos ORDER BY id", conn).ExecuteReaderAsync();
while (await reader.ReadAsync())
    Console.WriteLine($"{{id: {reader.GetInt32(0)}, title: {reader.GetString(1)}, done: {reader.GetBoolean(2)}}}");

GoldLapel.GoldLapel.Stop();
