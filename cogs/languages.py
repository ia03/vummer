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

    async def code_command(self, ctx, arg, lang_id):
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

        if ctx.message.attachments:
            attachment = await ctx.message.attachments[0].read()
        else:
            attachment = None

        thread = Thread(target=run_code, args=(arg[1:],
            message_id, channel_id, input_data, attachment, lang_id))
        thread.start()

    @commands.command(rest_is_raw=True)
    async def py(self, ctx, *, arg):
        """Runs Python (3.8.1) code.
        Usage: $py (code)
        """
        await self.code_command(ctx, arg, 71)

    @commands.command(rest_is_raw=True)
    async def py2(self, ctx, *, arg):
        """Runs Python (2.7.17) code.
        Usage: $py2 (code)
        """
        await self.code_command(ctx, arg, 70)

    @commands.command(rest_is_raw=True)
    async def cpp(self, ctx, *, arg):
        """Runs C++ (GCC 9.2.0) code.
        Usage: $cpp (code)
        """
        await self.code_command(ctx, arg, 54)

    @commands.command(rest_is_raw=True)
    async def c(self, ctx, *, arg):
        """Runs C (GCC 9.2.0) code.
        Usage: $c (code)
        """
        await self.code_command(ctx, arg, 50)

    @commands.command(rest_is_raw=True)
    async def cs(self, ctx, *, arg):
        """Runs C# (Mono 6.6.0.161) code.
        Usage: $cs (code)
        """
        await self.code_command(ctx, arg, 51)

    @commands.command(rest_is_raw=True)
    async def oc(self, ctx, *, arg):
        """Runs Objective C (Clang 7.0.1) code.
        Usage: $oc (code)
        """
        await self.code_command(ctx, arg, 79)

    @commands.command(rest_is_raw=True)
    async def java(self, ctx, *, arg):
        """Runs Java (OpenJDK 13.0.1) code.
        Usage: $java (code)
        """
        await self.code_command(ctx, arg, 62)

    @commands.command(rest_is_raw=True)
    async def js(self, ctx, *, arg):
        """Runs JavaScript (Node.js 12.14.0) code.
        Usage: $js (code)
        """
        await self.code_command(ctx, arg, 63)

    @commands.command(rest_is_raw=True)
    async def sql(self, ctx, *, arg):
        """Runs SQL (SQLite 3.27.2) code.
        Usage: $sql (code)
        """
        await self.code_command(ctx, arg, 82)

    @commands.command(rest_is_raw=True)
    async def vb(self, ctx, *, arg):
        """Runs Visual Basic .NET (vbnc 0.0.0.5943) code.
        Usage: $vb (code)
        """
        await self.code_command(ctx, arg, 84)

    @commands.command(rest_is_raw=True)
    async def octave(self, ctx, *, arg):
        """Runs Octave (5.1.0) code.
        Usage: $octave (code)
        """
        await self.code_command(ctx, arg, 66)

    @commands.command(rest_is_raw=True)
    async def clisp(self, ctx, *, arg):
        """Runs Common LISP (SBCL 2.0.0) code.
        Usage: $clisp (code)
        """
        await self.code_command(ctx, arg, 55)

    @commands.command(rest_is_raw=True)
    async def ass(self, ctx, *, arg):
        """Runs Assembly (NASM 2.14.02) code.
        Usage: $ass (code)
        """
        await self.code_command(ctx, arg, 45)

    @commands.command(rest_is_raw=True)
    async def bash(self, ctx, *, arg):
        """Runs Bash (5.0.0) code.
        Usage: $bash (code)
        """
        await self.code_command(ctx, arg, 46)

    @commands.command(rest_is_raw=True)
    async def php(self, ctx, *, arg):
        """Runs PHP (7.4.1) code.
        Usage: $php (code)
        """
        await self.code_command(ctx, arg, 68)

    @commands.command(rest_is_raw=True)
    async def lua(self, ctx, *, arg):
        """Runs Lua (5.3.5) code.
        Usage: $lua (code)
        """
        await self.code_command(ctx, arg, 64)

    @commands.command(rest_is_raw=True)
    async def pascal(self, ctx, *, arg):
        """Runs Pascal (FPC 3.0.4) code.
        Usage: $pascal (code)
        """
        await self.code_command(ctx, arg, 67)

    @commands.command(rest_is_raw=True)
    async def scala(self, ctx, *, arg):
        """Runs Scala (2.13.2) code.
        Usage: $scala (code)
        """
        await self.code_command(ctx, arg, 81)


    @commands.command(rest_is_raw=True)
    async def swift(self, ctx, *, arg):
        """Runs Swift (5.2.3) code.
        Usage: $swift (code)
        """
        await self.code_command(ctx, arg, 83)

    @commands.command(rest_is_raw=True)
    async def rust(self, ctx, *, arg):
        """Runs Rust (1.40.0) code.
        Usage: $rust (code)
        """
        await self.code_command(ctx, arg, 73)

    @commands.command(rest_is_raw=True)
    async def go(self, ctx, *, arg):
        """Runs Go (1.13.5) code.
        Usage: $go (code)
        """
        await self.code_command(ctx, arg, 60)

    @commands.command(rest_is_raw=True)
    async def ts(self, ctx, *, arg):
        """Runs TypeScript (3.7.4) code.
        Usage: $ts (code)
        """
        await self.code_command(ctx, arg, 74)

    @commands.command(rest_is_raw=True)
    async def kotlin(self, ctx, *, arg):
        """Runs Kotlin (1.3.70) code.
        Usage: $kotlin (code)
        """
        await self.code_command(ctx, arg, 78)

    @commands.command(rest_is_raw=True)
    async def rb(self, ctx, *, arg):
        """Runs Ruby (2.7.0) code.
        Usage: $rb (code)
        """
        await self.code_command(ctx, arg, 72)

    @commands.command(rest_is_raw=True)
    async def haskell(self, ctx, *, arg):
        """Runs Haskell (GHC 8.8.1) code.
        Usage: $haskell (code)
        """
        await self.code_command(ctx, arg, 61)

    @commands.command(rest_is_raw=True)
    async def basic(self, ctx, *, arg):
        """Runs Basic (FBC 1.07.1) code.
        Usage: $basic (code)
        """
        await self.code_command(ctx, arg, 47)

    @commands.command(rest_is_raw=True)
    async def fortran(self, ctx, *, arg):
        """Runs Fortran (GFortran 9.2.0) code.
        Usage: $fortran (code)
        """
        await self.code_command(ctx, arg, 59)

    @commands.command(rest_is_raw=True)
    async def r(self, ctx, *, arg):
        """Runs R (4.0.0) code.
        Usage: $r (code)
        """
        await self.code_command(ctx, arg, 80)

    @commands.command(rest_is_raw=True)
    async def erlang(self, ctx, *, arg):
        """Runs Erlang (OTP 22.2) code.
        Usage: $erlang (code)
        """
        await self.code_command(ctx, arg, 58)

    @commands.command(rest_is_raw=True)
    async def cobol(self, ctx, *, arg):
        """Runs COBOL (GnuCOBOL 2.2) code.
        Usage: $cobol (code)
        """
        await self.code_command(ctx, arg, 77)

    @commands.command(rest_is_raw=True)
    async def d(self, ctx, *, arg):
        """Runs D (DMD 2.089.1) code.
        Usage: $d (code)
        """
        await self.code_command(ctx, arg, 56)

    @commands.command(rest_is_raw=True)
    async def elixir(self, ctx, *, arg):
        """Runs Elixir (1.9.4) code.
        Usage: $elixir (code)
        """
        await self.code_command(ctx, arg, 57)

    @commands.command(rest_is_raw=True)
    async def ocaml(self, ctx, *, arg):
        """Runs OCaml (4.09.0) code.
        Usage: $ocaml (code)
        """
        await self.code_command(ctx, arg, 65)

    @commands.command(rest_is_raw=True)
    async def text(self, ctx, *, arg):
        """Displays plain text.
        Usage: $text (code)
        """
        await self.code_command(ctx, arg, 43)
