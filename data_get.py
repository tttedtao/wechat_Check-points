# -*- coding: utf-8 -*-
'''
@author:ttt
@name:获取数据可数据函数集合
'''


import sqlite3



#获取用户信息
def getUserinfo(openid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    seclet = "SELECT * FROM usertable WHERE openid=?"

    cursor.execute(seclet, (openid,))
    values = cursor.fetchone()
    cursor.close()
    conn.commit()
    conn.close()
    return values
#获取用户成绩
def getscore(openid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    seclet = "SELECT * FROM scoretable WHERE openid=?"

    cursor.execute(seclet, (openid,))
    values = cursor.fetchone()
    cursor.close()
    conn.commit()
    conn.close()
    if values:
        return str(values[2])
    else:
        return "没有你的数据，请绑定教务处！"







#获取用户课表
def gettable(openid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    seclet = "SELECT * FROM classtable WHERE openid=?"

    cursor.execute(seclet, (openid,))
    values = cursor.fetchone()
    cursor.close()
    conn.commit()
    conn.close()
    if values:
        return str(values[2])
    else:
        return "没有你的数据，请绑定教务处！"
#确认用户是否存在
def getok(openid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    seclet = "SELECT * FROM classtable WHERE openid=?"

    cursor.execute(seclet, (openid,))
    values = cursor.fetchone()
    cursor.close()
    conn.commit()
    conn.close()
    return values

