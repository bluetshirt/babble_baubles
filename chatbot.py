from discord.ext.commands import CommandNotFound

import discord
from discord.ext import commands
import random
import ggpt
import re
import asyncio
import argparse
import logging
import gptbot
import os

CMD_PROMPT = "<human>"
BOT_PROMPT = "<bot>"
END_TOKEN = "<end>"
MAX_PROMPT_LEN = 1000

INIT_LOG = f"This is a conversation between a bot and a human.\n The bot's messages will be indicated with {BOT_PROMPT}; the human's will be marked with {CMD_PROMPT}. Message endings are indicated with an {END_TOKEN} token.\nShort example:\n{CMD_PROMPT}hi bot!{END_TOKEN}\n{BOT_PROMPT}hello, human!{END_TOKEN}\n{CMD_PROMPT}how are you today?{END_TOKEN}\n{BOT_PROMPT}i am doing well for a robot!{END_TOKEN}\nThis concludes the example. The conversation begins below.\n\n"

description = '''GPT chat bot'''

async def get_reply(predictor):

    MAX_MSG_LEN = 1900
    MAX_TRIES = 5
        
    try:
        try_count = 0
        msg = None
        while try_count < MAX_TRIES and msg is None:
            try_count += 1
            print("SENDING:")
            print(predictor.chat_log)
            completion = predictor.predict(predictor.chat_log)
            print("RECEIVING:")
            print(completion)
            end_pos = completion.find(END_TOKEN)
            if end_pos >= 0:
                msg = completion[:end_pos]

        if msg is None:
            msg = f"[[[[nope - couldn't find end token after {MAX_TRIES} attempts]]]"
       
    except ggpt.GPTException as e:
        msg = f"nope - {e}"
    
    if len(msg) < MAX_MSG_LEN: 
        msg = msg[:MAX_MSG_LEN-1]

    return msg
    
@gptbot.bot.event    
async def on_message(message):

    ctx = await gptbot.bot.get_context(message)   

    predictor = gptbot.get_predictor(ctx)
    
    if gptbot.is_dm(ctx):
        if message.author != gptbot.bot.user:           

            said = message.content
            if not hasattr(predictor, 'chat_log'):
                predictor.chat_log = INIT_LOG       
               
            predictor.chat_log = f"{predictor.chat_log}{CMD_PROMPT}{said}{END_TOKEN}\n{BOT_PROMPT}"

            reply = await get_reply(predictor)
            predictor.chat_log = f"{predictor.chat_log}{reply}{END_TOKEN}\n"

            if len(predictor.chat_log) > MAX_PROMPT_LEN:
                predictor.chat_log  = predictor.chat_log[-MAX_PROMPT_LEN:]
                  
            await ctx.channel.send(reply)

if __name__ == "__main__":
    gptbot.bot.command_prefix = "&"       
    gptbot.bot.run(os.environ.get('DISCORD_KEY_CHATBOT'))