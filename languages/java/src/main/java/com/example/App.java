package com.example;

import com.goldlapel.GoldLapel;
import java.sql.*;

public class App {
    public static void main(String[] args) throws Exception {
        try (Connection conn = GoldLapel.start("postgres://gl:gl@localhost:5432/todos")) {
            conn.createStatement().execute(
                "CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)");

            try (PreparedStatement ps = conn.prepareStatement("INSERT INTO todos (title) VALUES (?)")) {
                ps.setString(1, "Try Gold Lapel");
                ps.execute();
            }
            try (PreparedStatement ps = conn.prepareStatement("INSERT INTO todos (title, done) VALUES (?, ?)")) {
                ps.setString(1, "Read the docs");
                ps.setBoolean(2, true);
                ps.execute();
            }

            ResultSet rs = conn.createStatement().executeQuery("SELECT id, title, done FROM todos ORDER BY id");
            while (rs.next()) {
                System.out.printf("{id: %d, title: %s, done: %s}%n",
                    rs.getInt("id"), rs.getString("title"), rs.getBoolean("done"));
            }
        } finally {
            GoldLapel.stop();
        }
    }
}
