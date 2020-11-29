# Import discord.py and json libraries.
import json
from discord.ext import commands

# Open json data file and fetch token within it.
with open('conf.json') as json_file:
    data        = json.load(json_file)
    token       = data['token']
    dPfx    = data['dPfx']

from modules.dbmod.dblist import UsrPrefs, Email, SrvPrefs

import modules.dbmod.dbmain

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

# load cogs/emailsend.py cog
bot.load_extension('modules.emailmod.emailmod')

###################################


###################################

bot.run(token)






