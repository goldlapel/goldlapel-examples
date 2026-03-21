# Gold Lapel — Spring Boot

One-dependency Spring Boot integration — auto-configures HikariCP.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Build and run:
   ```bash
   mvn spring-boot:run
   ```

3. Try it:
   ```bash
   curl http://localhost:8080/todos
   ```

## What to look for

GL starts automatically when Spring Boot connects to the database. The only GL-specific change is the `goldlapel-spring-boot-starter` dependency in `pom.xml` — it auto-configures HikariCP. Everything else is standard Spring Boot. Check the dashboard at http://localhost:7933 to see what GL found.
