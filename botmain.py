# Import discord.py and json libraries.
import json
from discord.ext import commands
from importlib import import_module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import modules.dbmod.base as base

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
bot.load_extension('modules.emailsend')

###################################

#dbengine = create_engine('postgresql://dev-wolf:cute-dev-wolf@localhost:62100/uwu', echo=True)

#base.Base.metadata.create_all(dbengine, checkfirst=True)
import modules.dbmod.dbmain
#session_init = sessionmaker(bind=dbengine)
#ormsession = session_init()

###################################

bot.run(token)






