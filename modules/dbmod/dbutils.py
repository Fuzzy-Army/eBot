""" Collection of db functions that are often used """
import modules.dbmod.dbmain as db
from sqlalchemy.sql import select

async def findinquery(intable, incolumn, thisvalue):
    """ Executes a select statement, 
    returning a whole row in {intable} 
    with {thisvalue} in {incolumn}"""
    return db.dbconnect.execute(select([intable]).where(incolumn == thisvalue))

async def checkexist(intable, incolumn, thisvalue):
    """ Checks if row in {incolumn} 
    exists with {thisvalue} in {intable},
    returning a True/False value"""
    return db.ormsession.query(db.ormsession.query(intable).filter(incolumn == thisvalue).exists()).scalar()
