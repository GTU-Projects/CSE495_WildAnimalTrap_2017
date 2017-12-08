import sqlite3
import os


dbFileName = "WildAnimalTrap.db"

# remote old db file
if os.path.exists(dbFileName):
    os.unlink(dbFileName)

conn = sqlite3.connect("WildAnimalTrap.db")

cur = conn.cursor()

# Create All Trap table
cur.execute("""
    CREATE TABLE `AllTraps` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`serial`	INTEGER
)
""")

# Add some initial traps to table
cur.execute("""
    INSERT INTO AllTraps(serial) VALUES(95)
""")
conn.commit()



# Create initialized/served trap table
cur.execute("""
    CREATE TABLE `ServedTraps` (
	`id`	INTEGER,
	`serial`	INTEGER NOT NULL,
	`email`	TEXT NOT NULL,
	`password`	TEXT NOT NULL,
	`location`	TEXT NOT NULL,
	`gsm`	TEXT NOT NULL,
	PRIMARY KEY(id,serial)
)
""")


















conn.close()