# Import libs required for send_email function.
import ssl
import sys
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Function in charge of the actual E-Mail sending.
async def SNDEML(eSMTP: str, ePORT, ePWRD: str, eSNDR: str, eRCVR: str, eSUBJ: str, eBODY: str) -> None:

    # Encodes Message.
    msg = MIMEMultipart()
    msg['From']     = eSNDR
    msg['To']       = eRCVR
    msg['Subject']  = eSUBJ
    msg.attach(MIMEText(eBODY, 'plain'))
    TXT = msg.as_string()

    # Creates SMTP session and starts TLS.
    try:
        server = smtplib.SMTP(eSMTP, ePORT)
        server.starttls()
        server.ehlo()

    # Logs in and sends E-Mail.
        server.login(eSNDR, ePWRD)
        server.sendmail(eSNDR, eRCVR, TXT)
        sccs = "e-mail sent successfully"
        return sccs
    except:
        emsg = f"ERROR: {sys.exc_info()}"
        return emsg


    # Import discord.py library.
from discord.ext import commands

# set up class for cog
class mail_cog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    # mail command
    @commands.command()
    async def mail(self, ctx):
        # function to condense certain repetitive functions.
        async def askfunc(self, ctx, cont):
            await ctx.channel.send(cont)
            def pred(m):
                return m.author == ctx.author and m.channel == ctx.channel
            ans = await self.bot.wait_for('message', check=pred)
            ans = ans.clean_content
            return ans
        await ctx.channel.send("You are now running the E-Mail command, please follow the next instructions.")
        eSMTP = await askfunc(self, ctx, '''What is the URL of the SMTP server that your E-Mail service provider provides?
        If you are not sure, please look online for your E-Mail provider SMTP settings.''')
        ePORT = await askfunc(self, ctx, "What's the port of the SMTP server?")
        eSNDR = await askfunc(self, ctx, 'What is your E-Mail account address?')
        ePWRD = await askfunc(self, ctx, 'And your password?')
        eRCVR = await askfunc(self, ctx, "What is the recipient's E-Mail address?")
        eSUBJ = await askfunc(self, ctx, 'Now, please send the E-Mail subject.')
        eBODY = await askfunc(self, ctx, 'Next, send the E-Mail contents.')
        # calls send_email function and waits for it to return output
        ertrn = await SNDEML(eSMTP, ePORT, ePWRD, eSNDR, eRCVR, eSUBJ, eBODY)
        await ctx.channel.send(ertrn)

# setup cog
def setup(bot):
    bot.add_cog(mail_cog(bot))