import random
import sqlite3 as sql
def encrypt(key:int, pwd:str):
    crlist = []
    for i in pwd:
        crlist.append(ord(i) * key)
    res = ""
    for i in crlist:
        res += str(i) + ";"
    res = res[0:-1]
    return res
def decrypt(key:int, pwd:str):
    crlist = pwd.split(";")
    reslist = []
    for i in crlist:
        reslist.append(int(int(i) / key))
    resstr = ""
    for i in reslist:
        resstr += chr(i)
    return resstr
def keygen():
    return random.randint(10000, 1000000)
