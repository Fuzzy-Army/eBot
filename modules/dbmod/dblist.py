from sqlalchemy import String, BigInteger, Integer, Column, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship
import modules.dbmod.base as base

metadata = MetaData()

class UsrPrefs(base.Base):
    """ Define user preferences table """
    __tablename__ = 'usrprefs'

    usrid = Column(BigInteger, primary_key=True)
    alias = Column(String)
    nouns = Column(Integer)
    email = relationship("Email")


class Email(base.Base):
    """ Define the E-Mail details table. """
    __tablename__ = 'edtls'

    eid     = Column(Integer, primary_key=True)
    ename   = Column(String)
    esmtp   = Column(String)
    eport   = Column(Integer)
    email   = Column(String)
    epwrd   = Column(String)
    usrid   = Column(BigInteger, ForeignKey('usrprefs.usrid'), index=True)

edtls = Table('edtls', metadata,
              Column('eid', Integer, primary_key=True),
              Column('ename', String),
              Column('esmtp', String),
              Column('eport', Integer),
              Column('email', String),
              Column('epwrd', String),
              Column('usrid', BigInteger, ForeignKey('usrprefs.usrid'), index=True))

class SrvPrefs(base.Base):
    """ Define server preferences table. """
    __tablename__ = 'srvprefs'

    srvid   = Column(BigInteger, primary_key=True)
    prefix  = Column(String)