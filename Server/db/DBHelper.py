import sqlite3
import initDBs
import Constants

import sys

CHECK_TRAP_SERIAL_QUERY = """SELECT id FROM AllTraps WHERE serial={}"""
CHECK_SERVED_TRAP_SERIAL_QUERY = """SELECT * FROM ServedTraps WHERE serial={}"""
CHECK_USER_TRAPS_QUERY = """SELECT * FROM ServedTraps WHERE userId={}"""
CHECK_USER_CREDENTIALS_QUERY = """SELECT * FROM Users WHERE email="{}" AND password="{}" """
INSERT_USERS_QUERY = """INSERT INTO Users(email,password) VALUES("{}","{}")"""
INSERT_SERVED_TRAP_QUERY = """INSERT INTO ServedTraps(serial,userId) VALUES({},{})"""
INSERT_SERVED_TRAP2_QUERY= """INSERT INTO ServedTraps(serial,userId,name,location) VALUES({},{},"{}","{}") """
CHECK_SERVED_TRAPS = """SELECT * FROM ServedTraps WHERE email="{}" """
GET_USERID_QUERY = """SELECT id FROM Users WHERE email="{}" """
GET_TRAP_DETAIL_QUERY ="""SELECT userID, name, location FROM ServedTraps WHERE serial={} """

def openConnection():
    try:
        print("SQLite DB File Path:",initDBs.dbFilePath)
        return sqlite3.connect(initDBs.dbFilePath)
    except Exception as e:
        print("ExceptionDBHelper:"+str(e))
        return None

def checkCredential(email,password):
    conn = None
    retVal = Constants.SUCCESS

    try:
        conn = openConnection()
        curr = conn.cursor()

        query = CHECK_USER_CREDENTIALS_QUERY.format(email,password)
        print("CheckCredential:",query)
        qResult = curr.execute(query).fetchone()
        if qResult==None:
            retVal = Constants.ERROR_WRONG_EMAIL_PASS

    except Exception as e:
        print("CheckCredential:"+str(e))
        retVal = Constants.ERROR_UNKNOWN

    finally:
        if conn:
            conn.close()

    return retVal

def createAccount(serial,email,password):
    """ Create new Trap account
    """
    conn = None
    retVal = Constants.SUCCESS

    try:
        conn = openConnection()
        cur = conn.cursor()

        retVal = checkAccount(cur,serial,email)
        # if serial used or not know, warn user
        if retVal!=Constants.SUCCESS:
            return retVal

        # first create user
        query = INSERT_USERS_QUERY.format(email,password)
        print("CreateAccount:",query)
        cur.execute(query)

        # get created user index-id
        query = GET_USERID_QUERY.format(email)
        print("CreateAccount:",query)
        userId = cur.execute(query).fetchone()[0]
                
        if not userId:
            raise Exception

        # serve trap for created user
        query = INSERT_SERVED_TRAP_QUERY.format(serial,userId)
        print("CreateAccount:",query)
        cur.execute(query)
        conn.commit()

    except Exception as e:
        print("CreateAccountException:"+str(e))
        # rollback/remove changes
        conn.rollback()
        retVal = Constants.ERROR_UNKNOWN
    finally:
        if conn:
            conn.close()

    return retVal

def checkAccount(cur,serial,email):
    """ Check if serial is valid and any one
        registered before with same email or serial number
    """
    retVal =  Constants.SUCCESS

    try:
        # check AllTraps table to check if serial valid
        query = CHECK_TRAP_SERIAL_QUERY.format(serial)
        qResult = cur.execute(query).fetchone() # save query result
       
        # if serial not found
        if qResult==None:
            retVal = Constants.ERROR_UNK_SERIAL

        else:
            # check if serial used before
            query = CHECK_SERVED_TRAP_SERIAL_QUERY.format(serial)
            qResult = cur.execute(query).fetchone()

            # TODO: check email used before
            if qResult!=None:
                retVal = Constants.ERROR_USED_SERIAL

    except Exception as e:
        print("CheckAccountException:",str(e))
        retVal= Constants.ERROR_UNKNOWN
    return retVal

def addNewTrap(email,serial,name,location):

    conn = None
    retVal = Constants.SUCCESS
    try:
        conn = openConnection()
        cur = conn.cursor()
        
        retVal = checkAccount(cur,serial,email)
        if retVal == Constants.SUCCESS:
            # get created user index-id
            query = GET_USERID_QUERY.format(email)
            print("CreateAccount:",query)
            userId = cur.execute(query).fetchone()[0]
                    
            if not userId:
                raise Exception

            # serve trap for created user
            query = INSERT_SERVED_TRAP2_QUERY.format(serial,userId,name,location)
            print("InsertServedTrap2Query:",query)
            cur.execute(query)
            conn.commit()

    except Exception as e:
        print("DBHelper: addNewTrap: exception:",str(e))
        retVal = Constants.ERROR_UNKNOWN
        conn.rollback() # remove last changes
    finally:
        if conn:
            conn.close()
    return retVal

def getTraps(email):
    """ Check if serial is valid and any one
        registered before with same email or serial number
    """
    conn = None
    retVal =  Constants.SUCCESS

    try:
        conn  = openConnection()
        cur = conn.cursor()

        query = GET_USERID_QUERY.format(email)
        print("getTraps:",query)
        userId = cur.execute(query).fetchone()[0]

        query = CHECK_USER_TRAPS_QUERY.format(userId)
        print("getTraps:",query)

        qResult = cur.execute(query).fetchall() # save query result

        retVal = []
        for trap in qResult:
            retVal.append({"serial":trap[1],
                        "userId":trap[2],
                        "name":trap[3],
                        "location":trap[4]})

        # if serial not found
        if qResult==None:
            retVal = Constants.ERROR_UNK_SERIAL

    except Exception as e:
        print("CheckTraps:",str(e))
        retVal= Constants.ERROR_UNKNOWN

    finally:
        if conn:
            conn.close()

    return retVal


def getTrapDetails(serial):
    conn = None
    trap = None
    try:
        conn  = openConnection()
        cur = conn.cursor()

        query = GET_TRAP_DETAIL_QUERY.format(serial)
        print("DBHelper: getTrapDetails: query:",query)
        qResult = cur.execute(query).fetchone() # save query result
   
        # if serial not found
        if qResult!=None:
            trap = Constants.Trap(serial,userId=qResult[0],name=qResult[1],location=qResult[2])

    except Exception as e:
        print("CheckTraps:",str(e))
        trap = None

    finally:
        if conn:
            conn.close()

    return trap