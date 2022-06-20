# This example requires the 'members' privileged intents

from discord.ext.commands import CommandNotFound

import discord
from discord.ext import commands
import random
import ggpt
import re
import asyncio
import argparse
import logging
import os

last_message = ""


parser = argparse.ArgumentParser()
parser.add_argument(
    "-log", 
    "--log", 
    default="warning",
    help=(
        "Provide logging level. "
        "Example --log debug', default='warning'"
    ),
)

options = parser.parse_args()
levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}

level = levels.get(options.log.lower())
if level is None:
    raise ValueError(
        f"log level given: {options.log}"
        f" -- must be one of: {' | '.join(levels.keys())}")
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

description = '''GPT bot'''

DM_PATTERN = "Direct Message with\s+(.*)"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=['?', '!'], description=description, intents=intents)

############
NEOX = 'gptneox_20B'
engines = ['gptj_6B', 'boris_6B', 'fairseq_gpt_13B', NEOX]
aliases = ['gptj', 'boris', 'fairseq', 'gptneox']

def match_engine(to_match):
    if to_match.lower() == 'neox':
        return NEOX
    for engine, alias in zip(engines, aliases):
        if to_match.lower() == engine.lower():
            return engine
        if to_match.lower() == alias.lower():
            return engine
    return None
############
    
gpt_contexts = {}

def get_predictor(ctx):
    channel_id = get_key(ctx)
    if not channel_id in gpt_contexts:
        g = ggpt.GPT()
        g.last_message = ""
        g.last_prompt = ""
        g.last_result = ""        
        gpt_contexts[channel_id] = g
    #logger.info(channel_id)

    return gpt_contexts[channel_id]

def is_dm(ctx):
    descriptor = str(ctx.channel)
    match = re.search(DM_PATTERN, descriptor)
    if match:
        return True
    else:
        return False
    
def get_key(ctx):
    descriptor = str(ctx.channel)
    match = re.search(DM_PATTERN, descriptor)
    if match: 
        channel_id = match.group(1)
    else:
        channel_id = f"#{descriptor}"
    return channel_id
    
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event    
async def on_message(message):
    ctx = await bot.get_context(message)   
    predictor = get_predictor(ctx)
    await bot.process_commands(message)      
    
    predictor.last_message = message.content

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@bot.command(name="settings", aliases=["why"])
async def settings(ctx):    
    predictor = get_predictor(ctx)
    settings_msg = str(predictor)
    await ctx.send(settings_msg)

@bot.command(name="complete", aliases=["predict", "gpt", "c"])
async def complete(ctx, *, arg):
    await predict_out(ctx, arg)
    
@bot.command(name="more", aliases=["m", "continue"])
async def more(ctx):
    predictor = get_predictor(ctx)
    await predict_out(ctx, predictor.last_result)

@bot.command(name="youtubethat", aliases=["last", "doit", "go", "recordthatjim"])
async def youtubethat(ctx):
    predictor = get_predictor(ctx)
    await predict_out(ctx, predictor.last_message)

@bot.command(name="makeitslick")
async def makeitslick(ctx):
    await ctx.send("i told you i can't make it slick")

def parse_float(x):
    try:
        return float(x)
    except ValueError:
        return None

@bot.command(name="engine")
async def engine(ctx, *, arg):
    matched_engine = match_engine(arg)
    if matched_engine is None:
        msg = f"{arg} is not a valid engine. choose from: " + ", ".join(engines)
    else:
        predictor = get_predictor(ctx)
        predictor.engine_id = matched_engine
        msg = f"engine set to {matched_engine}."
        
    await ctx.send(msg)
       

@bot.command(name="top_k")
async def top_k(ctx, *, arg):

    i = None
    if arg.isdigit():
        i = int(arg)
        if i < 1 or i > 1000:
            i = None

    if i is None:
        await ctx.send("nope - top_k must be an integer between 1 and 1000 (default = 40)")
    else:
        predictor = get_predictor(ctx)
        predictor.top_k = i        
        await ctx.send(f"top_k set to {predictor.top_k}")


@bot.command(name="max_tokens", aliases=['tokens', 'num_tokens'])
async def max_tokens(ctx, *, arg):

    i = None
    if arg.isdigit():
        i = int(arg)
        if i < 1 or i > 1024:
            i = None

    if i is None:
        await ctx.send("nope - max_tokens must be an integer between 1 and 1024")
    else:
        predictor = get_predictor(ctx)
        predictor.max_tokens = i        
        await ctx.send(f"max_tokens set to {predictor.max_tokens}")


@bot.command(name="top_p")
async def top_p(ctx, *, arg):

    f = parse_float(arg)
    if f is not None:
        if f < 0 or f > 1:
            f = None

    if f is None:
        await ctx.send("nope - top_p must be an float between 0 and 1 (default = 0.9)")
    else:
        predictor = get_predictor(ctx)
        predictor.top_p = f        
        await ctx.send(f"top_p set to {predictor.top_p}")

@bot.command(name="temperature", aliases=["temp"])
async def temperature(ctx, *, arg):

    f = parse_float(arg)

    if f is None:
        await ctx.send("nope - temperature must be a float")
    else:
        predictor = get_predictor(ctx)
        predictor.temperature = f        
        await ctx.send(f"temperature set to {predictor.temperature}")

@bot.command(name="again", aliases=["nno", "NNO", "no", "NO", "repeat", "bad", "boring", "BORING"])
async def again(ctx):
    predictor = get_predictor(ctx)
    await predict_out(ctx, predictor.last_prompt)

async def predict_out(ctx, prompt):

    await ctx.send(random.choice([":ok:", ":cool:", ":up:"]))

    await asyncio.sleep(1)
    
    MAX_MSG_LEN = 1900

    predictor = get_predictor(ctx)
    trunc_prompt = prompt
    if len(prompt) > 500:
        trunc_prompt = prompt[-499:]
    try:
        completion = predictor.predict(trunc_prompt)
        msg = f'*{trunc_prompt}*{completion}'
        predictor.last_result = f'{trunc_prompt}{completion}'
        predictor.last_prompt = trunc_prompt
        
    except ggpt.GPTException as e:
        msg = f"nope - {e}"
    
    if len(msg) < MAX_MSG_LEN: 
        await ctx.send(msg)    
    else:
        while len(msg) > MAX_MSG_LEN:
            to_post, remainder = msg[:MAX_MSG_LEN], msg[MAX_MSG_LEN:]
            await ctx.send(to_post)
            msg = remainder
            await asyncio.sleep(3)
    
    await ctx.send(random.choice([":white_check_mark:", ":checkered_flag:", ":blossom:"]))


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    bot.run(os.environ.get('DISCORD_KEY_GPTBOT'))
