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
        args = ctx.message.content[ctx.message.content.find(' ') + 1:]
        thread = Thread(target=run_code, args=(args,
            message_id, channel_id, input_data, lang_id))
        thread.start()

    @commands.command()
    async def py(self, ctx):
        """Runs Python 3 code. Accepts codeblocks and regular text.
        Usage: $py (code)
        """
        await self.code_command(ctx, 71)

    @commands.command()
    async def py2(self, ctx):
        """Runs Python 2 code. Accepts codeblocks and regular text.
        Usage: $py2 (code)
        """
        await self.code_command(ctx, 70)

    @commands.command()
    async def cpp(self, ctx):
        """Runs C++ code. Accepts codeblocks and regular text.
        Usage: $cpp (code)
        """
        await self.code_command(ctx, 54)

    @commands.command()
    async def c(self, ctx):
        """Runs C code. Accepts codeblocks and regular text.
        Usage: $c (code)
        """
        await self.code_command(ctx, 50)

    @commands.command()
    async def cs(self, ctx):
        """Runs C# code. Accepts codeblocks and regular text.
        Usage: $cs (code)
        """
        await self.code_command(ctx, 51)

    @commands.command()
    async def oc(self, ctx):
        """Runs Objective C code. Accepts codeblocks and regular text.
        Usage: $oc (code)
        """
        await self.code_command(ctx, 79)

    @commands.command()
    async def java(self, ctx):
        """Runs Java code. Accepts codeblocks and regular text.
        Usage: $java (code)
        """
        await self.code_command(ctx, 62)

    @commands.command()
    async def js(self, ctx):
        """Runs Javascript code. Accepts codeblocks and regular text.
        Usage: $js (code)
        """
        await self.code_command(ctx, 63)

    @commands.command()
    async def sql(self, ctx):
        """Runs SQL code. Accepts codeblocks and regular text.
        Usage: $sql (code)
        """
        await self.code_command(ctx, 82)

    @commands.command()
    async def vb(self, ctx):
        """Runs Visual Basic .NET code. Accepts codeblocks and regular text.
        Usage: $vb (code)
        """
        await self.code_command(ctx, 84)

    @commands.command()
    async def octave(self, ctx):
        """Runs Octave code. Accepts codeblocks and regular text.
        Usage: $octave (code)
        """
        await self.code_command(ctx, 66)

    @commands.command()
    async def clisp(self, ctx):
        """Runs Common LISP code. Accepts codeblocks and regular text.
        Usage: $clisp (code)
        """
        await self.code_command(ctx, 55)

    @commands.command()
    async def as(self, ctx):
        """Runs Assembly code. Accepts codeblocks and regular text.
        Usage: $as (code)
        """
        await self.code_command(ctx, 45)

    @commands.command()
    async def bash(self, ctx):
        """Runs Bash code. Accepts codeblocks and regular text.
        Usage: $bash (code)
        """
        await self.code_command(ctx, 46)

    @commands.command()
    async def PHP(self, ctx):
        """Runs PHP code. Accepts codeblocks and regular text.
        Usage: $php (code)
        """
        await self.code_command(ctx, 68)

    @commands.command()
    async def lua(self, ctx):
        """Runs Lua code. Accepts codeblocks and regular text.
        Usage: $lua (code)
        """
        await self.code_command(ctx, 64)

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
