# Import discord.py and json libraries.
from discord.ext import commands
import json

# Open json data file and fetch token within it.
with open('conf.json') as json_file:
    data    = json.load(json_file)
    token   = data['token']

# initialize bot instance
bot = commands.Bot(command_prefix='e.')
# log to console when bot logs into discord api
@bot.event
async def on_ready():
    print(f'Logged in @ {bot.user.name}')

# load cogs/emailsend.py cog
bot.load_extension('cogs.emailsend')
# initialize the bot
bot.run(token)