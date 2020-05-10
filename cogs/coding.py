from discord.ext import commands
from print_queue import send_message
from threading import Thread
from utils import (search_between, LimitedSizeDict, get_log_filename,
    get_code)
import datetime
import aiofiles
import judge0api as api

inputs = LimitedSizeDict(size_limit=1000)

client = api.Client("http://127.0.0.1")


def run_code(args, message_id, channel_id, input_data, lang_id):
    code = get_code(args)
    print('Running code: ', code)
    log_filename = get_log_filename(message_id)
    with open(log_filename, 'a') as log_file:
        log_file.write('Code: ' + code + '\n')
        log_file.write('Input: ' + input_data + '\n')
    submission = api.submission.submit(client, code.encode(), lang_id,
        stdin=input_data.encode())
    output = submission.stdout
    errors = submission.stderr
    if output:
        output = output.decode()
    if errors:
        errors = errors.decode()
    if output:
        send_message(channel_id, 'Output: ```\n' + output
            + '\n```')
    else:
        send_message(channel_id, 'No output sent.')
    if errors:
        send_message(channel_id,
            'Errors: ```\n' + errors + '\n```')

class Coding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def code_command(self, ctx, lang_id):
        author_id = str(ctx.message.author.id)
        if author_id in inputs:
            input_data = inputs[author_id]
        else:
            input_data = ''
        message_id = str(ctx.message.id)
        channel_id = ctx.message.channel.id
        async with aiofiles.open(get_log_filename(message_id), 'a') as log_file:
            await log_file.write(str(datetime.datetime.now()) + '\n')
            await log_file.write(author_id + ' ' + message_id + ' '
                + str(channel_id) + '\n')

        thread = Thread(target=run_code, args=(ctx.message.content[4:],
            message_id, channel_id, input_data, lang_id))
        thread.start()

    @commands.command()
    async def py(self, ctx):
        """Runs Python code. Accepts codeblocks and regular text.
        Usage: $py (code)
        """
        await self.code_command(ctx, 71)

    @commands.command()
    async def cpp(self, ctx):
        """Runs C++ code. Accepts codeblocks and regular text.
        Usage: $cpp (code)
        """
        await self.code_command(ctx, 53)

    @commands.command()
    async def setinput(self, ctx):
        """Sets the input that is to be passed to Python code you run. Using
        the command without an argument clears the input.
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
