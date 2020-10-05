import sqlite3 as sql

def setupDatabase(cursor):
    try:
        cursor.execute("create table bookmarks (name, url)")
    except:
        raise ValueError("Database Setup already satisfied")
def getBookmarkNames(cursor):
    cursor.execute("select name from bookmarks")
    results = cursor.fetchall()
    list = []
    for res in results:
        list.append(res[0])
    return list
def getBookmarkUrls(cursor):
    cursor.execute("select url from bookmarks")
    results = cursor.fetchall()
    list = []
    for res in results:
        list.append(res[0])
    return list
