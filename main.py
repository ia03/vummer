#!/usr/bin/env python3
import config
import discord
import re
from discord.ext import commands, tasks
from sandbox import setup_base
from print_queue import pop_message
from cogs.coding import Coding
from discord import Game

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('Bot is ready.')
    await bot.change_presence(activity=Game(name='with Python (try $help)'))

@tasks.loop(seconds=0.05)
async def check_print_queue():
    try:
        data = pop_message()
    except:
        return
    channel_id = data[0]
    message = data[1]
    print('New message to channel', str(channel_id) + ':', str(message))
    if len(message) > 2000:
        await bot.get_channel(channel_id).send(
        '[This message is too large.]')
        return
    try:
        await bot.get_channel(channel_id).send(message)
    except:
        pass

def main():
    setup_base()
    check_print_queue.start()
    bot.add_cog(Coding(bot))
    bot.run(config.token)

if __name__ == '__main__':
    main()
