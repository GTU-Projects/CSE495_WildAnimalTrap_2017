import sqlite3
import os

dbFilePath = os.path.dirname(os.path.abspath(__file__))
dbFilePath = dbFilePath+"/WildAnimalTrap.db"
print("DB_FILE PATH:",dbFilePath)

CHECK_TRAP_SERIAL_QUERY = """SELECT id FROM AllTraps WHERE serial={}"""
CHECK_SERVED_TRAP_SERIAL_QUERY = """SELECT * FROM ServedTraps WHERE serial={}"""
CHECK_USER_TRAPS_QUERY = """SELECT * FROM ServedTraps WHERE userId={}"""
CHECK_USER_CREDENTIALS = """SELECT * FROM Users WHERE email="{}" AND password="{}" """
INSERT_USERS_QUERY = """INSERT INTO Users(email,password) VALUES("{}","{}")"""
INSERT_SERVED_TRAP_QUERY = """INSERT INTO ServedTraps(serial,userId) VALUES({},{})"""
CHECK_SERVED_TRAPS = """SELECT * FROM ServedTraps WHERE email="{}" """
GET_USERID_QUERY = """SELECT id FROM Users WHERE email="{}" """

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