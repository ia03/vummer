#!/usr/bin/env python3
import config
import discord
import re
from discord.ext import commands, tasks
from print_queue import pop_message
from cogs.languages import Languages, set_input
from cogs.problems import Problems, read_problems
from utils import search_between
from discord import Game
from discord.utils import escape_mentions, oauth_url

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
async def setinput(ctx, *, stdin):
    """Sets the input that is to be passed to code you run.
    You can set multiple lines of input.
    Using the command without an argument clears the input.
    """
    print('Setting input:', stdin)
    if '```' in stdin:
        data = search_between(stdin, '```', '```')
    else:
        data = stdin
    set_input(ctx.author.id, data)
    if data:
        message = 'Input set: ```\n' + data + '\n```'
        await ctx.send(message)
    else:
        await ctx.send('Input cleared.')

@bot.command()
async def invite(ctx):
    """Sends the bot invite link."""
    await ctx.send(oauth_url(bot.user.id))

@bot.command()
@commands.is_owner()
async def guilds(ctx):
    """Lists the guilds the bot is in. Only available to the bot owner."""
    message = 'Guilds the bot is in:```\n'
    for guild in bot.guilds:
        message += guild.name + '\n'
    message += '```'
    await ctx.send(message)

def main():
    check_print_queue.start()
    read_problems()
    bot.add_cog(Languages(bot))
    bot.add_cog(Problems(bot))
    bot.run(config.token)

if __name__ == '__main__':
    main()
