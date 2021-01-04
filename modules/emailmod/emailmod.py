""" Extension for sending E-Mails. """
# Import libs required for send_email function.
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from discord.ext import commands
import modules.dbmod.dbmain as db
from modules.firstuse.firstuse import user_setup
from modules.utils.utils import ask, checkexist, selectwhere

async def send_email(esmtp: str, eport: int,
                     epwrd: str, esndr: str,
                     ercvr: str, esubj: str,
                     ebody: str) -> None:

    """ Function in charge of the back-end part of sending the E-Mail"""

    # Encodes Message.
    msg = MIMEMultipart()
    msg['From']     = esndr
    msg['To']       = ercvr
    msg['Subject']  = esubj
    msg.attach(MIMEText(ebody, 'plain'))
    ectnt = msg.as_string()

    # Creates SMTP session and starts TLS.
    try:
        server = smtplib.SMTP(esmtp, eport)
        server.starttls()
        server.ehlo()

    # Logs in and sends E-Mail.
        server.login(esndr, epwrd)
        server.sendmail(esndr, ercvr, ectnt)
        success = "E-Mail sent successfully!"
        return success
    except SystemError:
        error = f"""It seems we've encountered an error sendng your E-Mail.
        This normally happens when the given details are wrong, such as passwords.
        If you recently changed passwords, please delete your stored details from the bot and add your account again with your new password.
        Error details: {sys.exc_info()}"""
        return error



async def link_account(self, ctx):
    """ Function called when user wants to link E-Mail account. """
    await ctx.channel.send('''You are now running the account linking command.

We care about your privacy and account security, as such, you should know, after this process is finished, your account details will be encrypted, as such we won't have access to the unencrypted details.

We will need the following details to link your account, if your provider has one, be sure to use the SMTP port and URL specific to STARTTLS.''')

    loop = True
    while loop:

        email, cancelled = await ask(self, ctx, "Please enter the E-Mail address you'd like to link.", True)
        if cancelled:
            return 3

        epwrd, cancelled = await ask(self, ctx, "Please enter the E-Mail account password.", True)
        if cancelled:
            return 3

        esmtp, cancelled = await ask(self, ctx, "Please enter the E-Mail provider's SMTP server URL.", True)
        if esmtp.lower() == 'smtp.office365.com':
            await ctx.channel.send("We're sorry, due to Microsoft's E-Mail policies, we don't yet support linking Microsoft E-Mail accounts. This might be due to change in the future, but as of now, we don't have plans to add support for it.")
            return 2
        if cancelled:
            return 3

        eport, cancelled = await ask(self, ctx, "Please enter the E-Mail provider's SMTP server port.", True)
        if cancelled:
            return 3
    
        ename, cancelled = await ask(self, ctx, 'What would you like to name this preset?', True)
        if cancelled:
            return 3

        confirmed, cancelled = await ask(self, ctx, f'''Please verify these details are correct.
E-Mail preset name: {ename}
E-Mail address: {email}
E-Mail password: {epwrd}
SMTP server URL: {esmtp}
SMTP server port: {eport}
Is this correct? (Yes/No)''', True)

        if cancelled:
            return 3

        if confirmed.lower() == 'yes':
            loop = False

        elif confirmed.lower() == 'no':
            await ctx.channel.send("Account linking setup restarted!")
        

    await ctx.channel.send("Please hold on while I attempt to log into your account to verify the given credentials are correct.")
    try:
        server = smtplib.SMTP(esmtp, eport)
        server.starttls()
        server.ehlo()

        # Logs in to test credentials.
        server.login(email, epwrd)

        await ctx.channel.send('''E-Mail linked successfully!
To keep you secure, please delete your messages that contain sensitive details in case your account gets compromised.''')

        edb = db.Mail(ename=ename, esmtp=esmtp,
                    eport=eport, email=email,
                    epwrd=epwrd, usrid=ctx.author.id)
        db.orm.add(edb)
        db.orm.commit()
        return 1

    except:
        error = f"""It seems we've encountered an error logging into your E-Mail.
This normally happens when you've entered the wrong details, such as an incorrect password, or wrong/outdated SMTP details.
Please make sure you've entered the wrong details and run this command again.
Error details:
```{sys.exc_info()}```"""
        await ctx.channel.send(error)
        return 2


class Mailcmd(commands.Cog):
    """ Discord.py cog for the client side of E-Mail sending. """
    def __init__(self, client):
        self.bot = client

    # mail command
    @commands.command()
    async def mail(self, ctx):
        ''' Function for the mail command. '''

        if not await checkexist(db.User, db.User.usrid, ctx.author.id):
            success = await user_setup(self, ctx)
            if not success:
                return
        
        cmd = ctx.message.clean_content
        cmd = cmd[7:]

        async def create(self, ctx):
            success = await link_account(self, ctx)
            if success == 1 or 2:
                return

            elif success == 3:
                ctx.channel.send('Account linking setup cancelled successfully!')
                return

        async def send(self, ctx):
            if not await checkexist(db.Mail, db.Mail.usrid, ctx.author.id):
                askusr = await ask(self, ctx, '''Hey there!
It seems you have not set up an E-Mail account to use with this bot.
Would you like to do so? (Yes/No)''', False)
                
                loop = True
                while loop:
                    if askusr.lower() == 'yes':
                        success = await link_account(self, ctx)
                        if success == 2:
                            return
                        elif success == 3:
                            await ctx.channel.send('Account linking setup cancelled successfully!')
                            return
                        loop = False

                    elif askusr.lower() == 'no':
                        return

                    else:
                        askusr = await ask(self, ctx, 'You entered a wrong value, please retry!', False)

            column = [db.edtls.c.usrid, db.edtls.c.ename]
            e = await selectwhere(column, db.edtls.c.usrid, ctx.author.id)
            for row in e:
                print(row)

        # If no argument, or argument does not match.
        async def none(self, ctx):
            await ctx.channel.send('''Wrong command syntax!
Command mail needs an argument.
`e.mail (action)`
Valid actions: linkaccount | send''')

            return
        
        async def switch(option):
            options = {
                'create':   create,
                'send':     send
            }
            return options.get(option, none)

        argument = await switch(cmd)
        await argument(self, ctx)


def setup(bot):
    """ Add mail_cog cog to bot. """
    bot.add_cog(Mailcmd(bot))
