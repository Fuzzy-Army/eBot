""" The mitochondria is the powerhouse of the cell...
Defines tables along with the ORM and the SQL core of SQLAlchemy """
from sqlalchemy import create_engine,  String, BigInteger, Integer, Column, ForeignKey, Table, MetaData
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """ Defines user preferences table. """
    __tablename__ = 'usrprefs'
    usrid = Column(BigInteger, primary_key=True, index=True)
    alias = Column(String)
    nouns = Column(Integer)
    email = relationship("Mail")

class Mail(Base):
    """ Defines the E-Mail details table. """
    __tablename__ = 'edtls'
    eid     = Column(Integer, primary_key=True)
    ename   = Column(String)
    esmtp   = Column(String)
    eport   = Column(Integer)
    email   = Column(String)
    epwrd   = Column(String)
    usrid   = Column(BigInteger, ForeignKey('usrprefs.usrid'), index=True)

class Server(Base):
    """ Defines server preferences table. """
    __tablename__ = 'srvprefs'
    srvid   = Column(BigInteger, primary_key=True, index=True)
    prefix  = Column(String)

class WordGen(Base):
    """ Defines words table
    for password generation. """
    __tablename__ = 'wordgen'
    wordID      = Column(Integer, primary_key=True, index=True)
    longword    = Column(String)
    mediumword  = Column(String)
    shortword   = Column(String)

metadata = MetaData()

usrprefs    = Table('usrprefs', metadata,
                    Column('usrid', BigInteger, primary_key=True, index=True),
                    Column('alias', String),
                    Column('nouns', Integer))

edtls       = Table('edtls', metadata,
                    Column('eid', Integer, primary_key=True),
                    Column('ename', String),
                    Column('esmtp', String),
                    Column('eport', Integer),
                    Column('email', String),
                    Column('epwrd', String),
                    Column('usrid', BigInteger, ForeignKey('usrprefs.usrid'), index=True))

srvprefs    = Table('srvprefs', metadata,
                    Column('srvid', BigInteger, primary_key=True, index=True),
                    Column('prefix', String))

wordgen     = Table('wordgen', metadata,
                    Column('wordID', Integer, primary_key=True, index=True),
                    Column('longword', String),
                    Column('mediumword', String),
                    Column('shortword', String))

# Define engine with database connection.
dbengine = create_engine('postgresql://dev-wolf:cute-dev-wolf@localhost:62100/uwu')

# Create all defined tables if not exist.
Base.metadata.create_all(dbengine, checkfirst=True)

# Initialize ORM instance.
session_init = sessionmaker(bind=dbengine)
orm = session_init()

# Initialize engine connection.
dbconnect = dbengine.connect()
