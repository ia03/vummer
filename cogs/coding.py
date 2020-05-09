from discord.ext import commands
from sandbox import sandbox_python, stop_and_destroy
from print_queue import send_message
from multiprocessing import Process
from utils import search_between

inputs = {}

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

class Coding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def py(self, ctx):
        """Runs Python code. Accepts codeblocks and regular text. There is a
        time limit of 2 seconds.
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

    @commands.command()
    async def setinput(self, ctx):
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
