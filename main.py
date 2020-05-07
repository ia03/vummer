#!/usr/bin/env python
import config
import discord
import re
from discord.ext import commands
from sandbox import sandbox_python, prepare_lxc

bot = commands.Bot(command_prefix='$')

IGNORED_ERROR = '''Traceback (most recent call last):
  File "/usr/lib/python3.8/logging/__init__.py", line 260, in _after_at_fork_child_reinit_locks
  File "/usr/lib/python3.8/logging/__init__.py", line 228, in _releaseLock
RuntimeError: cannot release un-acquired lock'''

@bot.event
async def on_ready():
    print('Bot is ready.')
    prepare_lxc()

@bot.command()
async def py(ctx):
    args = ctx.message.content[3:]
    start = '```py'
    end = '```'
    code = args[args.find(start)+len(start):args.rfind(end)]
    print('Running code: ', code)
    def run_code():
        exec(code)
    results = sandbox_python(code)
    await ctx.send('Output: ```' + results['output'] + '\n```')
    if results['errors'] != '' and IGNORED_ERROR not in results['errors']:
        await ctx.send('Errors: ```' + results['errors'] + '\n```')
    prepare_lxc()

bot.run(config.token)
