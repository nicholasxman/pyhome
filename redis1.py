#! /usr/bin/python3
import pymysql

# 在mysql表中添加数据
con = pymysql.connect(host='localhost', user='root', password='123456', port=3306, database='yuanchao', charset='utf8')
cur = con.cursor()
sql1 = '''drop database if exists userdb '''
sql11 = 'create database userdb'
sql2 = 'use userdb'
sql3 = '''drop table if exists user'''
sql33 = '''
create TABLE user
(name VARCHAR(100),age int,score int);'''
sql4 = "insert into user values('Tom',25,99)"
cur.execute(sql1)
cur.execute(sql11)
cur.execute(sql2)  # 居然不能把use userdb合并成一句写！！！！！！！
cur.execute(sql3)
cur.execute(sql33)
cur.execute(sql4)
con.commit()
cur.close()
con.close()
