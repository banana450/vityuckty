import os
import asyncio
import time
import datetime
import discord
import time
from discord.ext import commands
from discord.ext.commands.core import command
#from functions import *
import os
import discord
from discord.ext import commands, tasks
from asyncio import sleep
from discord.utils import get
import random
import asyncio
import json
import sys
from discord.utils import find
import datetime
import requests

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.emojis = True
intents.webhooks = True
intents = intents



class Antinuke(commands.Cog):
    def __init__(self, client):
        self.client = client


    #anti ban
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.ban).flatten()
            logs = logs[0]
            if logs.user.id == 877922339382243328 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
             await guild.unban(user=member, reason="Virtucy Security | Auto Recovery")
             await logs.user.ban(reason=f"Virtucy Security | Anti Ban")



    #@commands.Cog.listener()
   # async def on_guild_emojis_update(self, emoji):
           # guild = emoji.guild
           # logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.emoji_update).flatten()
          #  logs = logs[0]
          #  await logs.user.ban(reason=f"LuciferNukeZ | Anti Emoji Update")

    #@commands.Cog.listener()
    #async def on_guild_emoji_create(self, emoji):
           # guild = emoji.guild
          #  logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.emoji_create).flatten()
          #  logs = logs[0]
         #   await emoji.delete()
         #   await logs.user.ban(reason=f"LuciferNukeZ | Anti Emoji Create")

  #  @commands.Cog.listener()
   # async def on_guild_emojis_delete(self, emoji):
           # guild = emoji.guild
          #  logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.emoji_delete).flatten()
          #  logs = logs[0]
           # await logs.user.ban(reason=f"LuciferNukeZ | Anti Emoji Delete")

    #@commands.Cog.listener()
    #async def on_sticker_create(self, sticker):
            #guild = sticker.guild
          #  logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.sticker_create).flatten()
          #  logs = logs[0]
           # await sticker.delete()
         #   await logs.user.ban(reason=f" LuciferNukeZ | Anti Sticker Create")

   # @commands.Cog.listener()
    #async def on_sticker_update(self, sticker):
         #   guild = sticker.guild
          #  logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.sticker_update).flatten()
          #  logs = logs[0]
          #  await logs.user.ban(reason=f"LuciferNukeZ | Anti Update Create")

   # @commands.Cog.listener()
   # async def on_sticker_delete(self, sticker):
           # guild = sticker.guild
          #  logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.sticker_delete).flatten()
          #  logs = logs[0]
           # await logs.user.ban(reason=f"LuciferNukeZ | Anti Sticker Update")      

    #anti kick and anti prune
    @commands.Cog.listener()
    async def on_member_remove(self, member, guild):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.kick).flatten()
            logs = logs[0]
            if logs.user.id == 877922339382243328 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
             await logs.user.ban(reason=f"Neutron Security | Anti Kick")
            prunelogs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.kick).flatten()
            prunelogs = prunelogs[0]
            if logs.user.id == 877922339382243328 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
             await logs.user.ban(reason=f"Neutron Security | Anti Prune")

    #anti channel create
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            guild = channel.guild
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_create).flatten()
            logs = logs[0]
            if logs.user.id == 877922339382243328 or logs.user.id == 695090470908330079 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
              await channel.delete(reason="Virtucy Security | Auto Recovery")
              await logs.user.ban(reason=f"Virtucy Security | Anti Channel Create")  
              


    #anti channel delete
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            guild = channel.guild
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_delete).flatten()
            logs = logs[0]
            if logs.user.id == 877922339382243328 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
              await channel.clone(reason="Virtucy Security | Auto Recovery")
              await logs.user.ban(reason=f"Virtucy Security | Anti Channel Delete")

    @commands.Cog.listener()
    async def on_guild_emojis_delete(guild):
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.emoji_delete).flatten()
            logs = logs[0]
            await logs.user.ban(reason=f"Virtucy Security | Anti Emoji Delete")
  

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            guild = before.guild
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_update).flatten()            
            logs = logs[0]
            if logs.user.id == 877922339382243328 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
              await after.edit(name=f"{before.name}", nsfw=f"{before.nsfw}", reason="Virtucy Security | Auto Recovery")
              await logs.user.ban(reason=f"Virtucy Security | Anti Channel Update")





    #anti role create
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            guild = role.guild
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_create).flatten()
            logs = logs[0]
            if logs.user.id == 877922339382243328 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
              await role.delete(reason="Virtucy Security | Auto Recovery")
              await logs.user.ban(reason=f"Virtucy Security | Anti Role Create")




    #anti role delete
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            guild = role.guild
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_delete).flatten()
            logs = logs[0]
            if logs.user.id == 877922339382243328 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
              await logs.user.ban(reason=f"Virtucy Security | Anti Role Delete")

                        



    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            guild = before.guild
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_update).flatten()
            logs = logs[0]
            if logs.user.id == 877922339382243328 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
              await after.edit(name=f"{before.name}",  hoist=f"{before.hoist}", mentionable=f"{before.mentionable}", reason="Virtucy Security | Auto Recovery")
              await logs.user.ban(reason=f"Virtucy Security | Anti Role Update")


    #anti guild update
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            guild = before
            logs = await after.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2),  action=discord.AuditLogAction.guild_update).flatten()
            logs = logs[0]
            if logs.user.id == 877922339382243328 or logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
              await after.edit(name=f"{before.name}", description=f"{before.description}", vanity_code=f"{before.vanity_invite}")
              await logs.user.ban(reason="Virtucy Security | Anti Guild Update")

    #anti unban
    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.unban).flatten()
            logs = logs[0]
            if logs.user.id == 877922339382243328 or logs.user.id == 695090470908330079 or str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
              await logs.user.ban(reason=f"Virtucy Security | Anti Unban")

    @commands.Cog.listener()
    async def on_webhooks_update(self, webhook):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            guild = webhook.guild
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.webhook_update).flatten()
            cname = channel.name
            logs = logs[0]
            if str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
              requests.delete(webhook)
              await logs.user.ban(reason=f"Virtucy Security | Anti Webhook Update")

    @commands.Cog.listener()
    async def on_webhooks_create(self, channel):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            guild = channel.guild
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.webhook_create).flatten()
            logs = logs[0]
            if str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
              await logs.user.ban(reason=f"Virtucy Security | Anti Webhook Create")

      

    @commands.Cog.listener()
    async def on_webhooks_delete(self, webhook):
      with open('whitelisted.json') as f:
            whitelisted = json.load(f)
            guild = webhook.guild
            logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.webhook_delete).flatten()
            logs = logs[0]
            if str(logs.user.id) in whitelisted[str(guild.id)]:
              pass
            else:
              await logs.user.ban(reason=f"Virtucy Security | Anti Webhook Delete")
      
    #anti bot and anti alt
    @commands.Cog.listener()
    async def on_member_join(self, member):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
        guild = member.guild
        logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.bot_add).flatten()
        logs = logs[0]
        if logs.user.id == guild.owner.id or str(logs.user.id) in whitelisted[str(guild.id)]:
          pass
        else:
         if member.bot:
          await member.ban(reason="Virtucy Security | Anti Bot Add")
          await logs.user.ban(reason=f"Virtucy Security | Anti Bot Add")


    @commands.command(name="kick",
                      usage="<member> [reason]")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member.id == ctx.author.id:
            await ctx.send("You cannot kick yourself!")
            return
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 877922339382243328 or ctx.author.id == 695090470908330079:
         await member.kick(reason=reason)

         await ctx.message.delete()
         kick = discord.Embed(description=f"**A member has been kicked.**\n\n"
                                          f"Moderator: {ctx.author.mention}\n"
                                          f"Member: {member.mention}", colour=discord.Colour.blue())
         kick.add_field(name="Reason", value=reason, inline=False)
         await ctx.send(embed=kick)
    @commands.command(name="lock",
                      usage="[#channel/id]")
    @commands.has_permissions(manage_messages=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720:
         channel = channel or ctx.channel
         overwrite = channel.overwrites_for(ctx.guild.default_role)
         overwrite.send_messages = False
         await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
         await ctx.send(f"{channel.mention} locked!")
    @commands.command(name="unlock",
                      usage="[#channel/id]")
    @commands.has_permissions(manage_messages=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720:
          channel = channel or ctx.channel
          overwrite = channel.overwrites_for(ctx.guild.default_role)
          overwrite.send_messages = True
          await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
          await ctx.send(f"{channel.mention} unlocked!")
    @commands.command(name="role",
                      usage="<member> <role>")
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, addORremove, member: discord.Member, role: discord.Role):

        addORremove = addORremove.lower()

        if addORremove == 'add':

            if role == ctx.author.top_role:
                return await ctx.send("That role has the same position as your top role!")

            if role in member.roles:
                return await ctx.send("The member already has this role assigned!")

            if role.position >= ctx.guild.me.top_role.position:
                return await ctx.send(f"This role is higher than my role, move it to the top!")
            if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720:
              await member.add_roles(role)
              await ctx.send(f"I have added {member.mention} the role {role.mention}")

        if addORremove == 'remove':
           

            if role == ctx.author.top_role:
                return await ctx.send("That role has the same position as your top role!")

            if role not in member.roles:
                return await ctx.send("The member does not have this role!")

            if role.position >= ctx.guild.me.top_role.position:
                return await ctx.send(f"This role is higher than my role, move it to the top!")
            if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 806519089144135720 or ctx.author.id == 806519089144135720:
              await member.remove_roles(role)
              await ctx.send(f"I have removed {member.mention} the role {role.mention}") 
def setup(client):
    client.add_cog(Antinuke(client))



