from discord.ext import commands

class main:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)

    # log to console what user signed into
    async def on_ready(self):
        print(f'Logged on as {self.bot.user}')

    async def on_message(self, message):

        # Print messages seen by bot
        print(f'Message from {message.author}: {message.content}')

        # check if user is bot

