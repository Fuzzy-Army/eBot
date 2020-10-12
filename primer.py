# Import discord.py and json libraries.
from discord.ext import commands
import json

# Open json data file and fetch token within it.
with open('conf.json') as json_file:
    data    = json.load(json_file)
    token   = data['token']

# Initialize bot instance and load main cog.
bot = commands.Bot(command_prefix='e.')
bot.load_extension("cogs.main")
bot.run(token)