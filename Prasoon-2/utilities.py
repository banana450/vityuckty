# -*- coding: utf-8 -*-
import contextlib
import io
import logging
import os
import random
import base64
import pprint
import traceback

import aiohttp
import discord
from discord.ext.commands.errors import CommandNotFound, MissingPermissions
import pymysql.cursors
from classes import NotGuildOwner, NotVoter
from discord.ext import commands

columnNames = ["defaultPrefix", "prefix1", "prefix2", "prefix3", "prefix4", "prefix5"]


def DotenvVar(var: str):
    return os.getenv(var)

topggSession = aiohttp.ClientSession(headers={"Authorization": DotenvVar("top-gg-auth")})

def EmojiBool(bool: bool):
    switch = {
        True: "<:burple_tick:949137414507614288>",
        False: "<:burple_wrong:949137632963727390>",
    }
    return switch.get(bool, "N/A")


def is_voter_only():
    async def predicate(ctx: commands.Context):
        if ctx.author.id == 806519089144135720:
            return True
        else:
            async with topggSession.get("https://top.gg/api/bots/861814656851378176/check?userId=%s" % (str(ctx.author.id))) as response:
               json = await response.json()
               print(json)
               if json["voted"] == 1:
                   response.close()
                   return True
               else:
                   response.close()
                   raise NotVoter()
    return commands.check(predicate)

def is_guild_owner():
    async def predicate(ctx: commands.Context):
        if ctx.author.id == ctx.guild.owner.id:
            return True
        else:
            return NotGuildOwner()
    return commands.check(predicate)



def create_linkvertise(redirect_url: str) -> str:
    return "https://link-to.net/327045/{0}/dynamic?r={1}".format(random.randint(1, 9000), base64.encodebytes(redirect_url.encode('utf-8')).decode('utf-8'))

def HumanStatus(status):
    switch = {
        "dnd": "Do Not Disturb.",
        "online": "Online.",
        "idle": "Idle.",
        "offline": "Offline.",
    }
    return switch.get(status, "Error.")



async def report(self, ctx, error):
    try:
        error = ''.join(traceback.format_exception(
            etype=type(error), value=error, tb=error.__traceback__))
        owner = await self.bot.fetch_user(self.bot.owner_id)
        id = __import__('nanoid').generate()
        embed = discord.Embed(title="Oops !", description="Something went wrong and we're not quite sure what. Your error has been reported to the developers. ID - `%s`" % (id),
                              color=discord.Color.red())
        await ctx.reply(embed=embed, mention_author=True)

        if len(error) < 1850:
            await owner.send('ID - **`{}`**\n**Error in the command `{}`**, Invoked in `{}` by `{}`\n```\n'.format(id, ctx.command.name, ctx.guild.name, ctx.author) + error + '\n```')
        else:
            await owner.send(content='**Error in the command `{}`**, Invoked in `{}` by `{}`'.format(ctx.command.name, ctx.guild.name, ctx.author), file=discord.File(fp=io.BytesIO(error.encode(errors='ignore')), filename='exception.txt'))
    except Exception as exc:
        print(traceback.format_exception(
            etype=type(exc), value=exc, tb=exc.__traceback__))




def logError(exception: Exception):
    pprint.pprint(traceback.format_exception(
        type(exception), exception, exception.__traceback__))


def logInfo(message):
    logging.log(logging.INFO, message)

def wrap(font, text,
         line_width):  # https://github.com/DankMemer/imgen/blob/master/utils/textutils.py (useful asf so i stole it not even gonna cap w you)
    words = text.split()
    lines = []
    line = []
    for word in words:
        newline = ' '.join(line + [word])
        width, height = font.getsize(newline)
        if width > line_width:
            lines.append(' '.join(line))
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(' '.join(line))
    return ('\n'.join(lines)).strip()
