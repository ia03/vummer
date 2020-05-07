#!/usr/bin/env python
import config
import discord
import re
from discord.ext import commands
from sandbox import sandbox_python, prepare_lxc

bot = commands.Bot(command_prefix='$')


@bot.command()
async def py(ctx):
    args = ctx.message.content[3:]
    start = '```py'
    end = '```'
    code = args[args.find(start)+len(start):args.rfind(end)]
    def run_code():
        exec(code)
    results = sandbox_python(code)
    await ctx.send('Output: ```' + results['output'] + '\n```')
    if results['errors']:
        await ctx.send('Errors: ```' + results['errors'] + '\n```')
    prepare_lxc()

bot.run(config.token)
