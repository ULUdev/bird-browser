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
def getBookmarks(cursor):
    cursor.execute("select * from bookmarks")
    results = cursor.fetchall()
    dict = {}
    for res in results:
        dict[res[0]] = res[1]
    return dict
def getBookmark(cursor, name:str):
    cursor.execute(f"select * from bookmarks where name='{name}'")
    res = cursor.fetchall()
    if len(res) == 0:
        raise ValueError(f"name doesnt exist")
    else:
        res = res[0]
        dict = {}
        dict[res[0]] = res[1]
    return dict
def addBookmark(cursor, name:str, url:str):
    cursor.execute(f"insert into bookmarks values ('{name}', '{url}')")
def modifyBookmark(cursor, name:str, newname:str, newurl:str):
    cursor.execute(f"update bookmarks set name = '{newname}', url = '{newurl}' where name = '{name}'")
