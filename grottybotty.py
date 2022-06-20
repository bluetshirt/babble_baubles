# This example requires the 'members' privileged intents

from discord.ext.commands import CommandNotFound

import discord
from discord.ext import commands
import random
import grottify
import os

description = '''GrottyBotty - Add songs to Stiff's spotify queue!'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command(name="enqueue", aliases=["queue", "q"])
async def enqueue(ctx, *, arg):
    """Add's a song to Stiff's Spotify queue."""
        
    #detect whether or not my husband is trying to sneak
    #the Dandy Warhols song "Bohemian Like You" onto my playlist.
    if "ohemi" in arg or "andy" in arg:
        await ctx.send("BOOO TOMATO TOMATO TOMATO TOMATO TOMATO")
    
    try:
        artists, name, _ = grottify.enqueue(arg)
        msg = f'Queued {artists} - "{name}"'
        await ctx.send(msg)
    except Exception as e:
        msg = f"exception: {str(e)}" 
        
@bot.command(name="like", aliases=["good", "yay"])
async def like(ctx, *, arg):
    """Add's a song to Stiff's Liked Songs list on Spotify."""

    try:
        artists, name, success = grottify.like(arg)
        if success:
            msg = f'Liked {artists} - "{name}"'
        else:
            msg = f'You already like {artists} - "{name}"!'
    except Exception as e:
        msg = f"exception: {str(e)}" 
    await ctx.send(msg)    
    
    
@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

bot.run(os.environ.get('DISCORD_KEY_GROTTYBOTTY'))



