#!/usr/local/bin/python3
from cgitb import enable
enable()
from cgi import FieldStorage
from html import escape
import pymysql as db

print('Content-Type: text/plain')
print()

form_data = FieldStorage()
score = escape(form_data.getfirst('score', '').strip())

try:
     connection = db.connect('cs1.ucc.ie', 'rh31', 'ahwuz', 'cs6503_cs1106_rh31')
     cursor = connection.cursor(db.cursors.DictCursor)
     cursor.execute("""INSERT INTO scores VALUES (%s)""", (score))
     connection.commit()
    print('success')
     cursor.close()
     connection.close()
except db.Error:
    print('problem')
