#   OBJECTIVES:
#   - nom on pizza uwu <--- not bloat <-- hloat
#   - Make email function actually work. Something about the encoding makes it fail <--- :bloat:


# Import discord.py and json libraries.
from discord.ext import commands
import json

# Open json data file and fetch token within it.
with open('conf.json') as json_file:
    data    = json.load(json_file)
    token   = data['token']

bot = commands.Bot(command_prefix='e.')

@bot.event
async def on_ready():
    print(f'Logged in @ {bot.user.name}')


bot.load_extension('cogs.emailsend')
bot.run(token)