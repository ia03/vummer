from discord.ext import commands
from print_queue import send_message
from threading import Thread
from utils import (search_between, get_log_filename, get_code)
import datetime
import aiofiles
import judge0api as api
from inputs import inputs

client = api.Client("http://127.0.0.1")


def run_code(args, message_id, channel_id, input_data, attachment, lang_id):
    if attachment:
        code = attachment
    else:
        code = get_code(args).encode()
    print('Running code: ', code.decode())
    log_filename = get_log_filename(message_id)
    with open(log_filename, 'a') as log_file:
        log_file.write('Code: ' + code.decode() + '\n')
        log_file.write('Input: ' + input_data + '\n')
    submission = api.submission.submit(client, code, lang_id,
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
    if submission.time and submission.memory:
        send_message(channel_id, 'CPU time: ' + str(submission.time) + ' s, '
            + 'Memory usage: ' + str(submission.memory) + ' kB')

class Languages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def code_command(self, ctx, args, lang_id):
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

        args = ' '.join(args)
        if ctx.message.attachments:
            attachment = await ctx.message.attachments[0].read()
        else:
            attachment = None

        thread = Thread(target=run_code, args=(args,
            message_id, channel_id, input_data, attachment, lang_id))
        thread.start()

    @commands.command()
    async def py(self, ctx, *args):
        """Runs Python (3.8.1) code.
        Usage: $py (code)
        """
        await self.code_command(ctx, args, 71)

    @commands.command()
    async def py2(self, ctx, *args):
        """Runs Python (2.7.17) code.
        Usage: $py2 (code)
        """
        await self.code_command(ctx, args, 70)

    @commands.command()
    async def cpp(self, ctx, *args):
        """Runs C++ (GCC 9.2.0) code.
        Usage: $cpp (code)
        """
        await self.code_command(ctx, args, 54)

    @commands.command()
    async def c(self, ctx, *args):
        """Runs C (GCC 9.2.0) code.
        Usage: $c (code)
        """
        await self.code_command(ctx, args, 50)

    @commands.command()
    async def cs(self, ctx, *args):
        """Runs C# (Mono 6.6.0.161) code.
        Usage: $cs (code)
        """
        await self.code_command(ctx, args, 51)

    @commands.command()
    async def oc(self, ctx, *args):
        """Runs Objective C (Clang 7.0.1) code.
        Usage: $oc (code)
        """
        await self.code_command(ctx, args, 79)

    @commands.command()
    async def java(self, ctx, *args):
        """Runs Java (OpenJDK 13.0.1) code.
        Usage: $java (code)
        """
        await self.code_command(ctx, args, 62)

    @commands.command()
    async def js(self, ctx, *args):
        """Runs JavaScript (Node.js 12.14.0) code.
        Usage: $js (code)
        """
        await self.code_command(ctx, args, 63)

    @commands.command()
    async def sql(self, ctx, *args):
        """Runs SQL (SQLite 3.27.2) code.
        Usage: $sql (code)
        """
        await self.code_command(ctx, args, 82)

    @commands.command()
    async def vb(self, ctx, *args):
        """Runs Visual Basic .NET (vbnc 0.0.0.5943) code.
        Usage: $vb (code)
        """
        await self.code_command(ctx, args, 84)

    @commands.command()
    async def octave(self, ctx, *args):
        """Runs Octave (5.1.0) code.
        Usage: $octave (code)
        """
        await self.code_command(ctx, args, 66)

    @commands.command()
    async def clisp(self, ctx, *args):
        """Runs Common LISP (SBCL 2.0.0) code.
        Usage: $clisp (code)
        """
        await self.code_command(ctx, args, 55)

    @commands.command()
    async def ass(self, ctx, *args):
        """Runs Assembly (NASM 2.14.02) code.
        Usage: $ass (code)
        """
        await self.code_command(ctx, args, 45)

    @commands.command()
    async def bash(self, ctx, *args):
        """Runs Bash (5.0.0) code.
        Usage: $bash (code)
        """
        await self.code_command(ctx, args, 46)

    @commands.command()
    async def php(self, ctx, *args):
        """Runs PHP (7.4.1) code.
        Usage: $php (code)
        """
        await self.code_command(ctx, args, 68)

    @commands.command()
    async def lua(self, ctx, *args):
        """Runs Lua (5.3.5) code.
        Usage: $lua (code)
        """
        await self.code_command(ctx, args, 64)

    @commands.command()
    async def pascal(self, ctx, *args):
        """Runs Pascal (FPC 3.0.4) code.
        Usage: $pascal (code)
        """
        await self.code_command(ctx, args, 67)

    @commands.command()
    async def scala(self, ctx, *args):
        """Runs Scala (2.13.2) code.
        Usage: $scala (code)
        """
        await self.code_command(ctx, args, 81)


    @commands.command()
    async def swift(self, ctx, *args):
        """Runs Swift (5.2.3) code.
        Usage: $swift (code)
        """
        await self.code_command(ctx, args, 83)

    @commands.command()
    async def rust(self, ctx, *args):
        """Runs Rust (1.40.0) code.
        Usage: $rust (code)
        """
        await self.code_command(ctx, args, 73)

    @commands.command()
    async def go(self, ctx, *args):
        """Runs Go (1.13.5) code.
        Usage: $go (code)
        """
        await self.code_command(ctx, args, 60)

    @commands.command()
    async def ts(self, ctx, *args):
        """Runs TypeScript (3.7.4) code.
        Usage: $ts (code)
        """
        await self.code_command(ctx, args, 74)

    @commands.command()
    async def kotlin(self, ctx, *args):
        """Runs Kotlin (1.3.70) code.
        Usage: $kotlin (code)
        """
        await self.code_command(ctx, args, 78)

    @commands.command()
    async def rb(self, ctx, *args):
        """Runs Ruby (2.7.0) code.
        Usage: $rb (code)
        """
        await self.code_command(ctx, args, 72)

    @commands.command()
    async def haskell(self, ctx, *args):
        """Runs Haskell (GHC 8.8.1) code.
        Usage: $haskell (code)
        """
        await self.code_command(ctx, args, 61)

    @commands.command()
    async def basic(self, ctx, *args):
        """Runs Basic (FBC 1.07.1) code.
        Usage: $basic (code)
        """
        await self.code_command(ctx, args, 47)

    @commands.command()
    async def fortran(self, ctx, *args):
        """Runs Fortran (GFortran 9.2.0) code.
        Usage: $fortran (code)
        """
        await self.code_command(ctx, args, 59)

    @commands.command()
    async def r(self, ctx, *args):
        """Runs R (4.0.0) code.
        Usage: $r (code)
        """
        await self.code_command(ctx, args, 80)

    @commands.command()
    async def erlang(self, ctx, *args):
        """Runs Erlang (OTP 22.2) code.
        Usage: $erlang (code)
        """
        await self.code_command(ctx, args, 58)

    @commands.command()
    async def cobol(self, ctx, *args):
        """Runs COBOL (GnuCOBOL 2.2) code.
        Usage: $cobol (code)
        """
        await self.code_command(ctx, args, 77)

    @commands.command()
    async def d(self, ctx, *args):
        """Runs D (DMD 2.089.1) code.
        Usage: $d (code)
        """
        await self.code_command(ctx, args, 56)

    @commands.command()
    async def elixir(self, ctx, *args):
        """Runs Elixir (1.9.4) code.
        Usage: $elixir (code)
        """
        await self.code_command(ctx, args, 57)

    @commands.command()
    async def ocaml(self, ctx, *args):
        """Runs OCaml (4.09.0) code.
        Usage: $ocaml (code)
        """
        await self.code_command(ctx, args, 65)

    @commands.command()
    async def text(self, ctx, *args):
        """Displays plain text.
        Usage: $text (code)
        """
        await self.code_command(ctx, args, 43)
