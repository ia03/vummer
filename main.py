#!/usr/bin/env python3
import config
import discord
import re
from discord.ext import commands, tasks
from sandbox import sandbox_python, stop_and_destroy, setup_base
from multiprocessing import Process, Queue
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
    if results['output']:
        print_queue.put((channel_id, 'Output: ```\n' + results['output']
            + '\n```'))
    else:
        print_queue.put((channel_id, 'No output sent.'))
    if results['errors'] != '':
        print_queue.put((channel_id,
            'Errors: ```\n' + results['errors'] + '\n```'))
    stop_and_destroy(message_id)
    print('Container destroyed. Ending process.')

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
    print('Setting input:', args)
    if '```' in args:
        data = search_between(args, '```', '```')
    else:
        data = args
    inputs[str(ctx.message.author.id)] = data
    await ctx.send('Input set.')

@tasks.loop(seconds=0.05)
async def check_print_queue():
    print('t')
    try:
        data = print_queue.get(False)
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
    bot.run(config.token)

if __name__ == '__main__':
    main()
