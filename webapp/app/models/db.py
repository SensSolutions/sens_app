# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:48:58 2015

@author: mcollado

mysql> desc user;

+--------+---------+------+-----+---------+----------------+
| Field  | Type    | Null | Key | Default | Extra          |
+--------+---------+------+-----+---------+----------------+
| id     | int(11) | NO   | PRI | NULL    | auto_increment |
| name   | text    | NO   |     | NULL    |                |
| passwd | text    | NO   |     | NULL    |                |
| email  | text    | YES  |     | NULL    |                |
+--------+---------+------+-----+---------+----------------+

mysql> desc data;
+-----------+-------------+------+-----+---------+----------------+
| Field     | Type        | Null | Key | Default | Extra          |
+-----------+-------------+------+-----+---------+----------------+
| id        | int(11)     | NO   | PRI | NULL    | auto_increment |
| org       | varchar(50) | YES  |     | NULL    |                |
| place     | varchar(50) | YES  |     | NULL    |                |
| what      | varchar(50) | YES  |     | NULL    |                |
| sensor    | varchar(50) | YES  |     | NULL    |                |
| type      | varchar(50) | YES  |     | NULL    |                |
| dname     | varchar(50) | YES  |     | NULL    |                |
| dvalue    | float       | YES  |     | NULL    |                |
| timestamp | datetime    | YES  |     | NULL    |                |
| payload   | text        | YES  |     | NULL    |                |
| _dthhmm   | datetime    | YES  |     | NULL    |                |
+-----------+-------------+------+-----+---------+----------------+

http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#sql-abstraction-layer
http://docs.sqlalchemy.org/en/rel_1_0/core/connections.html
http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html

http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
http://stackoverflow.com/questions/19406859/sqlalchemy-convert-select-query-result-to-a-list-of-dicts
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    passwd = Column(Text)
    email = Column(Text)
    def __repr__(self):
        return self


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    org = Column(String(50))
    place = Column(String(50))
    what = Column(String(50))
    sensor = Column(String(50))
    type = Column(String(50))
    dname = Column(String(50))
    dvalue = Column(Float)
    timestamp = Column(DateTime)
    payload = Column(Text)
    _dthhmm = Column(DateTime)
    def __repr__(self):
        return self


engine = create_engine('mysql://mqtt:@localhost/mqtt', echo=True)
Session = sessionmaker(bind=engine)

Session.configure(bind=engine)  # once engine is available
session = Session()

"""
Example Add registers

ed_user = User(name='edi', passwd='passwd', email='edsmail@mail.org')

session.add_all([
    User(name='wendy', email='wend@mail.org', passwd='foobar'),
    User(name='mary', email='mary@mail.org', passwd='xxg527'),
    User(name='fred', email='fred@mail.org', passwd='blah')])

for dades in session.query(Data).filter(Data.timestamp >= '2015-11-05 12:00:00').filter(Data.sensor == 'air').filter(
                Data.dname == 'temperature'):
    print dades.dname, dades.dvalue, dades.timestamp
"""

"""
How to get last value:
Current temp from air sensor

SQL:
use mqtt;
SELECT data.place, data.timestamp, data.dvalue
FROM data
WHERE  data.timestamp >= '2015-11-06' AND data.dname ='temperature' AND sensor ='air'
ORDER BY data.timestamp DESC
LIMIT 0,1

"""

last_user = session.query(User.id, User.name, User.email).order_by(User.id.desc()).first()

import datetime
i = datetime.datetime.now()
now = i.strftime('%Y-%m-%d') #2015-11-06

last_temp = session.query(Data.dvalue).filter(Data.timestamp >= now).filter(Data.sensor == 'air').filter(Data.dname == 'temperature').order_by((Data.id.desc())).first()
print last_temp[0]

"""
How to get a list and JSONify it
"""
row = session.query(User.id, User.name, User.email).all()

import json
row_json = json.dumps(row, sort_keys=True,indent=4)

row2 = session.query(Data.timestamp, Data.dvalue).filter(Data.timestamp >= '2015-11-05 12:00:00').filter(Data.sensor == 'air').filter(Data.dname == 'temperature').

"""
use mqtt;
SELECT data.place, data.timestamp, data.dvalue
FROM data
WHERE data.timestamp >= '2015-11-06' AND data.dname ='temperature' AND sensor ='air'
ORDER BY data.timestamp ASC
LIMIT 0,9999
"""




