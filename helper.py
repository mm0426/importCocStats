import time
import datetime
from cocapi import CocApi
import mysql.connector
import env

def mysqlConnect():

    return mysql.connector.connect(
      host=env.mysqlhost,
      user=env.mysqluser,
      password=env.mysqlpassword,
      database=env.mysqldatabase,
      auth_plugin='mysql_native_password'
    )


def getclaninfo():

    apiCall = CocApi(env.cocApiAuthToken, env.cocApiTimeout)
    claninfo = apiCall.clan_tag('#80j0jrlp')
    return claninfo


def importClanMemberList():

    mydb = mysqlConnect()
    claninfo = getclaninfo()
    ts = time.time()
    currentTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    for member in claninfo['memberList']:

        mycursor = mydb.cursor()
        sql = "INSERT INTO memberrawimport (name, tag, role, expLevel, clanRank, previousClanRank, " \
              "donations, donationsReceived, trophies, versusTrophies, timestamp) VALUES (%s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s)"
        val = (member['name'], member['tag'], member['role'], member['expLevel'], member['clanRank'],
               member['previousClanRank'], member['donations'], member['donationsReceived'], member['trophies'],
               member['versusTrophies'], currentTime)

        mycursor.execute(sql, val)

        mydb.commit()