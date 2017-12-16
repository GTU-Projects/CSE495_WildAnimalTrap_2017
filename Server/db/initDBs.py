import sqlite3
import os

dbFilePath = os.path.dirname(os.path.abspath(__file__))
dbFilePath = dbFilePath+"/WildAnimalTrap.db"
print("DB_FILE PATH:",dbFilePath)

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

	cur.execute("""
		CREATE TABLE "Users" (
		`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
		`email`	TEXT NOT NULL UNIQUE,
		`password`	TEXT NOT NULL,
		`gsm`	TEXT DEFAULT '+'
		)
	""")

	# Create initialized/served trap table
	cur.execute("""
		CREATE TABLE `ServedTraps` (
		`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
		`serial`	INTEGER UNIQUE NOT NULL,
		`userID` INTEGER NOT NULL,
		`name` TEXT DEFAULT 'No Name',
		`location` TEXT DEFAULT 'No Location'
		)
	""")


	# Serve 1 trap for tests

	#cur.execute("""
	#	INSERT INTO ServedTraps(serial,email,password) VALUES(95,"hmen.56@gmail.com","Hasan5669")
	#""")
	conn.commit()

	conn.close()

if __name__=="__main__":
	initialize()