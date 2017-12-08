import sqlite3
import os

dbFilePath = os.path.dirname(os.path.abspath(__file__))
dbFilePath = dbFilePath+"/WildAnimalTrap.db"
print("DB_FILE PATH:",dbFilePath)

CHECK_TRAP_SERIAL_QUERY = "SELECT id FROM AllTraps WHERE serial={}"
CHECK_SERVED_TRAP_SERIAL_QUERY = """SELECT * FROM ServedTraps WHERE serial={} OR email="{}" """
CEHCK_TRAP_CREDENTIALS = """SELECT * FROM ServedTraps WHERE email="{}" AND password="{}" """
INSERT_SERVED_TRAP_QUERY=""" INSERT INTO ServedTraps(serial,email,password) VALUES({},"{}","{}")"""


def initialize():
	# remote old db file
	if os.path.exists(dbFilePath):
		os.unlink(dbFilePath)

	conn = sqlite3.connect(dbFilePath)

	cur = conn.cursor()

	# Create All Trap table
	cur.execute("""
		CREATE TABLE `AllTraps` (
		`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
		`serial`	INTEGER UNIQUE
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
		`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
		`serial`	INTEGER UNIQUE NOT NULL,
		`email`	TEXT NOT NULL,
		`password`	TEXT NOT NULL,
		`location`	TEXT,
		`gsm`	TEXT
	)
	""")

	conn.close()

if __name__=="__main__":
	initialize()