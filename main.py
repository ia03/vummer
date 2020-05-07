#!/usr/bin/env python
import config
import discord
import re
from discord.ext import commands
from sandbox import sandbox_python

bot = commands.Bot(command_prefix='$')


@bot.command()
async def py(ctx):
    args = ctx.message.content[3:]
    start = '```py'
    end = '```'
    code = args[args.find(start)+len(start):args.rfind(end)]
    def run_code():
        exec(code)

    await ctx.send(sandbox_python(code))



bot.run(config.token)
