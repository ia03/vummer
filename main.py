#!/usr/bin/env python
import config
import discord
import re
from discord.ext import commands
from sandbox import sandbox_python, stop_and_destroy
from multiprocessing import Process, Queue
import asyncio

bot = commands.Bot(command_prefix='$')
print_queue = Queue()

@bot.event
async def on_ready():
    print('Bot is ready.')


def py_process(args, message_id, channel_id, print_queue):
    if '```py' in message_content:
        code = search_between(args, '```py', '```')
    elif '```' in message_content:
        code = search_between(args, '```', '```')
    else:
        code = message_content
    print('Running code: ', code)

    results = sandbox_python(code, message_id)
    print_queue.put((channel_id, 'Output: ```' + results['output'] + '\n```'))
    if results['errors'] != '':
        print_queue.put((channel_id,
            'Errors: ```' + results['errors'] + '\n```'))
    stop_and_destroy(message_id)

@bot.command()
async def py(ctx):
    process = Process(target=py_process, args=(ctx.message.content[4:],
        str(ctx.message.id), ctx.message.channel.id, print_queue))
    process.start()


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
        await bot.get_channel(channel_id).send(message)
bot.loop.create_task(check_print_queue())
bot.run(config.token)
