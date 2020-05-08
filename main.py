#!/usr/bin/env python
import config
import discord
import re
from discord.ext import commands
from sandbox import sandbox_python, stop_and_destroy
from multiprocessing import Process, Queue
import asyncio
from utils import search_between

bot = commands.Bot(command_prefix='$')
print_queue = Queue()

inputs = {}

@bot.event
async def on_ready():
    print('Bot is ready.')


def py_process(args, message_id, channel_id, input_data, print_queue):
    if '```python' in args:
        code = search_between(args, '```python', '```')
    elif '```py' in args:
        code = search_between(args, '```py', '```')
    elif '```' in args:
        code = search_between(args, '```', '```')
    else:
        code = args
    print('Running code: ', code)

    results = sandbox_python(code, message_id, input_data)
    print_queue.put((channel_id, 'Output: ```' + results['output'] + '\n```'))
    if results['errors'] != '':
        print_queue.put((channel_id,
            'Errors: ```' + results['errors'] + '\n```'))
    stop_and_destroy(message_id)

@bot.command()
async def py(ctx):
    input_key = str(ctx.message.author.id)
    if input_key in inputs:
        input_data = inputs[input_key]
    else:
        input_data = ''
    process = Process(target=py_process, args=(ctx.message.content[4:],
        str(ctx.message.id), ctx.message.channel.id, input_data, print_queue))
    process.start()

@bot.command()
async def input(ctx):
    args = ctx.message.content[7:]
    if '```' in args:
        data = search_between(args, '```', '```')
    else:
        data = args
    inputs[str(ctx.message.author.id)] = data
    await ctx.send('Input set.')

async def check_print_queue():
    while True:
        await asyncio.sleep(0.05)
        try:
            data = print_queue.get(False)
        except:
            continue
        channel_id = data[0]
        message = data[1]
        print('New message to channel', str(channel_id) + ':', str(data))
        if len(message) > 2000:
            await bot.get_channel(channel_id).send(
            '[This message is too large.]')
            continue
        try:
            await bot.get_channel(channel_id).send(message)
        except:
            pass
bot.loop.create_task(check_print_queue())
bot.run(config.token)
