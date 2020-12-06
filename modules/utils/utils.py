""" Contains commonly used code as functions. """

import modules.dbmod.dbmain as db
from sqlalchemy.sql import select

async def ask(self, ctx, cont, cancellable):
    """ Function to minimize code size, is in charge
    of sending messages, awaiting for the response
    and returning its value """

    await ctx.channel.send(cont)
    def pred(original):
        return original.author == ctx.author and original.channel == ctx.channel
    ans = await self.bot.wait_for('message', check=pred)
    ans = ans.clean_content
    if cancellable:

        cancel = False

        if ans.lower() == 'cancel':
            cancel = True

        return ans, cancel

    return ans

async def findinquery(intable, incolumn, thisvalue):
    """ Executes a select statement, 
    returning a whole row in {intable} 
    with {thisvalue} in {incolumn}"""
    return db.dbconnect.execute(select(intable).where(incolumn == thisvalue))

async def checkexist(intable, incolumn, thisvalue):
    """ Checks if row in {incolumn} 
    exists with {thisvalue} in {intable},
    returning a True/False value"""
    return db.orm.query(db.orm.query(intable).filter(incolumn == thisvalue).exists()).scalar()
