""" Is ran when a user uses the bot for the first time or when the bot is added to a new server. """
import modules.dbmod.dbmain as db
from modules.utils.utils import askfunc as ask

async def user_setup(self, ctx):
    confirm, cancel = await ask(self, ctx, '''Hi there!
Before using me, we need to set up your preferences.
Would you like to set up your preferences? (Yes/No)
''')
    if confirm.lower() == 'yes':
        await ctx.channel.send('''First use setup started!
Use ``cancel`` anytime to cancel this setup.''')

        async def askdtls(self, ctx):
            loop = True
            # Loops until user either
            # confirms or cancels command.
            while loop:
                # Fetch user ID to store later.
                usrid = ctx.author.id

                # Ask user for preferred name.
                alias, cancelled = await ask(self, ctx, '''What name do you want me to call you?''')

                # If ask() returned True on cancelled, return.
                if cancelled:
                    return

                # Deteremine if user provided valid option,
                # and returns contents of valid option.
                async def determine_noun(nouns):
                    switchx = {
                        '1': 'He/Him',
                        '2': 'She/Her',
                        '3': 'They/Them'
                    }
                    switchy = {
                        '1': False,
                        '2': False,
                        '3': False
                    }
                    return switchx.get(nouns), switchy.get(nouns, True)

                # Ask user for preferred pronouns.
                nouns, cancelled = await ask(self, ctx, '''What pronouns would you like me to use?
1. He/Him
2. She/Her
3. They/Them''')

                # If ask() returned True on cancelled, return.
                if cancelled:
                    return
                
                # Determine if user provided valid value
                # and convert it to its appropriate meaning.
                pnoun, loop2 = await determine_noun(nouns)

                # Loops until user provides a valid answer.
                while loop2:
                    nouns, cancelled = await ask(self, ctx, 'You entered a wrong value, please retry!')
                    pnoun, loop2 = determine_noun(nouns)
                    # If ask() returned True on cancelled, return.
                    if cancelled:
                        return

                # Switch case to determine if
                # user provided valid value and
                # if user needs to start again.
                async def determine_confirm(confirm):
                    # If user says yes, return True, if no, return False
                    switchx = {
                        'yes':      True,
                        'no':       False
                    }
                    # If message matches these, return False, if not, return True
                    switchy = {
                        'yes':      False,
                        'no':       False
                    }
                    return switchx.get(confirm), switchy.get(confirm, True)
                
                # Ask user for confirmation on provided details.
                confirm, cancelled = await ask(self, ctx, f'''I will now call you {alias} and use {pnoun} when referring to you. 
Is that correct? (Yes/No)''')

                # If ask() returned True on cancelled, return.
                if cancelled:
                    return

                # Determine if valid user
                # response and convert to boolean.
                confirm, loop2 = await determine_confirm(confirm.lower())

                # Loops until user provides a valid answer.
                while loop2:
                    confirm, cancelled = await ask(self, ctx, 'You entered a wrong value, please retry!')
                    # If ask() returned True on cancelled, return.
                    if cancelled:
                        return
                    confirm, loop2 = await determine_confirm(confirm.lower())

                # Add user details to database.
                user = db.User(usrid=usrid, 
                               alias=alias,
                               nouns= nouns)
                db.orm.add(user)
                db.orm.commit()

                return True

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
