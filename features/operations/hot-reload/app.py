import os
import time
import tempfile
import goldlapel

config_dir = tempfile.mkdtemp()
config_path = os.path.join(config_dir, "goldlapel.toml")

with open(config_path, "w") as f:
    f.write('mode = "waiter"\n\n[thresholds]\nmin_pattern_count = 10\n')

print(f"Config file: {config_path}")

gl = goldlapel.GoldLapel("postgres://gl:gl@localhost:5432/todos", config={
    "config": config_path,
})
conn = gl.start()

print("Started in waiter mode with min_pattern_count=10")
time.sleep(2)

with open(config_path, "w") as f:
    f.write('mode = "bellhop"\n\n[thresholds]\nmin_pattern_count = 3\n')

print("Config updated — GL will hot-reload within 30 seconds")
print("Watch GL logs for 'hot-reloaded: mode: bellhop' and 'hot-reloaded: min-pattern-count: 10 -> 3'")

print("Waiting 35 seconds for the poll cycle...")
time.sleep(35)

print("Done — check dashboard to confirm mode changed to bellhop")
print("Dashboard: http://localhost:7933")

conn.close()
gl.stop()
