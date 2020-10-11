# Objective 1: Make bot modular.
# Objective 2: add more objectives, feel free to do so.
# Objective 3: get database up and running

import discord
from discord.ext import commands
from emailsend import send_email
import json

with open('conf.json') as json_file:
    data    = json.load(json_file)
    dPfx    = data['dPfx']
    token   = data['token']

class main(discord.Client):

    # log to console what user signed into
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):

        # Print messages seen by bot
        print(f'Message from {message.author}: {message.content}')

        # check if user is bot
        if message.author == commands.Bot.user or message.author.bot: # we don't want to have bots automating stuff
            return
        
        # store message as variable and chop off prefix
        msgpfx = message.content[:2]

        # check for prefix and command
        if msgpfx == dPfx:
            msgcmd = message.content[2:]
            if "mail" in msgcmd:
                def pred(m):
                    return m.author == message.author and m.channel == message.channel
                await message.channel.send('SMTP:')
                smtp = await client.wait_for('message', check=pred)
                esmtp = smtp.clean_content
                await message.channel.send('Sender email:')
                send = await client.wait_for('message', check=pred)
                esend = send.clean_content
                await message.channel.send('receiver email:')
                recv = await client.wait_for('message', check=pred)
                erecv = recv.clean_content
                await message.channel.send('subject:')
                subj = await client.wait_for('message', check=pred)
                esubj = subj.clean_content
                await message.channel.send('email password:')
                pwrd = await client.wait_for('message', check=pred)
                epwrd = pwrd.clean_content
                await message.channel.send('email body:')
                body = await client.wait_for('message', check=pred)
                ebody = body.clean_content
                await message.channel.send('eport:')
                port = await client.wait_for('message', check=pred)
                eport = port.clean_content
                send_email(esmtp, esend, erecv, esubj, epwrd, ebody, eport)


client = main()
client.run(token)

