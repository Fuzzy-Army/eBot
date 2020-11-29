""" Extension for sending E-Mails. """
# Import libs required for send_email function.
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from discord.ext import commands
from modules.dbmod.dblist import UsrPrefs, Email, SrvPrefs
from modules.dbmod.dbmain import ormsession
from modules.firstuse.firstuse import user_setup
from sqlalchemy.sql import select

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

async def link_account(self, ctx, askfunc):
    """ Function called when user wants to link E-Mail account. """
    await ctx.channel.send('''You are now running the account linking command.

We care about your privacy and account security, as such, you should know, after this process is finished, your account details will be encrypted, as such we won't have access to the unencrypted details.

We will need the following details to link your account, if your provider has one, be sure to use the SMTP port and URL specific to STARTTLS.''')

    loop = True
    while loop:

        email = await askfunc(self, ctx, "Please enter the E-Mail address you'd like to link.")
        if email.lower() == 'cancel':
            return 3

        epwrd = await askfunc(self, ctx, "Please enter the E-Mail account password.")
        if epwrd.lower() == 'cancel':
            await ctx.channel.send('Command cancelled successfully!')
            return 3

        esmtp = await askfunc(self, ctx, "Please enter the E-Mail provider's SMTP server URL.")
        if esmtp.lower() == 'smtp.office365.com':
            await ctx.channel.send("We're sorry, due to Microsoft's E-Mail policies, we don't yet support linking Microsoft E-Mail accounts. This might be due to change in the future, but as of now, we don't have plans to add support for it.")
            return 2
        elif esmtp.lower() == 'cancel':
            return 3

        eport = await askfunc(self, ctx, "Please enter the E-Mail provider's SMTP server port.")
        if eport.lower() == 'cancel':
            return 3
    
        ename = await askfunc(self, ctx, 'What would you like to name this preset?')
        if ename.lower() == 'cancel':
            return 3

        confirmed = await askfunc(self, ctx, f'''Please verify these details are correct.
E-Mail preset name: {ename}
E-Mail address: {email}
E-Mail password: {epwrd}
SMTP server URL: {esmtp}
SMTP server port: {eport}
Is this correct? (Yes/No)''')

        if confirmed.lower() == 'yes':
            loop = False

        elif confirmed.lower() == 'no':
            await ctx.channel.send("Account linking setup restarted!")
        
        elif confirmed.lower() == 'cancel':
            return 3

    await ctx.channel.send("Plese hold on while I attempt to log into your account to verify the given credentials are correct.")
    try:
        server = smtplib.SMTP(esmtp, eport)
        server.starttls()
        server.ehlo()

        # Logs in to test credentials.
        server.login(email, epwrd)

        await ctx.channel.send('''E-Mail linked successfully!
To keep you secure, please delete your messages that contain sensitive details in case your account gets compromised.''')

        edb = Email(ename=ename, esmtp=esmtp,
                    eport=eport, email=email,
                    epwrd=epwrd, usrid=ctx.author.id)
        ormsession.add(edb)
        ormsession.commit()
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

        async def askfunc(self, ctx, cont):
            """ Function to minimize code size, is in charge
            of sending messages, awaiting for the response
            and returning its value """

            await ctx.channel.send(cont)
            def pred(original):
                return original.author == ctx.author and original.channel == ctx.channel
            ans = await self.bot.wait_for('message', check=pred)
            ans = ans.clean_content
            return ans

        user_exists = ormsession.query(ormsession.query(UsrPrefs).filter(UsrPrefs.usrid == ctx.author.id).exists()).scalar()

        if not user_exists:
            success = await user_setup(self, ctx)
            if not success:
                return
        
        cmd = ctx.message.clean_content

        if cmd[7:].lower() == 'linkaccount':
            success = await link_account(self, ctx, askfunc)
            if success == 1 or 2:
                return

            elif success == 3:
                ctx.channel.send('Account linking setup cancelled successfully!')
                return

        elif cmd[7:].lower() == 'send':
            user_exists = ormsession.query(ormsession.query(Email).filter(Email.usrid == ctx.author.id).exists()).scalar()

            if not user_exists:
                ask = await askfunc(self, ctx, '''Hey there!
It seems you have not set up an E-Mail account to use with this bot.
Would you like to do so? (Yes/No)''')

                if ask.lower() == 'yes':
                    success = await link_account(self, ctx, askfunc)
                    if success == 2:
                        return

                    elif success == 3:
                        await ctx.channel.send('Account linking setup cancelled successfully!')
                        return

                elif ask.lower() == 'no':
                    await ctx.channel.send('''E-Mail sending cannot proceed without a linked account.
Command has been cancelled.''')
                    return

            #find = select([users]).where(users.c.name == 'uwu')
            #ertrn = await send_email(esmtp, eport, epwrd, esndr, ercvr, esubj, ebody)
        else:
            await ctx.channel.send('''Wrong command syntax!
Command mail needs an argument.
``e.mail (argument_1)``
argument_1: linkaccount | send''')
            return

def setup(bot):
    """ Add mail_cog cog to bot. """
    bot.add_cog(Mailcmd(bot))
