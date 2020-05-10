#!/usr/bin/env python3
import config
import discord
import re
from discord.ext import commands, tasks
from print_queue import pop_message
from cogs.languages import Languages
from discord import Game
from discord.utils import escape_mentions
from inputs import inputs

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('Bot is ready.')
    await bot.change_presence(activity=Game(name='with code (try $help)'))

@tasks.loop(seconds=0.05)
async def check_print_queue():
    try:
        data = pop_message()
    except:
        return
    channel_id = data[0]
    message = escape_mentions(data[1])
    if len(message) > 2000:
        await bot.get_channel(channel_id).send(
        '[This message is too large.]')
        return
    try:
        await bot.get_channel(channel_id).send(message)
    except:
        pass

@bot.command()
async def setinput(ctx):
    """Sets the input that is to be passed to code you run.
    You can set multiple lines of input.
    Using the command without an argument clears the input.
    Usage: $setinput [input]
    """
    args = ctx.message.content[10:]
    print('Setting input:', args)
    if '```' in args:
        data = search_between(args, '```', '```')
    else:
        data = args
    inputs[str(ctx.message.author.id)] = data
    if data:
        message = 'Input set: ```\n' + data + '\n```'
        await ctx.send(message)
    else:
        await ctx.send('Input cleared.')

def main():
    check_print_queue.start()
    bot.add_cog(Languages(bot))
    bot.run(config.token)

if __name__ == '__main__':
    main()
