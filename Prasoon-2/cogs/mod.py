# -*- coding: utf-8 -*-

import asyncio
import collections
import contextlib
from datetime import datetime, timezone
import pprint
import random
import string
import typing
import time

from discord.embeds import Embed

import utilities as tragedy
import classes as classes
import discord
import humanize
import nanoid
import pymysql.cursors
from classes import WelcomeNotConfigured
from discord.channel import DMChannel
from discord.colour import Color
from discord.ext import commands, tasks
from discord.ext.commands.converter import TextChannelConverter
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.errors import BadArgument
from discord.permissions import Permissions
from discord_components import *
from discord_components.component import Button, ButtonStyle


class Mod(commands.Cog, description="Commands to moderate your server !"):
	def __init__(self, bot):
		self.bot = bot
		self.snipe_cache = collections.defaultdict(dict)
		self.edit_cache = collections.defaultdict(dict)
		DiscordComponents(self.bot)



	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if message.author.bot is False and isinstance(message.channel, DMChannel) is not True:
			self.snipe_cache[message.channel.id] = message

	@commands.Cog.listener()
	async def on_message_edit(self, before: discord.Message, after: discord.Message):
		if after.author.bot is False and isinstance(after.channel, DMChannel) is not True:
			self.edit_cache[after.channel.id] = {
				"before": before, "after": after
			}

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 10, commands.BucketType.member)
	@commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
	async def snipe(self, ctx):
		if not ctx.channel.id in self.snipe_cache:
			return await ctx.send('Nothing to snipe.')
		data: discord.Message = self.snipe_cache[ctx.channel.id]
		time = data.created_at
		embed = discord.Embed(color=Color.blurple(), timestamp=time)
		embed.set_author(name=data.author.name,
						 icon_url=data.author.avatar_url)
		if data.content:
			embed.description = data.content
		if data.attachments:
			if str(data.attachments[0].filename).lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
				embed.set_image(
					url="attachment://{}".format(data.attachments[0].filename))
				embed.set_footer(text='Sniped message sent at {}'.format(
					time.strftime("%I:%M %p")))
				del self.snipe_cache[ctx.channel.id]
				return await ctx.send(embed=embed, file=await data.attachments[0].to_file())
		del self.snipe_cache[ctx.channel.id]
		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 10, commands.BucketType.member)
	@commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
	async def editsnipe(self, ctx):
		if not ctx.channel.id in self.edit_cache:
			return await ctx.send('Nothing to snipe.')

		before: discord.Message = self.edit_cache[ctx.channel.id]["before"]
		after: discord.Message = self.edit_cache[ctx.channel.id]["after"]
		edited_at = after.created_at

		embed = discord.Embed(color=Color.blurple(), timestamp=edited_at)
		embed.set_author(name=after.author,
						 url=after.jump_url,
						 icon_url=after.author.avatar_url)
		if after.content:
			embed.add_field(
				name="Before", value=before.clean_content, inline=False)
			embed.add_field(
				name="After", value=after.clean_content, inline=False)
		del self.edit_cache[ctx.channel.id]

		await ctx.send(embed=embed)

	@commands.command()
	@commands.has_permissions(manage_emojis=True)
	async def steal(self, ctx: commands.Context, emoji: commands.EmojiConverter):
		emoji: discord.Emoji = emoji
		await ctx.guild.create_custom_emoji(name=emoji.name, reason="tragedy Emoji Steal", image=await emoji.url.read())
		await ctx.send(embed=discord.Embed(
			title="Emoji Steal",
			color=Color.blurple(),
			description="{} added with name `:{}:`".format(emoji, emoji.name)
		))

	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	@commands.bot_has_guild_permissions(manage_messages=True)
	@commands.cooldown(1, 15, type=BucketType.member)
	@commands.group(invoke_without_command=True)
	async def purge(self, ctx, amount: typing.Optional[int] = 5):
		await ctx.message.delete()
		await ctx.channel.purge(limit=amount)
		temp = await ctx.send(">>> Purged `{}` Messages".format(amount))
		await asyncio.sleep(5)
		await temp.delete()

	@purge.command(name='until')
	async def _until(self, ctx, message: commands.MessageConverter):
		await ctx.message.delete()
		await ctx.channel.purge(after=message)

	@purge.command(name='user')
	async def _user(self, ctx, user: commands.MemberConverter, amount: typing.Optional[int] = 100):
		def check(msg):
			return msg.author.id == user.id

		await ctx.channel.purge(limit=amount, check=check, before=None, bulk=True)

	@purge.command(name="all")
	async def _all(self, ctx: commands.Context):
		def check(response):
			return ctx.author == response.user and response.channel == ctx.channel

		Confirm = await ctx.reply(embed=discord.Embed(title="Are you sure?", description="This will delete **every message** in this channel.", color=Color.blurple()), mention_author=True, components=[
			[
				Button(style=ButtonStyle.green, label="Yes"),
				Button(style=ButtonStyle.red, label="No")
			]
		])

		try:
			interaction = await self.bot.wait_for("button_click", check=check, timeout=15)
			if interaction.component.label == "Yes":
				try:
					await Confirm.delete()
					position_index = ctx.channel.position
					await ctx.channel.delete()
					clone = await ctx.channel.clone()
					await clone.edit(position=position_index)
					try:
						await clone.send(embed=discord.Embed(title="Channel Nuked!",
														   description="Type \"{}help\" for commands.".format(
															   random.choice(tragedy.getServerPrefixes(ctx.guild.id))),
														   color=discord.Color.blurple()).set_image(
							url='https://media.giphy.com/media/HhTXt43pk1I1W/source.gif'), delete_after=5)
					except Exception as exc:
						tragedy.logError(exc)
				except discord.Forbidden:
					raise commands.BotMissingPermissions(["manage_channels"])
			else:
				await Confirm.delete()
				await ctx.message.delete()
				return
		except asyncio.exceptions.TimeoutError:
			await Confirm.edit(content="Took too long !", embed=None, components=[])    

	@commands.command()
	async def nuke(self, ctx: commands.Context):
		def check(response):
			return ctx.author == response.user and response.channel == ctx.channel

		Confirm = await ctx.reply(embed=discord.Embed(title="Are you sure?", description="This will **Nuke** this channel.", color=Color.red()), mention_author=True, components=[
			[
				Button(style=ButtonStyle.green, label="Yes"),
				Button(style=ButtonStyle.red, label="No")
			]
		])

		try:
			interaction = await self.bot.wait_for("button_click", check=check, timeout=15)
			if interaction.component.label == "Yes":
				try:
					await Confirm.delete()
					position_index = ctx.channel.position
					await ctx.channel.delete()
					clone = await ctx.channel.clone()
					await clone.edit(position=position_index)
					try:
						await clone.send(embed=discord.Embed(title="Channel Nuked!",
														   description="Type \"{}help\" for commands.".format(
															   random.choice(tragedy.getServerPrefixes(ctx.guild.id))),
														   color=discord.Color.blurple()).set_image(
							url='https://media.giphy.com/media/HhTXt43pk1I1W/source.gif'), delete_after=5)
					except Exception as exc:
						tragedy.logError(exc)
				except discord.Forbidden:
					raise commands.BotMissingPermissions(["manage_channels"])
			else:
				await Confirm.delete()
				await ctx.message.delete()
				return
		except asyncio.exceptions.TimeoutError:
			await Confirm.edit(content="Took too long !", embed=None, components=[])        