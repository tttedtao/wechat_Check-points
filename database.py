# -*- coding: utf-8 -*-

'''
author = @ttt
name = 数据库基础函数
'''


import sqlite3
from getdata import chen_ji

#创建基础数据库
# conn = sqlite3.connect('database.db')
# cursor = conn.cursor()
# create = "create table usertable (openid varchar(28) primary key,user varchar(20),password1 varchar(20),password2 varchar(20))"
# create1 = "create table scoretable (openid varchar(28) primary key,user varchar(20),scoretext text)"
# create2 = "create table classtable (openid varchar(28) primary key,user varchar(20),classtext text)"
# cursor.execute(create)
# cursor.execute(create1)
# cursor.execute(create2)
from data_get import getUserinfo, getok

#保存用户信息
def insertiUserinfo(openid,user,pw1,pw2):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    v = (openid,user,pw1,pw2)
    ins = "insert into usertable values(?,?,?,?);"
    cursor.execute(ins, v)
    cursor.close()
    conn.commit()
    conn.close()
    if cursor.rowcount ==1:
        return "加入数据成功"
    else:
        return "操作失败"
#保存成绩信息
def insertiUserscore(openid,user,score):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    v = (openid,user,score)
    ins = "insert into scoretable values(?,?,?);"
    cursor.execute(ins, v)
    cursor.close()
    conn.commit()
    conn.close()
    if cursor.rowcount ==1:
        return "加入数据成功"
    else:
        return "操作失败"
#保存课表信息
def insertiUserclass(openid,user,text):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    v = (openid,user,text)
    ins = "insert into classtable values(?,?,?);"
    cursor.execute(ins, v)
    cursor.close()
    conn.commit()
    conn.close()
    if cursor.rowcount ==1:
        return "加入数据成功"
    else:
        return "操作失败"
#同步更新数据库
def web2db(openid):
    info = getUserinfo(openid)
    ok = getok(openid)

    if info == None:
        return "你个傻逼，都没绑定账号，同步你个大头鬼啊"

    else:
        if ok !=None:
            return "已经添加过数据，请勿再次添加"
        else:

            try:
                user = info[1]
                pw1 = info[2]
                pw2 = info[3]
                result = chen_ji(user,pw1,pw2)
                score = result[0]
                kebiao = result[1]
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                v1 = (openid, user, score)
                v2 = (openid,user,kebiao)
                ins_score = "insert into scoretable values(?,?,?);"
                ins_class = "insert into classtable values(?,?,?);"
                cursor.execute(ins_score, v1)
                cursor.execute(ins_class,v2)
                cursor.close()
                conn.commit()
                conn.close()
                return "应该已经把数据加入数据库了吧，我也不确定"
            except BaseException as e:
                return str(e)

#更新课表
def updateclass(openid):
    info = getUserinfo(openid)
    ok = getok(openid)

    if info == None:
        return "你个傻逼，都没绑定账号，更新你个大头鬼啊"

    else:


        try:
            user = info[1]
            pw1 = info[2]
            pw2 = info[3]
            result = chen_ji(user, pw1, pw2)

            kebiao = result[1]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            v = (kebiao,openid,)
            up = "UPDATE classtable set classtext =?  WHERE openid=?"
            cursor.execute(up, v)
            cursor.close()
            conn.commit()
            conn.close()
            if cursor.rowcount == 1:
                return "更新数据成功"
            else:
                return "操作失败"
        except BaseException as e:
            return str(e)
#更新成绩
def updatescore(openid):
    info = getUserinfo(openid)
    ok = getok(openid)

    if info == None:
        return "你个傻逼，都没绑定账号，更新你个大头鬼啊"

    else:


        try:
            user = info[1]
            pw1 = info[2]
            pw2 = info[3]
            result = chen_ji(user, pw1, pw2)

            score = result[0]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            v = (score, openid,)
            up = "UPDATE scoretable set scoretext =?  WHERE openid=?"
            cursor.execute(up, v)
            cursor.close()
            conn.commit()
            conn.close()
            if cursor.rowcount == 1:
                    return "更新数据成功"
            else:
                    return "操作失败"
        except BaseException as e:
            return str(e)

    # if cursor.rowcount == 1:
    #     return "加入数据成功"
    # else:
    #     return "操作失败"




