from sqlalchemy import Column, Integer, String
from fly import db


class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=False)
    pwd = Column(String(32), )
    __table_args__={
        'mysql_engine':'InnoDB',
        'mysql_charset':'utf8'
    }
class Groups(db.Model):
    __tablename__='groups'
    id=Column(Integer,primary_key=True)
    name=Column(String(32),index=True, nullable=False)
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
