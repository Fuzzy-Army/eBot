# Import libs required for send_email function.
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from discord.ext import commands
from sqlalchemy import Column, Integer, String
from modules.dbmod.base import Base
from modules.dbmod.dbmain import ormsession

class Email(Base):
    """ Define the E-Mail details table. """
    __tablename__ = 'edtls'

    usrid = Column(Integer, primary_key=True)
    esmtp = Column(String)
    eport = Column(Integer)
    email = Column(String)
    epwrd = Column(String)
 
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

class Mailcmd(commands.Cog):
    """ Discord.py cog for the client side of E-Mail sending"""
    def __init__(self, client):
        self.bot = client

    # mail command
    @commands.command()
    async def mail(self, ctx):
        """ Function to minimize code size, is in charge
            of sending messages, awaiting for the response
            and returning its value """
        async def askfunc(self, ctx, cont):
            await ctx.channel.send(cont)
            def pred(m):
                return m.author == ctx.author and m.channel == ctx.channel
            ans = await self.bot.wait_for('message', check=pred)
            ans = ans.clean_content
            return ans
            
        print(ormsession.query(ormsession.query(Email).filter(Email.usrid == ctx.author.id).exists()).scalar())
        await ctx.channel.send("You are now running the E-Mail command, please follow the next instructions.")
        esmtp = await askfunc(self, ctx, '''What is the URL of the SMTP server that your E-Mail service provider provides?
        If you are not sure, please look online for your E-Mail provider SMTP settings.''')
        eport = await askfunc(self, ctx, "What's the port of the SMTP server?")
        esndr = await askfunc(self, ctx, 'What is your E-Mail account address?')
        epwrd = await askfunc(self, ctx, 'And your password?')
        ercvr = await askfunc(self, ctx, "What is the recipient's E-Mail address?")
        esubj = await askfunc(self, ctx, 'Now, please send the E-Mail subject.')
        ebody = await askfunc(self, ctx, 'Next, send the E-Mail contents.')
        # calls send_email function and waits for it to return output
        ertrn = await send_email(esmtp, eport, epwrd, esndr, ercvr, esubj, ebody)
        await ctx.channel.send(ertrn)

def setup(bot):
    """ Add mail_cog cog to bot. """
    bot.add_cog(Mailcmd(bot))
