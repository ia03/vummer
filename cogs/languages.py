from discord.ext import commands
from print_queue import send_message
from threading import Thread
from utils import (search_between, get_log_filename, get_code)
import datetime
import aiofiles
import judge0api as api
from inputs import inputs

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
    status = submission.status
    output = submission.stdout
    errors = submission.stderr
    compile_output = submission.compile_output
    if output:
        output = output.decode()
    if errors:
        errors = errors.decode()
    if compile_output:
        compile_output = compile_output.decode()
    send_message(channel_id, 'Status: ' + status['description'])

    if output:
        send_message(channel_id, 'Output: ```\n' + output
            + '\n```')
    else:
        send_message(channel_id, 'No output sent.')
    if errors:
        send_message(channel_id,
            'Errors: ```\n' + errors + '\n```')
    if compile_output:
        send_message(channel_id, 'Compiler output: ```\n' + compile_output
            + '\n```')

class Languages(commands.Cog):
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
        first_space = ctx.message.content.find(' ')
        first_newline = ctx.message.content.find('\n', 2)
        if first_space > 0 and first_newline > 0:
            start_index = min(first_space, first_newline)
        elif first_space > 0:
            start_index = first_space
        elif first_newline > 0:
            start_index = first_newline
        else:
            await ctx.send('No code was provided.')
            return

        args = ctx.message.content[start_index + 1:]

        thread = Thread(target=run_code, args=(args,
            message_id, channel_id, input_data, lang_id))
        thread.start()

    @commands.command()
    async def py(self, ctx):
        """Runs Python (3.8.1) code.
        Usage: $py (code)
        """
        await self.code_command(ctx, 71)

    @commands.command()
    async def py2(self, ctx):
        """Runs Python (2.7.17) code.
        Usage: $py2 (code)
        """
        await self.code_command(ctx, 70)

    @commands.command()
    async def cpp(self, ctx):
        """Runs C++ (GCC 9.2.0) code.
        Usage: $cpp (code)
        """
        await self.code_command(ctx, 54)

    @commands.command()
    async def c(self, ctx):
        """Runs C (GCC 9.2.0) code.
        Usage: $c (code)
        """
        await self.code_command(ctx, 50)

    @commands.command()
    async def cs(self, ctx):
        """Runs C# (Mono 6.6.0.161) code.
        Usage: $cs (code)
        """
        await self.code_command(ctx, 51)

    @commands.command()
    async def oc(self, ctx):
        """Runs Objective C (Clang 7.0.1) code.
        Usage: $oc (code)
        """
        await self.code_command(ctx, 79)

    @commands.command()
    async def java(self, ctx):
        """Runs Java (OpenJDK 13.0.1) code.
        Usage: $java (code)
        """
        await self.code_command(ctx, 62)

    @commands.command()
    async def js(self, ctx):
        """Runs JavaScript (Node.js 12.14.0) code.
        Usage: $js (code)
        """
        await self.code_command(ctx, 63)

    @commands.command()
    async def sql(self, ctx):
        """Runs SQL (SQLite 3.27.2) code.
        Usage: $sql (code)
        """
        await self.code_command(ctx, 82)

    @commands.command()
    async def vb(self, ctx):
        """Runs Visual Basic .NET (vbnc 0.0.0.5943) code.
        Usage: $vb (code)
        """
        await self.code_command(ctx, 84)

    @commands.command()
    async def octave(self, ctx):
        """Runs Octave (5.1.0) code.
        Usage: $octave (code)
        """
        await self.code_command(ctx, 66)

    @commands.command()
    async def clisp(self, ctx):
        """Runs Common LISP (SBCL 2.0.0) code.
        Usage: $clisp (code)
        """
        await self.code_command(ctx, 55)

    @commands.command()
    async def ass(self, ctx):
        """Runs Assembly (NASM 2.14.02) code.
        Usage: $ass (code)
        """
        await self.code_command(ctx, 45)

    @commands.command()
    async def bash(self, ctx):
        """Runs Bash (5.0.0) code.
        Usage: $bash (code)
        """
        await self.code_command(ctx, 46)

    @commands.command()
    async def php(self, ctx):
        """Runs PHP (7.4.1) code.
        Usage: $php (code)
        """
        await self.code_command(ctx, 68)

    @commands.command()
    async def lua(self, ctx):
        """Runs Lua (5.3.5) code.
        Usage: $lua (code)
        """
        await self.code_command(ctx, 64)

    @commands.command()
    async def pascal(self, ctx):
        """Runs Pascal (FPC 3.0.4) code.
        Usage: $pascal (code)
        """
        await self.code_command(ctx, 67)

    @commands.command()
    async def scala(self, ctx):
        """Runs Scala (2.13.2) code.
        Usage: $scala (code)
        """
        await self.code_command(ctx, 81)

    @commands.command()
    async def swift(self, ctx):
        """Runs Swift (5.2.3) code.
        Usage: $swift (code)
        """
        await self.code_command(ctx, 83)

    @commands.command()
    async def rust(self, ctx):
        """Runs Rust (1.40.0) code.
        Usage: $rust (code)
        """
        await self.code_command(ctx, 73)

    @commands.command()
    async def go(self, ctx):
        """Runs Go (1.13.5) code.
        Usage: $go (code)
        """
        await self.code_command(ctx, 60)

    @commands.command()
    async def ts(self, ctx):
        """Runs TypeScript (3.7.4) code.
        Usage: $ts (code)
        """
        await self.code_command(ctx, 74)

    @commands.command()
    async def kotlin(self, ctx):
        """Runs Kotlin (1.3.70) code.
        Usage: $kotlin (code)
        """
        await self.code_command(ctx, 78)

    @commands.command()
    async def rb(self, ctx):
        """Runs Ruby (2.7.0) code.
        Usage: $rb (code)
        """
        await self.code_command(ctx, 72)

    @commands.command()
    async def haskell(self, ctx):
        """Runs Haskell (GHC 8.8.1) code.
        Usage: $haskell (code)
        """
        await self.code_command(ctx, 61)

    @commands.command()
    async def basic(self, ctx):
        """Runs Basic (FBC 1.07.1) code.
        Usage: $basic (code)
        """
        await self.code_command(ctx, 47)

    @commands.command()
    async def fortran(self, ctx):
        """Runs Fortran (GFortran 9.2.0) code.
        Usage: $fortran (code)
        """
        await self.code_command(ctx, 59)

    @commands.command()
    async def r(self, ctx):
        """Runs R (4.0.0) code.
        Usage: $r (code)
        """
        await self.code_command(ctx, 80)

    @commands.command()
    async def erlang(self, ctx):
        """Runs Erlang (OTP 22.2) code.
        Usage: $erlang (code)
        """
        await self.code_command(ctx, 58)

    @commands.command()
    async def cobol(self, ctx):
        """Runs COBOL (GnuCOBOL 2.2) code.
        Usage: $cobol (code)
        """
        await self.code_command(ctx, 77)

    @commands.command()
    async def d(self, ctx):
        """Runs D (DMD 2.089.1) code.
        Usage: $d (code)
        """
        await self.code_command(ctx, 56)
