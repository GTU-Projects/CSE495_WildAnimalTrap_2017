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

        query = initDBs.CEHCK_TRAP_CREDENTIALS.format(email,password)
        print(query)
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

        query = initDBs.INSERT_SERVED_TRAP_QUERY.format(serial,email,password)
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

        query = initDBs.CHECK_TRAP_SERIAL_QUERY.format(serial)

        qResult = cur.execute(query).fetchone() # save query result

        # if serial not found
        if qResult==None:
            retVal = Constants.ERROR_UNK_SERIAL

        else:
            # check email or serial used before
            query = initDBs.CHECK_SERVED_TRAP_SERIAL_QUERY.format(serial,email)
            qResult = cur.execute(query).fetchone()
            # TODO: extend used serial or email options
            if qResult!=None:
                retVal = Constants.ERROR_USED_SERIAL

    except Exception as e:
        print("CheckAccountException:",str(e))
        retVal= Constants.ERROR_UNKNOWN

    finally:
        if conn:
            conn.close()

    return retVal
