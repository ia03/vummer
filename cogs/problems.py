from discord.ext import commands
from problem import Problem
import jsons
import aiofiles

problems = {}

current_problem = {}

problems_filename = 'problems.json'

def get_problem(problem_name):
    return problems[problem_name]

def get_current_problem(author_id):
    if author_id in current_problem:
        if current_problem[author_id] in problems:
            return current_problem[author_id]
        else:
            current_problem[author_id] = None
            return None
    else:
        return None

def read_problems():
    global problems
    problems = {}
    with open('problems.json') as problems_file:
        list = jsons.loads(problems_file.read())
    for problem_name in list:
        problems[problem_name] = Problem()
        problems[problem_name].details = list[problem_name]['details']
        problems[problem_name].cases = {}
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
        """Adds a problem. Only available to the bot owner."""
        if problem_name in problems:
            await ctx.send('Problem ' + problem_name + ' already exists.')
            return
        problems[problem_name] = Problem()
        problems[problem_name].cases = {}
        await ctx.send('Problem ' + problem_name + ' successfully added.')
        await write_problems()

    @commands.command()
    @commands.is_owner()
    async def delprob(self, ctx, problem_name):
        """Deletes a problem. Only available to the bot owner"""
        if not await problem_exists(ctx, problem_name):
            return
        del problems[problem_name]
        await ctx.send('Problem ' + problem_name + ' successfully deleted.')
        await write_problems()

    @commands.command()
    @commands.is_owner()
    async def setprobdetails(self, ctx, problem_name, *, arg):
        """Sets a problem's details. Only available to the bot owner."""
        if not await problem_exists(ctx, problem_name):
            return
        problems[problem_name].details = arg
        await ctx.send('Problem details set.')
        await write_problems()

    @commands.command()
    async def prob(self, ctx, problem_name):
        """Retrieves information about a problem."""
        if not await problem_exists(ctx, problem_name):
            return
        text = 'Problem details:```\n'
        text += problems[problem_name].details
        text += '\n```'
        await ctx.send(text)

    @commands.command()
    @commands.is_owner()
    async def clearcases(self, ctx, problem_name):
        """Clears a problem's cases. Only available to the bot owner."""
        if not await problem_exists(ctx, problem_name):
            return
        problems[problem_name].cases = {}
        await ctx.send('Cases cleared.')
        await write_problems()

    @commands.command()
    @commands.is_owner()
    async def addcase(self, ctx, problem_name, *, arg):
        """Adds a problem case. Only available to the bot owner."""
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
    @commands.is_owner()
    async def delcase(self, ctx, problem_name, *, arg):
        """Deletes a problem case. Only available to the bot owner."""
        if not await problem_exists(ctx, problem_name):
            return
        if arg not in problems[problem_name].cases:
            await ctx.send('The specified case does not exist.')
        del problems[problem_name].cases[arg]
        await ctx.send('Case deleted.')
        await write_problems()

    @commands.command()
    @commands.is_owner()
    async def listcases(self, ctx, problem_name):
        """Lists a problem's cases. Only available to the bot owner."""
        if not await problem_exists(ctx, problem_name):
            return
        cases = problems[problem_name].cases
        if not cases:
            await ctx.send('No cases found.')
            return
        message = ""
        for expected_input in cases:
            expected_output = cases[expected_input]
            message += ("Expected input:```\n" + expected_input + "\n```"
                + "Expected output:```\n" + expected_output + "\n```")
        await ctx.send(message)

    @commands.command()
    async def setprob(self, ctx, problem_name=None):
        """Uses future code submissions as answers to the specific problem.
        Using this command without a problem name makes the bot stop checking
        your submissions against the specified problem."""
        if problem_name:
            if not await problem_exists(ctx, problem_name):
                return
        current_problem[ctx.author.id] = problem_name
        if problem_name:
            await ctx.send('Problem successfully set.')
        else:
            await ctx.send('The bot will no longer check your submissions.')

    @commands.command()
    async def listprobs(self, ctx):
        """Lists available problems."""
        if not problems:
            await ctx.send('No problems were found.')
            return
        problems_list = "Problems:\n```\n"
        for problem_name in problems:
            problems_list += problem_name + "\n"
        problems_list += "```"
        await ctx.send(problems_list)
