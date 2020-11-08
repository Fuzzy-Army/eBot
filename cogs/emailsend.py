# Import libs required for send_email function.
import ssl
import sys
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Function in charge of sending E-Mail.
async def send_email(esmtp: str, esend: str, erecv: str, esubj: str, epwrd: str, ebody: str, eport) -> None:

    # Encodes Message.
    msg = MIMEMultipart()
    msg['From']     = esend
    msg['To']       = erecv
    msg['Subject']  = esubj
    msg.attach(MIMEText(ebody, 'plain'))
    txt = msg.as_string()

    # Creates SMTP session and starts TLS.
    try:
        server = smtplib.SMTP(esmtp, eport)
        server.starttls()
        server.ehlo()

    # Logs in and sends E-Mail.
        server.login(esend, epwrd)
        server.sendmail(esend, erecv, txt)
        sccs = "e-mail sent successfully"
        return sccs
    except:
        emsg = f"ERROR: {sys.exc_info()}"
        return emsg


    # Import discord.py library.
from discord.ext import commands
class eml(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command()
    async def mail(self, ctx):
    #    async def ask(ctx):
    #        def pred(m):
    #            return m.author == ctx.author and m.channel == ctx.channel
    #        ans = await ctx.wait_for('message', check=pred)
    #        ans = ans.clean_content
    #        return ans
        async def askfunc(self, ctx, cont):
            await ctx.channel.send(cont)
            def pred(m):
                return m.author == ctx.author and m.channel == ctx.channel
            ans = await self.bot.wait_for('message', check=pred)
            ans = ans.clean_content
            return ans
        esmtp = await askfunc(self, ctx, 'SMTP:')
        esend = await askfunc(self, ctx, 'Sender e-mail:')
        erecv = await askfunc(self, ctx, 'Receiver e-mail:')
        esubj = await askfunc(self, ctx, 'Subject:')
        epwrd = await askfunc(self, ctx, 'Password:')
        ebody = await askfunc(self, ctx, 'e-mail body:')
        eport = await askfunc(self, ctx, 'e-mail port')
        ertrn = await send_email(esmtp, esend, erecv, esubj, epwrd, ebody, eport)
        await ctx.channel.send(ertrn)

def setup(bot):
    bot.add_cog(eml(bot))