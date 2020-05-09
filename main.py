#!/usr/bin/env python3
import config
import discord
import re
from discord.ext import commands, tasks
from sandbox import sandbox_python, stop_and_destroy, setup_base
from multiprocessing import Process
from utils import search_between
from print_queue import send_message, pop_message

bot = commands.Bot(command_prefix='$')


inputs = {}

@bot.event
async def on_ready():
    print('Bot is ready.')



def py_process(args, message_id, channel_id, input_data):
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
        send_message(channel_id, 'Output: ```\n' + results['output']
            + '\n```')
    else:
        send_message(channel_id, 'No output sent.')
    if results['errors'] != '':
        send_message(channel_id,
            'Errors: ```\n' + results['errors'] + '\n```')
    stop_and_destroy(message_id)
    print('Container destroyed. Ending process.')

@bot.command()
async def py(ctx):
    """Runs Python code. Accepts codeblocks and regular text.
    Usage: $py (code)
    """
    input_key = str(ctx.message.author.id)
    if input_key in inputs:
        input_data = inputs[input_key]
    else:
        input_data = ''
    process = Process(target=py_process, args=(ctx.message.content[4:],
        str(ctx.message.id), ctx.message.channel.id, input_data))
    process.start()

@bot.command()
async def setinput(ctx):
    """Sets the input that is to be passed to Python code you run.
    Usage: $setinput (input)
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
    bot.run(config.token)

if __name__ == '__main__':
    main()
