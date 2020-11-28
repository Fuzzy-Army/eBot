from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import modules.dbmod.base as base
import modules.dbmod.dblist

dbengine = create_engine('postgresql://dev-wolf:cute-dev-wolf@localhost:62100/uwu', echo=True)

base.Base.metadata.create_all(dbengine, checkfirst=True)

session_init = sessionmaker(bind=dbengine)
ormsession = session_init()