# -*- coding: utf-8 -*-
"""
mysql> select * from user;

+----+--------+---------+------------------+
| id | name   | passwd  | email            |
+----+--------+---------+------------------+
|  1 | kcraam |         | kcraam           |
+----+--------+---------+------------------+

mysql> desc data;
+-----------+-------------+------+-----+---------+-------+
| Field     | Type        | Null | Key | Default | Extra |
+-----------+-------------+------+-----+---------+-------+
| org       | varchar(50) | YES  |     | NULL    |       |
| place     | varchar(50) | YES  |     | NULL    |       |
| what      | varchar(50) | YES  |     | NULL    |       |
| sensor    | varchar(50) | YES  |     | NULL    |       |
| type      | varchar(50) | YES  |     | NULL    |       |
| dname     | varchar(50) | YES  |     | NULL    |       |
| dvalue    | float       | YES  |     | NULL    |       |
| timestamp | datetime    | YES  |     | NULL    |       |
| payload   | text        | YES  |     | NULL    |       |
| _dthhmm   | datetime    | YES  |     | NULL    |       |
+-----------+-------------+------+-----+---------+-------+

http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#sql-abstraction-layer
http://docs.sqlalchemy.org/en/rel_1_0/core/connections.html

"""
from app import app
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String


SQLALCHEMY_DATABASE_URI = 'mysql://mqtt:passsecret@localhost/mqtt'

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
metadata = MetaData(bind=engine)

connection = engine.connect()

users = Table('user', metadata, autoload=True)
data = Table('data', metadata, autoload=True)

dades = data.select(data.c.timestamp >= '2015-11-03 00:00:00').execute()

connection.close()
