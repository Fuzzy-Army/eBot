""" Is ran when a user uses the bot for the first time or when the bot is added to a new server. """
from modules.dbmod.dblist import UserDtls
from modules.dbmod.dbmain import ormsession

async def user_setup(self, ctx):
    await ctx.channel.send('''Hi there!
Before using me, we need to set up your profile, please answer the following questions.
''')
    async def askfunc(self, ctx, cont):
        await ctx.channel.send(cont)
        def pred(m):
            return m.author == ctx.author and m.channel == ctx.channel
        ans = await self.bot.wait_for('message', check=pred)
        ans = ans.clean_content
        return ans

    async def askdtls(self, ctx):
        usrid = ctx.author.id
        alias = await askfunc(self, ctx, '''What name do you want me to call you?''')
        nouns = await askfunc(self, ctx, '''What pronouns would you like me to use?
1. He/Him
2. She/Her
3. They/Them''')
        if nouns == '1':
            pnoun = 'He/Him'

        elif nouns == '2':
            pnoun = 'She/Her'

        elif nouns == '3':
            pnoun = 'They/Them'

        confirm = await askfunc(self, ctx, f'''I will now call you {alias} and use {pnoun} when referring to you. 
Is that correct? (Yes/No)''')
        if confirm == 'Yes':            
            toadd = UserDtls(usrid=usrid, alias=alias, nouns=nouns)
            ormsession.add(toadd)
            ormsession.commit()
            return True
        else:
            return False

    confirm = False
    while not confirm:
        confirm = await askdtls(self, ctx)
        if not confirm:
            await ctx.channel.send('Setup restarted!')
        elif confirm:
            await ctx.channel.send('Setup successful!')
