async def askfunc(self, ctx, cont):
    """ Function to minimize code size, is in charge
    of sending messages, awaiting for the response
    and returning its value """

    await ctx.channel.send(cont)
    def pred(original):
        return original.author == ctx.author and original.channel == ctx.channel
    ans = await self.bot.wait_for('message', check=pred)
    ans = ans.clean_content
    cancel = False
    if ans.lower() == 'cancel':
        cancel = True
    return ans, cancel
