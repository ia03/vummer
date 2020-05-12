from discord.ext import commands
from problem import Problem
import jsons
import aiofiles

problems = {}

problems_filename = 'problems.json'

def read_problems():
    global problems
    problems = {}
    with open('problems.json') as problems_file:
        list = jsons.loads(problems_file.read())
    for problem_name in list:
        problems[problem_name] = Problem()
        problems[problem_name].details = list[problem_name]['details']
        for input in list[problem_name]['cases']:
            problems[problem_name].cases[input] = (list[problem_name]['cases']
                [input])

async def write_problems():
    async with aiofiles.open('problems.json', 'w') as problems_file:
        await problems_file.write(jsons.dumps(problems))

async def problem_exists(ctx, problem_name):
    if problem_name in problems:
        return True
    else:
        await ctx.send('Problem ' + problem_name + ' does not exist.')
        return False

class Problems(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send('You must be the bot owner to use this command.')
            return
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send('You do not have the permissions required to use',
                'this command.')
            return
        print(error)

    @commands.command()
    @commands.is_owner()
    async def addprob(self, ctx, problem_name):
        '''Adds a problem. Only available to the bot owner.'''
        if problem_name in problems:
            await ctx.send('Problem ' + problem_name + ' already exists.')
            return
        problems[problem_name] = Problem()
        await ctx.send('Problem ' + problem_name + ' successfully added.')
        await write_problems()

    @commands.command()
    @commands.is_owner()
    async def delprob(self, ctx, problem_name):
        '''Deletes a problem. Only available to the bot owner'''
        if not await problem_exists(ctx, problem_name):
            return
        del problems[problem_name]
        await ctx.send('Problem ' + problem_name + ' successfully deleted.')
        await write_problems()

    @commands.command()
    @commands.is_owner()
    async def setprobdetails(self, ctx, problem_name, *, arg):
        '''Sets a problem's details. Only available to the bot owner.'''
        if not await problem_exists(ctx, problem_name):
            return
        problems[problem_name].details = arg
        await write_problems()

    @commands.command()
    async def prob(self, ctx, problem_name):
        '''Retrieves information about a problem.'''
        if not await problem_exists(ctx, problem_name):
            return
        text = 'Problem details:```\n'
        text += problems[problem_name].details
        text += '\n```'
        await ctx.send(text)

    @commands.command()
    @commands.is_owner()
    async def clearprobcases(self, ctx, problem_name):
        '''Clears a problem's cases. Only available to the bot owner.'''
        if not await problem_exists(ctx, problem_name):
            return
        problems[problem_name].cases = {}

        await write_problems()

    @commands.command()
    @commands.is_owner()
    async def addcase(self, ctx, problem_name, *, arg):
        '''Adds a problem case. Only available to the bot owner.'''
        if not await problem_exists(ctx, problem_name):
            return
        list = arg.split('|')
        expected_input = list[0]
        expected_output = list[1]
        problems[problem_name].cases[expected_input] = expected_output
        message = 'Case successfully added.\n'
        message += 'Expected input:```\n' + expected_input + '```'
        message += 'Expected output:```\n' + expected_output + '```'
        await ctx.send(message)
        await write_problems()

    @commands.command()
    async def listprobs(self, ctx):
        '''Lists available problems.'''
        if not problems:
            await ctx.send('No problems were found.')
            return
        problems_list = "Problems:\n```\n"
        for problem_name in problems:
            problems_list += problem_name + "\n"
        problems_list += "```"
        await ctx.send(problems_list)
