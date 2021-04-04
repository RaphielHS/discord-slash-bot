import time
start = time.time()
try:
    import discord
    import asyncio
    import random
    import datetime

    from discord import Embed
    from discord.ext import commands
    from discord_slash import SlashCommand, SlashContext
    from discord_slash.utils.manage_commands import create_option

    client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
    slash = SlashCommand(client, sync_commands=True)

    __author__ = 'Raphiel#4045'
    __version__ = '1.0.1'

    def uptime():
        now = time.time()
        hours, rem = divmod(now - start, 3600)
        minutes, seconds = divmod(rem, 60)
        return ("{:0>2} Hours(H), {:0>2} Minutes(M), {:05.2f} Seconds(S).".format(int(hours),int(minutes),seconds))

    @client.event
    async def on_ready():
        print("Ready as %s." % client.user)
        print(f"Bot Created By {__author__}")
        print(f"Bot Version: {__version__}")

    guildids = [744103149471662152]

    @slash.slash(name="ping",
                 description="Get the bot latency",
                 guild_ids=guildids
                 )
    async def _ping(ctx):
        await ctx.send(f"Pong! My Ping is {round(client.latency * 1000)}ms!")

    @slash.slash(name="say",
                 description="Make the bot say something!",
                 guild_ids=guildids,
                 options = [
                    {
                        "name": "Message",
                        "description": "The Message The Bot is going to say",
                        "type": 3,
                        "required": "true"
                    }
                 ])
    async def _say(ctx, *, message=None):
        await ctx.send(f"\"{message}\"\n ~ {ctx.author.mention}", allowed_mentions=discord.AllowedMentions(everyone=False))

    @slash.slash(name="timer",
                 description="Make a timer that go off!",
                 guild_ids=guildids,
                 options = [
                    {
                        "name": "time",
                        "description": "Timeout",
                        "type": 4,
                        "required": "true"
                    }
                 ])
    async def _timer(ctx, time):
        message = await ctx.send(f"Time set for {time} seconds!")
        await asyncio.sleep(int(time) - 1)
        await message.edit(content="Times Up!")
        await ctx.author.send(f"Times Up For {time}s!")

    @slash.slash(name="choose",
                 description="Pick a random stuff!",
                 guild_ids=guildids,
                 options = [
                     {
                        "name": "first",
                        "description": "First Message",
                        "type": 3,
                        "required": "true"
                     },
                     {
                        "name": "second",
                        "description": "Second Message",
                        "type": 3,
                        "required": "true"
                     },
                     {
                        "name": "third",
                        "description": "Second Message",
                        "type": 3,
                        "required": "false"
                     },
                     {
                        "name": "fourth",
                        "description": "Second Message",
                        "type": 3,
                        "required": "false"
                     },
                     {
                        "name": "fifth",
                        "description": "Second Message",
                        "type": 3,
                        "required": "false"
                     }
                 ])
    async def _choose(ctx, *args):
        r = random.choice(list(args))
        await ctx.send(f"I Choose, `{r}`!", allowed_mentions=discord.AllowedMentions(everyone=False))

    @slash.slash(name="random_int",
                 description="Generate a random number",
                 guild_ids=guildids,
                 options=[
                    {
                        "name": "range",
                        "description": "Amount to generate and random pick (Default 100)",
                        "type": 4,
                        "required": "false"
                    }
                 ])
    async def _random_int(ctx, amount: int=100):
        r = random.choice(range(0, amount))
        await ctx.send(f"Random generating {amount} Numbers...\nI Choose `{r}`!")

    @slash.slash(name="serverinfo",
                 description="Get the server info!",
                 guild_ids=guildids
                 )
    async def _serverinfo(ctx):
        embed = Embed(
            title=f"{ctx.guild.name} Info",
            description=f"""
**[>] Guild Name:** {ctx.guild.name}
**[>] Guild ID:** {ctx.guild.id},
**[>] Guild Owner:** {ctx.guild.owner}
**[>] Guild Roles:** {len(ctx.guild.roles)} Roles
**[>] Guild Members:** {len(ctx.guild.members)} Members""",
            color=discord.Color.green())
        await ctx.send(embed=embed)

    @slash.slash(name="userinfo",
                 description="Get the info of a user",
                 guild_ids=guildids,
                 options=[
                    {
                        "name": "user",
                        "description": "Info of the mentioned user!",
                        "type": 6,
                        "required": "true"
                    }
                 ])

    async def _userinfo(ctx, user):
        try:
            u = user.created_at
            integer_val = 10000 * u.year + 100 * u.month + u.day
            days = integer_val // 86400
            hours = (integer_val - days * 86400) // 3600
            minutes = (integer_val - days * 86400 - hours * 3600) // 60
            seconds = integer_val - days * 86400 - hours * 3600 - minutes * 60
            result = ("{} days, ".format(days) if days else "") + \
                     ("{} hours, ".format(hours) if hours else "") + \
                     ("{} minutes, ".format(minutes) if minutes else "") + \
                     ("{} seconds, ".format(seconds) if seconds else "")
            created_at =  f"{result} Ago."
            roles = []
            for role in user.roles:
                if role.name != '@everyone':
                    roles.append(role.mention)
            roles.reverse()
            roless = ', '.join(roles)
            embed = Embed(
                title=f"{user.name} Info",
                description=f"""
**[>] Username:** {user.name}
**[>] Display Name:** {user.display_name}
**[>] Discriminator:** {user.discriminator}
**[>] Created At:** {user.created_at.strftime("%d/%m/%Y, %H:%M:%S")} ({created_at})
**[>] User Roles:** {roless + ", @everyone"}""",
                color=discord.Color.green()
                )
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            raise e

    @slash.slash(name="info",
                 description="Get the bot info!",
                 guild_ids=guildids
                 )
    async def _info(ctx):
        embed = Embed(
            title=f"{client.user.name} info",
            description=f"""
**[>] Username:** {client.user.name}
**[>] Discriminator:** {client.user.discriminator}
**[>] Guild Display Name:** {client.user.display_name}
**[>] Ping:** {round(client.latency * 1000)}ms
**[>] Guilds:** {len(client.guilds)}
**[>] Uptime:** {uptime()}""",
            color=discord.Color.green()
            )
        await ctx.send(embed=embed)

    @slash.slash(name="math",
                 description="Reduce, Add, Multiply, and Split Numbers",
                 guild_ids=guildids,
                 options=[
                    {
                        "name": "first",
                        "description": "First Number",
                        "type": 4,
                        "required": "true"
                    },
                    {
                        "name": "operator",
                        "description": "Operator",
                        "type": 3,
                        "required": "true"
                    },
                    {
                        "name": "second",
                        "description": "Second Number",
                        "type": 4,
                        "required": "true"
                    },
                 ])
    async def _math(ctx, first, operator, second):
        try:
            if operator in ['+', 'add', 'Add', 'plus', 'Plus']:
                await ctx.send("The Result Is {}".format(first + second))
                return
            if operator in ['/', 'divide', 'Divide', 'slash', 'Slash']:
                await ctx.send("The Result Is {}".format(first / second))
                return
            if operator in ['*', 'multiply', 'Multiply', 'time', 'times']:
                await ctx.send("The Result Is {}".format(first * second))
                return
            if operator in ['-', 'reduce', 'Reduce', 'min', 'Min', 'minus', 'Minus']:
                await ctx.send("The Result Is {}".format(first - second))
                return
            await ctx.send(f"{ctx.author.mention}, Sorry, But {operator} is not a valid operator.")

        except ZeroDivisionError:
            await ctx.send(f"Error: You can't Divide 0.")

    client.run("token")
except Exception as e:
    print(e)
    raise e
