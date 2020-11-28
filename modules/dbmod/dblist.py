from sqlalchemy import String, BigInteger, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
import modules.dbmod.base as base

class UserDtls(base.Base):
    """ Define user preferences table """
    __tablename__ = 'usrdtls'

    usrid = Column(BigInteger, primary_key=True)
    alias = Column(String)
    nouns = Column(Integer)
    email = relationship("Email")


class Email(base.Base):
    """ Define the E-Mail details table. """
    __tablename__ = 'edtls'

    idnmb = Column(Integer, primary_key=True)
    ename = Column(String)
    esmtp = Column(String)
    eport = Column(Integer)
    email = Column(String)
    epwrd = Column(String)
    usrid = Column(BigInteger, ForeignKey('usrdtls.usrid'))
