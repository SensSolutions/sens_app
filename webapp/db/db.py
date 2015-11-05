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
#        return "<User(name='%s', email='%s')>" % (self.name, self.email)
        return [self.id, self.name, self.passwd, self.email]

class Data(Base):
    __tablename__= 'data'
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

ed_user =User(name='edi', passwd='passwd', email='edsmail@mail.org')

session.add_all([
    User(name='wendy', email='wend@mail.org', passwd='foobar'),
    User(name='mary',  email='mary@mail.org', passwd='xxg527'),
    User(name='fred',  email='fred@mail.org', passwd='blah')])

for dades in session.query(Data).filter(Data.timestamp>='2015-11-05 12:00:00').filter(Data.sensor=='air').filter(Data.dname=='temperature'):
    print dades.dname, dades.dvalue, dades.timestamp

"""
How to get last value:
""""
results = session.query(Data).filter(Data.timestamp>='2015-11-05 12:00:00').filter(Data.sensor=='air').filter(Data.dname=='temperature').order_by((Data.id.desc()))
results.fisrt()
