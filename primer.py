# Objective 1: Make bot modular.
# Objective 2: add more objectives, feel free to do so.
# Objective 3: get database up and running

import discord
from discord.ext import commands
import json

with open('conf.json') as json_file:
    data    = json.load(json_file)
    token   = data['token']

bot = commands.Bot(command_prefix='e.')

bot.load_extension("cogs.main")

bot.run(token)