# This example requires the 'members' privileged intents

import discord
from discord.ext import commands
import random
import ggpt
import re
import gptbot
import oblique_strategy
import os

description = '''S.E.R.G.E. - a Synthesizer, Except Really Good At English'''

intents = discord.Intents.default()
intents.members = True

@gptbot.bot.event
async def on_ready():
    print(f'Logged in as {gptbot.bot.user} (ID: {gptbot.bot.user.id})')
    print('------ :)')

@gptbot.bot.command(name="serge", aliases=["s"])
async def serge(ctx):
    await ctx.send("that's me! S.E.R.G.E! a Synthesizer Except Really Good at English! Bleep bloop!")

@gptbot.bot.command(name="oblique", aliases=["o", "eno", "schmidt", "strat", "strategy", "random", "inspire"])
async def oblique(ctx):
    await ctx.send(oblique_strategy.random_quote())

@gptbot.bot.command(name="unique", aliases=["fart"])
async def unique(ctx):
    await ctx.send(oblique_strategy.custom_wisdom())

@gptbot.bot.command(name="wisdom", aliases=["add"])
async def wisdom(ctx, *, arg):
    oblique_strategy.save_quote(arg)
    await ctx.send(":brain:")

gptbot.bot.command_prefix = "!"
       
gptbot.bot.run(os.environ.get("DISCORD_KEY_SERGE"))

