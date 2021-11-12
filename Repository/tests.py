from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.

#读取数据库里的内容
# !/usr/bin/python3
# coding=utf-8

import pymysql

# Open database connection
db = pymysql.connect(host='121.40.142.200',
    user='root',
    password='1234',
    database='starFlow')


# prepare a cursor object using cursor() method
cursor = db.cursor()
# 按字典返回
# cursor = db.cursor(pymysql.cursors.DictCursor)

# 查询操作，从member表里输出所有信息，条件为id=xxxx
sql = "SELECT * FROM Repository_member "
# print (sql)
try:
    # Execute the SQL command
    cursor.execute(sql)
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    for row in results:
        # print (row)
        #输出前端要的内容，从表的row赋值给他

        # Now print fetched result
        #print("name = %s %s,age = %s,sex = %s,income = %s" % \
              #(fname, lname, age, sex, income))
except:
    import traceback

    traceback.print_exc()

    print("Error: unable to fetch data")

# disconnect from server
db.close()
11111111
