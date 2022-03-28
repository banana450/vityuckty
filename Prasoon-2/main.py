import discord
import os
from discord.ext import commands
import json
os.system("pip install discord_components")
os.system("pip install discord_buttons_plugin")
from discord.colour import Color
import requests
import os.path
from dotenv import load_dotenv
load_dotenv()
from discord_components import DiscordComponents, Button, Select, SelectOption
from discord_components import *
from discord_components.component import Button, ButtonStyle

import datetime
start_time = datetime.datetime.utcnow()
from Tools.utils import getConfig
from Tools.utils import updateConfig
from cogs.AntiSpam import AntiSpam
from cogs.Antinuke import Antinuke
from cogs.Info import Info
from cogs.mod import Mod
from cogs.music import Music
from dotenv import load_dotenv
load_dotenv()
from discord_components import *
from discord_components.component import Button, ButtonStyle
import discord_buttons_plugin
from discord.ext import commands
from discord_buttons_plugin import *

token = "ODYxODE0NjU2ODUxMzc4MTc2.YOPRcQ.-4eYzTUNxqCDqO70GzA1OvP_9Yo" 

prefix = ">"

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(
  command_prefix=commands.when_mentioned_or(">"), 
  intents=intents,
  help_command=None
)
buttons = ButtonsClient(client)
client.add_cog(AntiSpam(client))
client.add_cog(Info(client))
client.add_cog(Mod(client))
client.add_cog(Music(client))


def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 806519089144135720 or ctx.message.author.id == 806519089144135720


@client.listen("on_guild_join")
async def update_json(guild):
    with open ('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)


    if str(guild.id) not in whitelisted:
      whitelisted[str(guild.id)] = []


    with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
        

@client.event
async def on_ready():
  print(f"Successfully Connected to {client.user}")


@client.event
async def on_connect():

  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))

@client.event
async def on_member_join(member):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
    guild = member.guild
    reason = "ViRTUCY SEC | Anti Bot"
    logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add).flatten()
    logs = logs[0]
    if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
      return
    else:
     if member.bot:
      await member.ban(reason=f"{reason}")
      await logs.user.ban(reason=f"{reason}")

@client.event
async def on_member_remove(member):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
    guild = member.guild
    logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
    logs = logs[0]
    reason = "ViRTUCY SEC | Anti-Kick "
    if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
      return
    else:
      await logs.user.ban(reason=f"{reason}")

    
@client.listen("on_member_remove")
async def on_member_prune(member):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
  guild = member.guild
  logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.member_prune).flatten()
  logs = logs[0]
  if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
    return
  else:
    reason = "ViRTUCY SEC | Anti-Prune"
    await logs.user.ban(reason=f"{reason}")

@client.event
async def on_member_ban(guild, member : discord.Member):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
    reason = "ViRTUCY SEC | Anti-Ban"
    logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
    logs = logs[0]
    if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
      return
    else:
      await logs.user.ban(reason=f"{reason}")
      await guild.unban(user=member, reason="ViRTUCY SEC | Recovery ")

@client.event
async def on_member_unban(guild, user):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
  reason= "ViRTUCY SEC | Anti Member Unban"
  logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.unban).flatten()
  logs = logs[0]
  if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
    return
  else:
    await logs.user.ban(reason=f"{reason}")
    await user.ban(reason="ViRTUCY SEC | Recovery ")


@client.event
async def on_guild_channel_create(channel):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
  reason = "ViRTUCY SEC | Anti Channel Create"
  guild = channel.guild
  logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create).flatten()
  logs = logs[0]
  if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
    return
  else:
    await channel.delete(reason=f"ViRTUCY SEC | Recovery")
    await logs.user.ban(reason=f"{reason}")


@client.event
async def on_webhooks_update(webhook):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
  guild = webhook.guild
  reason= 'ViRTUCY SEC | Anti Webhook Create'
  logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.webhook_create).flatten()
  logs = logs[0]
  if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
    return
  else:
    await logs.user.ban(reason=f"{reason}")


@client.event
async def on_guild_role_create(role):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
  reason = "ViRTUCY SEC | Anti Role Create"
  guild = role.guild
  logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create).flatten()
  logs = logs[0]
  if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
    return
  else:
    await role.delete(reason=f"ViRTUCY SEC | Recovery")
    await logs.user.ban(reason=f"{reason}")


                    
@client.event
async def on_guild_update(before, after):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)      
  reason = "ViRTUCY SEC | Anti Guild Update"
  logs = await after.audit_logs(limit=1,action=discord.AuditLogAction.guild_update).flatten()
  logs = logs[0]
  if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(logs.guild.id)]:
    return
  else:
    await after.edit(name=f"{before.name}", reason = "ViRTUCY SEC | Recovery")
    await logs.user.ban(reason=f"{reason}")



@client.event
async def on_message(message):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
  await client.process_commands(message)
  member = message.author
  guild = message.guild
  if message.mention_everyone:
    if member.id == 806519089144135720 or member.id == 806519089144135720 or member.id == client.user.id or str(member.id) in whitelisted[str(guild.id)]:
      pass
    else:
      await message.delete()
      await member.ban(reason = "ViRTUCY SEC | Anti Everyone/here")
  else:
    if message.embeds:
      if member.bot:
        pass
      else:
        await member.ban(reason="ViRTUCY SEC | Anti Selfbot")      


@client.event
async def on_guild_emojis_update(guild, before, after):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
  reason = "ViRTUCY SEC | Emoji Update"
 # guild = after.guild
  logs = await guild.audit_logs(limit=1,action=discord.AuditLogAction.emoji_create).flatten()
  logs = logs[0]
  if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
    return
  else:
    await logs.user.ban(reason=f"{reason}")

@client.event
async def on_guild_role_delete(role):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
  guild = role.guild
  logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete).flatten()
  reason = "ViRTUCY SEC | Anti Role Delete"
  logs = logs[0]
  if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
    return
  else:
    await guild.create_role(name=f"{role}", reason=f"ViRTUCY SEC | Recovery")
    await logs.user.ban(reason=f"{reason}")


@client.event
async def on_guild_channel_delete(channel):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
  guild = channel.guild
  logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete).flatten()
  reason = "ViRTUCY SEC | Anti Channel Delete"
  logs = logs[0]
  if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
    return
  else:
    await channel.clone(reason=f"ViRTUCY SEC | Recovery")
    await logs.user.ban(reason=f"{reason}")

@client.event
async def on_guild_channel_update(before, after):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)    
  reason = "ViRTUCY SEC | Anti Channel Update"
  guild = after.guild
  logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update).flatten()
  logs = logs[0]
  if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
    return
  else: 
    await after.edit(name=f"{before.name}", reason=f"ViRTUCY SEC | Recovery")
    await logs.user.ban(reason=f"{reason}")


@client.event
async def on_guild_role_update(before, after):
  with open('whitelisted.json') as f:
    whitelisted = json.load(f)  
  reason = "ViRTUCY SEC | Anti Role Update"
  guild = after.guild
  logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update).flatten()
  logs = logs[0]
  if logs.user.id == 806519089144135720 or logs.user.id == 806519089144135720 or logs.user.id == client.user.id or str(logs.user.id) in whitelisted[str(guild.id)]:
    return
  else:
    await logs.user.ban(reason=f"{reason}")
    await after.edit(name=f"{before.name}", reason=f"ViRTUCY SEC | Recovery")



@client.command()
async def whitelisted(ctx):
  if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720:
    embed = discord.Embed(title=f"Whitelisted users for {ctx.guild.name}", description="")

    with open ('whitelisted.json', 'r') as i:
        whitelisted = json.load(i)
    try:
      for u in whitelisted[str(ctx.guild.id)]:
        embed.description += f"<@{(u)}> - {u}\n"
      await ctx.send(embed = embed)
    except KeyError:
      await ctx.send("Nothing found for this guild!")
  else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(color=Color.blurple(), description=f'**`Only {owner.display_name} Can Run This Command!`**')

        embed.set_author(
            name='ViRTUCY SEC',
            icon_url=            'https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        await ctx.send(embed=embed)    
        
@whitelisted.error
async def whitelisted_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title='ViRTUCY SEC', color=Color.blurple(), description=f'<@{ctx.guild.owner.id}> `Only Guild Owner can see Whitelisted list`')
        await ctx.reply(embed=embed)

@client.command(aliases=["wl"])
async def whitelist(ctx, user: discord.Member = None):
  if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720:
    if user is None:
        embed = discord.Embed(title='ViRTUCY SEC', color=Color.blurple(), description=f'**`Please Specify A Member To Whitelist`**')
        await ctx.reply(embed=embed)
        return
    with open ('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)


    if str(ctx.guild.id) not in whitelisted:
      whitelisted[str(ctx.guild.id)] = []
    else:
      if str(user.id) not in whitelisted[str(ctx.guild.id)]:
        whitelisted[str(ctx.guild.id)].append(str(user.id))
      else:
        embed = discord.Embed(title='ViRTUCY SEC', color=Color.blurple(), description=f'<@{user.id}> `is already in the Whitelist`**')
        await ctx.reply(embed=embed)
        return



    with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
    embed = discord.Embed(title='ViRTUCY SEC', color=Color.blurple(), description=f'<@{user.id}> `Has been added to Whitelist`')
    await ctx.reply(embed=embed)
  else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(color=Color.blurple(), description=f'**`Only {owner.display_name} Can Run This Command!`**')

        embed.set_author(
            name='ViRTUCY SEC',
            icon_url=            'https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        embed.set_thumbnail(
            url=            'https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        await ctx.send(embed=embed)   
@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title='ViRTUCY SEC', color=Color.blurple(), description=f'<@{ctx.guild.owner.id}> `Only Guild Owner can whitelist users`')
        await ctx.reply(embed=embed)

@client.command(description='antiprune')
async def antiprune(ctx):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720: #remove the "or True" later
        embed = discord.Embed(color=Color.blurple())
        embed.set_footer(text='ViRTUCY SEC')
        embed.set_author(
            
            name='ViRTUCY SEC Anti prune setup',
            icon_url='https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        embed.add_field(name="SettingUp", value='Anti Prune is Setting up')
        await ctx.send(embed=embed)
        role = await ctx.guild.create_role(name='SECURITY')
        print(ctx.guild.members)
        for mem in ctx.guild.members:
            try:
                await mem.add_roles(role)
            except:
                pass
        embed = discord.Embed(color=Color.blurple())
        embed.set_author(
            name='ViRTUCY SEC Anti prune ',
            icon_url=            'https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        embed.set_thumbnail(
            url=           'https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        embed.set_footer(text='ViRTUCY SEC ')
        embed.add_field(name="Finished",
                        value='<:burple_tick:949137414507614288> Finished up setting AntiPrune')
        
        await ctx.channel.send(embed=embed)
    else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(color=Color.blurple(), description=f'**`Only {owner.display_name} Can Run This Command!`**')

        embed.set_author(
            name='ViRTUCY SEC Anti prune',
            icon_url=            'https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        embed.set_thumbnail(
            url=            'https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        await ctx.send(embed=embed)

@client.command(aliases=["uwl"])
async def unwhitelist(ctx, user: discord.Member = None):
  if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720:
    if user is None:
      embed = discord.Embed(title='ViRTUCY SEC', color=Color.blurple(), description=f'`Please Specify A Member To Remove From Whitelist`')
      await ctx.reply(embed=embed)
      return
    with open ('whitelisted.json', 'r') as f:
      whitelisted = json.load(f)
    try:
      if str(user.id) in whitelisted[str(ctx.guild.id)]:
        whitelisted[str(ctx.guild.id)].remove(str(user.id))
      
      with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
      embed = discord.Embed(title='ViRTUCY SEC', color=Color.blurple(), description=f'<@{user.id}> `Has been Removed Whitelist`')
      await ctx.reply(embed=embed)
    except KeyError:
      embed = discord.Embed(title='ViRTUCY SEC', color=Color.blurple(), description=f'<@{user.id}> `Was never in Whitelist`')
      await ctx.reply(embed=embed)
  else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(color=Color.blurple(), description=f'**`Only {owner.display_name} Can Run This Command!`**')

        embed.set_author(
            name='ViRTUCY SEC Un-Whitelist',
            icon_url=            'https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        embed.set_thumbnail(
            url=            'https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif'
        )
        await ctx.send(embed=embed)     
@unwhitelist.error
async def unwhitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title='ViRTUCY SEC', color=Color.blurple(), description=f'<@{ctx.guild.owner.id}> `Only Guild Owner can whitelist users`')
        await ctx.reply(embed=embed)


@client.command()
async def features(ctx, member: discord.Member = None):
  embed = discord.Embed(color=Color.blurple()) 
  embed.set_author(name='ViRTUCY SEC',icon_url='https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif') 
  embed.set_thumbnail(url="https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif")
  embed.add_field( name=f"<:burple_book:950306397004890202>**__Features__**", value=f" ``` Anti Ban\n Anti Kick\n Anti Prune\n Anti Channel Create\n Anti Channel Update\n Anti Channel Delete\n Anti Role Create\n Anti Role Update\n Anti Role Delete\n Anti Guild Update\n Anti Everyone/Here\n Anti Invite Delete\n Anti Invite Update\n Anti Integration Create \n Anti Integration Update\n Anti Integration Delete\n Anti Bot Add\n Anti Community Spam\n Anti Webhook Create\n Anti Webhook Update\n Anti Webhook Delete\n Anti Unban\n``` \n **__SETTINGS__** \n `LIMITS = 1` \n `PUNISHMENT = BAN` \n `RECOVER = TRUE`",inline=True)

  await ctx.reply(embed=embed)


  



@client.command()
@commands.has_permissions(administrator=True)
async def recover(ctx):
    for channel in ctx.guild.channels:
        if channel.name in ('rules', 'moderator-only'):
            try: 
              await channel.delete()
            except: 
              pass

@client.command()
async def pruneestr(ctx):
  guild = ctx.guild
  try:
    po = await ctx.guild.estimate_pruned_members(days=1, roles=guild.roles)
    await ctx.channel.send(f"Here s your result {po}")
  except:
    pass

@client.command()
async def pruneest(ctx):
  try:
    po = await ctx.guild.estimate_pruned_members(days=1)
    await ctx.channel.send(f"Here s your result {po}")
  except:
    pass
    


@client.command()
@commands.check(is_server_owner)
async def antispam(ctx, antiSpam):

        antiSpam = antiSpam.lower()

        if antiSpam == "enable":
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["antiSpam"] = True
            

            embed = discord.Embed(color=Color.blurple())
            embed.add_field(name=f"**AntiSpam**", value=f"<:burple_tick:949137414507614288> AntiSpam is **enable** ", inline=False)
            await ctx.send(embed=embed)   

        elif antiSpam == "disable":
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["antiSpam"] = False
            

            embed = discord.Embed(color=Color.blurple())
            embed.add_field(name=f"**AntiSpam**", value=f"<:burple_wrong:949137632963727390> AntiSpam is **disable**", inline=False)
            await ctx.send(embed=embed)   
        
        
        updateConfig(ctx.guild.id, data)


@client.command()
@commands.check(is_server_owner)
async def antilink(ctx, antiLink):

        antiLink = antiLink.lower()

        if antiLink == "enable":
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["antiLink"] = True
            

            embed = discord.Embed(color=Color.blurple())
            embed.add_field(name=f"**AntiLink**", value=f"<:burple_tick:949137414507614288> AntiLink is **enable**", inline=False)
            await ctx.send(embed=embed)
        elif antiLink == "disable":
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["antiLink"] = False
            

            embed = discord.Embed(color=Color.blurple())
            embed.add_field(name=f"**AntiLink**", value=f"<:burple_wrong:949137632963727390> AntiLink is **disable**", inline=False)
            await ctx.send(embed=embed)
        
        
        updateConfig(ctx.guild.id, data)  

@client.command()
@commands.check(is_server_owner)
async def punishment(ctx, punishment):

        punishment = punishment.lower()

        if punishment == "ban":
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["punishment"] = "ban"
            

            embed = discord.Embed(description=f"**ViRTUCY SEC**", color=Color.blurple())
            embed.add_field(name=f"**Punishment**", value=f"Punishment Set To `Ban`", inline=False)
            await ctx.send(embed=embed)
        elif punishment == "kick":
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["punishment"] = "kick"
            

            embed = discord.Embed(description=f"**ViRTUCY SEC**", color=Color.blurple())
            embed.add_field(name=f"**Punishment**", value=f"Punishment Set To `Kick`", inline=False)
            await ctx.send(embed=embed)
        
        
        updateConfig(ctx.guild.id, data) 


@client.group(invoke_without_command=True)
async def help(ctx):
    page1 = discord.Embed (
        title = 'ViRTUCY SEC\nHelp, Prefix: >',
      description = '[Invite Me](https://discord.com/oauth2/authorize?client_id=861814656851378176&permissions=8&scope=bot%20applications.commands)\n[Support Server](https://discord.gg/BkFfD5C)',
        colour = discord.Colour.blurple()
    )
    page1.add_field(name = "<:stolen_emoji:952431975531176016> **Help**", value= "```Shows Help Menu```",inline=True)
    page1.add_field(name = "<:stolen_emoji:952431975531176016> **Moderation**", value= "```Shows Moderation Commands```",inline=True)
    page1.add_field(name = "<:stolen_emoji:952431975531176016> **Security**", value= "```Shows Security Commands```",inline=True)
    page1.add_field(name = "<:stolen_emoji:952431975531176016> **Utility**", value= "```Shows Utility Commands```",inline=True)
    page1.add_field(name = "<:stolen_emoji:952431975531176016> **Features**", value= "```Shows Antinuke Features```",inline=True)
    page1.set_thumbnail(url="https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif")
    page1.set_footer(text=">help <category> for more info | Ping 1ms")

    page2 = discord.Embed (
        title = 'ViRTUCY SEC | Moderation',
        colour = discord.Colour.blurple()
    )
    page2.add_field(name = "<:Staff:952425019823230986> **Snipe**", value= "```Shows Recently Deleted Message```",inline=True)
    page2.add_field(name = "<:Staff:952425019823230986> **Editsnipe**", value= "```Shows Recently Edited Message```",inline=True)
    page2.add_field(name = "<:Staff:952425019823230986> **Steal**", value= "```Steal Emoji```",inline=True)
    page2.add_field(name = "<:Staff:952425019823230986> **Purge**", value= "```Clear Messages [Ammount/User/all]```",inline=True)
    page2.set_thumbnail(url="https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif")
    page2.set_footer(text="Made with 💖 by ~ Prasoon#5547 ")

    page3 = discord.Embed (
        title = 'ViRTUCY SEC | Security',
        colour = discord.Colour.blurple()
    )

    page3.add_field(name = "<:Vip:952425213172269076> **Antiprune**", value= "```Setups Anti Prune```",inline=True)
    page3.add_field(name = "<:Vip:952425213172269076> **Antispam**", value= "```Antispam [Enable/Disable]```",inline=True)
    page3.add_field(name = "<:Vip:952425213172269076> **Antilink**", value= "```Antilink [Enable/Disable]```",inline=True)
    page3.add_field(name = "<:Vip:952425213172269076> **Whitelist**", value= "```Whitelists a Member```",inline=True)
    page3.add_field(name = "<:Vip:952425213172269076> **Unwhitelist**", value= "```Unwhitelists a Member```",inline=True)
    page3.add_field(name = "<:Vip:952425213172269076> **Whitelisted**", value= "```Shows The List Of Whitelisted Members```",inline=True)
    page3.add_field(name = "<:Vip:952425213172269076> **Recover**", value= "```Recovers Server From Community Spam```",inline=True)
    page3.set_thumbnail(url="https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif")
    page3.set_footer(text="Made with 💖 by ~ Prasoon#5547 ")

    page4 = discord.Embed (
        title = 'ViRTUCY SEC | Utility',
        colour = discord.Colour.blurple()
    )
    page4.add_field(name = "<:Settings:952425087494139944> **Userinfo**", value= "```Shows User's Info ```",inline=True)
    page4.add_field(name = "<:Settings:952425087494139944> **Serverinfo**", value= "```Shows Server's Info```",inline=True)
    page4.add_field(name = "<:Settings:952425087494139944> **Av**", value= "```Shows User's Avatar```",inline=True)
    page4.add_field(name = "<:Settings:952425087494139944> **Roleinfo**", value= "```Shows Info Of a Role```",inline=True)
    page4.add_field(name = "<:Settings:952425087494139944> **Invite**", value= "```Send Bot's Invite Link```",inline=True)
    page4.set_thumbnail(url="https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif")
    page4.set_footer(text="Made with 💖 by ~ Prasoon#5547 ")

    page5 = discord.Embed (
        title = 'ViRTUCY SEC | Features',
        colour = discord.Colour.blurple()
    )
    page5.set_thumbnail(url="https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif")
    page5.add_field( name=f"<:burple_book:950306397004890202>**__Features__**", value=f"``` Anti Ban\n Anti Kick\n Anti Prune\n Anti Channel Create\n Anti Channel Update\n Anti Channel Delete\n Anti Role Create\n Anti Role Update\n Anti Role Delete\n Anti Guild Update\n Anti Everyone/Here\n Anti Invite Delete\n Anti Invite Update\n Anti Integration Create \n Anti Integration Update\n Anti Integration Delete\n Anti Bot Add\n Anti Community Spam\n Anti Webhook Create\n Anti Webhook Update\n Anti Webhook Delete\n Anti Unban\n``` \n **__SETTINGS__** \n `LIMITS = 1` \n `PUNISHMENT = BAN` \n `RECOVER = TRUE`",inline=True)
    
        
    pages = [page1, page2, page3, page4, page5]

    message = await ctx.reply(embed = page1)
    await message.add_reaction('<:Backward_L:950309177002197042>')
    await message.add_reaction('<:backward:950308680467906581>')
    await message.add_reaction('<:forward:950308918582739014>')
    await message.add_reaction('<:Forward_R:950309065286893590>')

    def check(reaction, user):
        return user == ctx.author

    i = 0
    reaction = None

    while True:
        if str(reaction) == '<:Backward_L:950309177002197042>':
            i = 1
            await message.edit(embed = page1)
        elif str(reaction) == '<:backward:950308680467906581>':
            if i > 0:
                i -= 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '<:forward:950308918582739014>':
            if i < 5:
                i += 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '<:Forward_R:950309065286893590>':
            i = 6
            await message.edit(embed = page5)
        
        try:
            reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
            await message.remove_reaction(reaction, user)
        except:
            break

    await message.clear_reactions()

@help.command()
async def moderation(ctx):
  page2 = discord.Embed (
        title = 'ViRTUCY SEC | Moderation',
        colour = discord.Colour.blurple()
    )
  page2.add_field(name = "<:Staff:952425019823230986> **Snipe**", value= "```Shows Recently Deleted Message```",inline=True)
  page2.add_field(name = "<:Staff:952425019823230986> **Editsnipe**", value= "```Shows Recently Edited Message```",inline=True)
  page2.add_field(name = "<:Staff:952425019823230986> **Steal**", value= "```Steal Emoji```",inline=True)
  page2.add_field(name = "<:Staff:952425019823230986> **Purge**", value= "```Clear Messages [Ammount/User/all]```",inline=True)
  page2.add_field(name = "<:Staff:952425019823230986> **Nuke**", value= "```Nukes a Channel```",inline=True)
  page2.set_thumbnail(url="https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif")
  page2.set_footer(text="Made with 💖 by ~ Prasoon#5547")

  await ctx.reply(embed=page2)

@help.command()
async def security(ctx):
  page3 = discord.Embed (
        title = 'ViRTUCY SEC | Security',
        colour = discord.Colour.blurple()
    )

  page3.add_field(name = "<:Vip:952425213172269076> **Antiprune**", value= "```Setups Anti Prune```",inline=True)
  page3.add_field(name = "<:Vip:952425213172269076> **Antispam**", value= "```Antispam [Enable/Disable]```",inline=True)
  page3.add_field(name = "<:Vip:952425213172269076> **Antilink**", value= "```Antilink [Enable/Disable]```",inline=True)
  page3.add_field(name = "<:Vip:952425213172269076> **Whitelist**", value= "```Whitelists a Member```",inline=True)
  page3.add_field(name = "<:Vip:952425213172269076> **Unwhitelist**", value= "```Unwhitelists a Member```",inline=True)
  page3.add_field(name = "<:Vip:952425213172269076> **Whitelisted**", value= "```Shows The List Of Whitelisted Members```",inline=True)
  page3.add_field(name = "<:Vip:952425213172269076> **Recover**", value= "```Recovers Server From Community Spam```",inline=True)
  page3.set_thumbnail(url="https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif")
  page3.set_footer(text="Made with 💖 by ~ Prasoon#5547")

  await ctx.reply(embed=page3)

@help.command()
async def utility(ctx):
  page4 = discord.Embed (
        title = 'ViRTUCY SEC | Utility',
        colour = discord.Colour.blurple()
    )
  page4.add_field(name = "<:Settings:952425087494139944> **Userinfo**", value= "```Shows User's Info ```",inline=True)
  page4.add_field(name = "<:Settings:952425087494139944> **Serverinfo**", value= "```Shows Server's Info```",inline=True)
  page4.add_field(name = "<:Settings:952425087494139944> **Av**", value= "```Shows User's Avatar```",inline=True)
  page4.add_field(name = "<:Settings:952425087494139944> **Roleinfo**", value= "```Shows Info Of a Role```",inline=True)
  page4.add_field(name = "<:Settings:952425087494139944> **Invite**", value= "```Send Bot's Invite Link```",inline=True)
  page4.set_thumbnail(url="https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif")
  page4.set_footer(text="Made with 💖 by ~ Prasoon#5547")

  await ctx.reply(embed=page4)  
    

@client.command()
async def invite(ctx):
	embed = discord.Embed( color=discord.Colour.blurple(), description=f"[Invite ViRTUCY SEC](https://discord.com/oauth2/authorize?client_id=861814656851378176&permissions=8&scope=bot%20applications.commands) \n[Join Support Server](https://dsc.gg/vestrol-support)\n[Vote the bot on top.gg](https://top.gg/bot/861814656851378176/vote)")
	await buttons.send(
		content = None,
		embed = embed,
		channel = ctx.channel.id,
		components = [
			ActionRow([
				Button(
					style = ButtonType().Link,
					label = "Invite",
					url = f"https://discord.com/oauth2/authorize?client_id=861814656851378176&permissions=8&scope=bot%20applications.commands"
				),
			])
		]
	)

@client.command()
async def ping(ctx):
  message = await ctx.send(content="`Pinging...`")
  await message.edit(content=f"Latency is `{round(client.latency * 1000)}ms`")

@client.command()
async def about(ctx):
    servers = client.guilds
    guilds = len(client.guilds)
    servers.sort(key=lambda x: x.member_count, reverse=True)
    y = 0
    for x in client.guilds:
        y += x.member_count
    embed = discord.Embed(color=discord.Colour.blurple(),description=f"ViRTUCY SEC is Best anti nuke bot which prevents your server from any type of damage", timestamp=datetime.datetime.utcnow())
    embed.set_author(name=f"Bot Info", icon_url='https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif')
    embed.add_field(name="**General Statistics**", value=f"<a:arrows:948970252614635532> **USERS** :\n `{y}`\n<a:arrows:948970252614635532> **GUILDS** :\n `{guilds}`\n<a:arrows:948970252614635532> **Onwer** :\n <@806519089144135720> `~ Prasoon#5547`\n **Language** \n `Python`", inline=False)
    embed.add_field(name=f" **Prefix** :", value=f"`>`\n", inline=False)
    embed.set_footer(text="Made with 💖 by ~ Prasoon#5547 ")
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/949165203268993094/952455738050117663/discord-avatar-128-F27I2.gif')
    await ctx.send(embed=embed)


client.run(token)
        