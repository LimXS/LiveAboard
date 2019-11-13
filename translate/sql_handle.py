#coding=utf-8
import pymysql

def sql_connect():
    db = pymysql.connect(host="182.92.130.30", port=3309,user="jkant",passwd="jkant520YE",db="liveaboard",cursorclass=pymysql.cursors.DictCursor )
    cursor = db.cursor()
    return cursor, db


def sql_search(sql):
    # db = pymysql.connect(host="182.92.130.30", port=3309,user="jkant",passwd="jkant520YE",db="liveaboard" )
    cursor = sql_connect()[0]
    cursor.execute(sql)
    results = cursor.fetchall()
    # redata = [a for a in results]
    cursor.close()
    # print(results)
    return results

def sql_excute(sql):
    cur = sql_connect()
    try:
        cur[0].execute(sql)
        cur[1].commit()
    except:
        cur[1].rollback()
    cur[1].close()




