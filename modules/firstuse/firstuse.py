""" Is ran when a user uses the bot for the first time or when the bot is added to a new server. """
from modules.dbmod.dblist import UsrPrefs
from modules.dbmod.dbmain import ormsession

async def user_setup(self, ctx):
    async def askfunc(self, ctx, cont):
        await ctx.channel.send(cont)
        def pred(original):
            return original.author == ctx.author and original.channel == ctx.channel
        ans = await self.bot.wait_for('message', check=pred)
        ans = ans.clean_content
        return ans
    confirm = await askfunc(self, ctx, '''Hi there!
Before using me, we need to set up your preferences.
Would you like to set up your preferences? (Yes/No)
''')
    if confirm.lower() == 'yes':
        await ctx.channel.send('''First use setup started!
Use ``cancel`` anytime to cancel this setup.''')

        async def askdtls(self, ctx):
            loop = True
            while loop:
                usrid = ctx.author.id

                alias = await askfunc(self, ctx, '''What name do you want me to call you?''')
                if alias.lower() == 'cancel':
                    return

                loop2 =  True
                while loop2:
                    nouns = await askfunc(self, ctx, '''What pronouns would you like me to use?
1. He/Him
2. She/Her
3. They/Them''')
                    if nouns == '1':
                        pnoun = 'He/Him'
                        loop2 = False

                    elif nouns == '2':
                        pnoun = 'She/Her'
                        loop2 = False

                    elif nouns == '3':
                        pnoun = 'They/Them'
                        loop2 = False

                    elif nouns.lower() == 'cancel':
                        return

                    else:
                        await ctx.channel.send('You entered a wrong value, please retry!')

                confirm = await askfunc(self, ctx, f'''I will now call you {alias} and use {pnoun} when referring to you. 
Is that correct? (Yes/No)''')
                loop2 = True
                while loop2:
                    if confirm.lower() == 'yes':            
                        toadd = UsrPrefs(usrid=usrid, alias=alias, nouns=nouns)
                        ormsession.add(toadd)
                        ormsession.commit()
                        return True

                    elif confirm.lower() == 'no':
                        await ctx.channel.send('First use setup restarted!')
                        loop2 = False

                    elif confirm.lower() == 'cancel':
                        await ctx.channel.send('First use setup cancelled successfully!')
                        return

                    else:
                        confirm = await askfunc(self, ctx, 'You entered a wrong value, please retry!')

        confirm = await askdtls(self, ctx)

        if not confirm:
            await ctx.channel.send('First use setup cancelled successfully!')
            return

        elif confirm:
            await ctx.channel.send('First use setup successful!')
            return True
    
    elif confirm.lower() == 'no':
        await ctx.channel.send('First use setup cancelled successfully!')
        return
