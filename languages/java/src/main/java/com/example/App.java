package com.example;

import com.goldlapel.GoldLapel;
import java.sql.*;
import java.util.Properties;

public class App {
    public static void main(String[] args) throws Exception {
        try (GoldLapel gl = GoldLapel.start("postgres://gl:gl@localhost:5432/todos", opts -> {
            opts.setPort(7932);
        })) {
            // The JDBC driver rejects inline userinfo — use the JDBC URL plus
            // the parsed user/password properties.
            Properties props = new Properties();
            if (gl.getJdbcUser() != null) props.setProperty("user", gl.getJdbcUser());
            if (gl.getJdbcPassword() != null) props.setProperty("password", gl.getJdbcPassword());

            try (Connection conn = DriverManager.getConnection(gl.getJdbcUrl(), props)) {
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
            }

            // Wrapper methods also work directly on the GoldLapel instance.
            gl.docInsert("events", "{\"type\":\"demo.ran\"}");
            System.out.println("events: " + gl.docFind("events", "{\"type\":\"demo.ran\"}"));
        }
        // try-with-resources auto-stops the proxy
    }
}
