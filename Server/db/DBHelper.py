import sqlite3
import initDBs
import Constants

import sys

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

        query = initDBs.CHECK_USER_CREDENTIALS.format(email,password)
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
        curr = conn.cursor()

        # first create user
        query = initDBs.INSERT_USERS_QUERY.format(email,password)
        print("CreateAccount:",query)
        curr.execute(query)

        # get created user index-id
        query = initDBs.GET_USERID_QUERY.format(email)
        print("CreateAccount:",query)
        userId = curr.execute(query).fetchone()[0]
                
        if not userId:
            raise Exception

        # serve trap for created user
        query = initDBs.INSERT_SERVED_TRAP_QUERY.format(serial,userId)
        print("CreateAccount:",query)
        curr.execute(query)
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

def checkAccount(serial,email):
    """ Check if serial is valid and any one
        registered before with same email or serial number
    """
    conn = None
    retVal =  Constants.SUCCESS

    try:
        conn  = openConnection()
        cur = conn.cursor()

        # check AllTraps table to check if serial valid
        query = initDBs.CHECK_TRAP_SERIAL_QUERY.format(serial)

        qResult = cur.execute(query).fetchone() # save query result

        # if serial not found
        if qResult==None:
            retVal = Constants.ERROR_UNK_SERIAL

        else:
            # check if serial used before
            query = initDBs.CHECK_SERVED_TRAP_SERIAL_QUERY.format(serial)
            qResult = cur.execute(query).fetchone()

            # TODO: check email used before
            if qResult!=None:
                retVal = Constants.ERROR_USED_SERIAL

    except Exception as e:
        print("CheckAccountException:",str(e))
        retVal= Constants.ERROR_UNKNOWN

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

        query = initDBs.GET_USERID_QUERY.format(email)
        print("getTraps:",query)
        userId = cur.execute(query).fetchone()[0]

        query = initDBs.CHECK_USER_TRAPS_QUERY.format(userId)
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