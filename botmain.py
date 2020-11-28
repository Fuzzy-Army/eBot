# Import discord.py and json libraries.
import json
from discord.ext import commands

# Open json data file and fetch token within it.
with open('conf.json') as json_file:
    data        = json.load(json_file)
    token       = data['token']


# initialize bot instance
bot = commands.Bot(command_prefix='e.')
# log to console when bot logs into discord api
@bot.event
async def on_ready():
    """ Print when bot logs in successfully. """
    print(f'Logged in @ {bot.user.name}')

# load cogs/emailsend.py cog
bot.load_extension('modules.emailmod.emailmod')

###################################

import modules.dbmod.dbmain

###################################

bot.run(token)






