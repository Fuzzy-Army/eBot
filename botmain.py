# Import discord.py and json libraries.
import json
from discord.ext import commands
import modules.dbmod.dbmain

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

# Open json data file and fetch token within it.
with open('conf.json') as json_file:
    data        = json.load(json_file)
    token       = data['token']
    dPfx    = data['dPfx']

#async def prefix(bot, message):
#    guild = message.guild
#    if guild:
#        return customprefixes.get(guild.id, dPfx)

# initialize bot instance
bot = commands.Bot(command_prefix='e.', case_insensitive=True)

# log to console when bot logs into discord api
@bot.event
async def on_ready():
    """ Print when bot logs in successfully. """
    print(f'Logged in @ {bot.user.name}')

bot.load_extension('modules.emailmod.emailmod')
bot.run(token)






