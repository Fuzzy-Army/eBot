# Import libs required for send_email function.
import ssl
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Function in charge of sending E-Mail.
def send_email(esmtp: str, esend: str, erecv: str, esubj: str, epwrd: str, ebody: str, eport) -> None:

    # Encodes Message.
    msg = MIMEMultipart()
    msg['From']     = esend
    msg['To']       = erecv
    msg['Subject']  = esubj
    msg.attach(MIMEText(ebody, 'plain'))
    txt = msg.as_string()

    # Creates SMTP session and starts TLS.
    server = smtplib.SMTP(esmtp, eport)
    server.starttls()
    server.ehlo()

    # Logs in and sends E-Mail.
    server.login(esend, epwrd)
    server.sendmail(esend, erecv, txt)


from discord.ext import commands

class mail_cmd(commands.Cog):

    @commands.command()
    async def mail(self, ctx):
        async def ask(self, ctx):
            def pred(m):
                return m.author == ctx.author and m.channel == ctx.channel
            ans = await ctx.wait_for('message', check=pred)
            ans = ans.clean_content
            return ans
        await ctx.channel.send('SMTP:')
        esmtp = ask(self, ctx)
        await ctx.channel.send('Sender email:')
        esend = ask(self, ctx)
        await ctx.channel.send('receiver email:')
        erecv = ask(self, ctx)
        await ctx.channel.send('subject:')
        esubj = ask(self, ctx)
        await ctx.channel.send('email password:')
        epwrd = ask(self, ctx)
        await ctx.channel.send('email body:')
        ebody = ask(self, ctx)
        await ctx.channel.send('eport:')
        eport = ask(self, ctx)
        try:
            send_email(esmtp, esend, erecv, esubj, epwrd, ebody, eport)
        except ValueError:
            ctx.channel.send('Sorry! There was an unexpected error sending your E-Mail: {0}'.format(ValueError))
