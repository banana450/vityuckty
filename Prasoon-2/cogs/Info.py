# -*- coding: utf-8 -*-

import contextlib
import timezone

import datetime
import aiohttp
import utilities as tragedy
import dateutil.parser
import discord
import humanize
from discord.activity import *
from discord.colour import Color
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Info(commands.Cog, description="Commands that return information"):
	def __init__(self, bot):
		self.bot = bot
		self.aiohttp = aiohttp.ClientSession(headers={"X-Tragedy-Task": "Info Cog"})

	@commands.command(aliases=["ui", "userinfo"],description="you know what this does dont play stupid", help="whois [member]")
	@commands.cooldown(1, 5, type=BucketType.member)
	async def whois(self, ctx, member: commands.MemberConverter = None):
		member = member if member != None else ctx.author
		roleNameList = list(
			role.mention for role in member.roles if role != ctx.guild.default_role)
		# userProfile = await self.bot.fetch_user_profile(member.id) User profile has been depracated since v1.7
		# externalAccounts = list("Type: {} - Username: {}".format(external.get("type", "Error"), external.get("name", "Error")) for external in await userProfile.connected_accounts) User profile has been depracated since v1.7
		embed = discord.Embed(color=Color.blurple())
		embed.set_author(name="{}".format(
			member), icon_url=member.avatar_url)
		embed.add_field(name="Basic Info",
						value="Joined Server At - {} <t:{}:R>\nRegistered on Discord At - {} <t:{}:R>".format(
							humanize.naturaldate(member.joined_at),
							int(member.joined_at.timestamp()),
							humanize.naturaldate(member.created_at),
							int(member.created_at.timestamp())))
		embed.add_field(name="Status Info (Buggy)",
						value="Desktop Status - {}\nMobile Status - {}\nWeb Application Status - {}".format(
							tragedy.HumanStatus(str(member.desktop_status)),
							tragedy.HumanStatus(str(member.mobile_status)),
							tragedy.HumanStatus(str(member.web_status))), inline=False)
		embed.add_field(name="Role Info", value="Top Role - {}\nRole(s) - {}".format(
			member.top_role.mention if member.top_role != ctx.guild.default_role else "None",
			', '.join(roleNameList) if roleNameList != [] else "None"), inline=False)
		embed.add_field(name="Flags",
						value="{} - Discord Staff\n{} - Discord Partner\n{} - Verified Bot Developer".format(tragedy.EmojiBool(member.public_flags.staff), tragedy.EmojiBool(member.public_flags.partner), tragedy.EmojiBool(member.public_flags.verified_bot_developer)))
		# embed.add_field(name="Other Info", value="HypeSquad House - {}\nUser has Nitro - {}\nConnected Accounts - {}".format(str(userProfile.hypesquad_houses).title(), tragedy.EmojiBool(await userProfile.nitro), ', '.join(externalAccounts).removeprefix(', ') if externalAccounts != [] else "None")) User profile has been depracated since v1.7
		embed.set_footer(icon_url=ctx.author.avatar_url, text='Requested By: {}'.format(ctx.author.name))
		await ctx.reply(embed=embed, mention_author=True)

	@commands.command(aliases=["guild", "si", "serverinfo", "guildinfo"], description="Returns info about current guild", help="serverinfo")
	@commands.cooldown(1, 5, type=BucketType.member)
	async def server(self, ctx):
		findbots = sum(1 for member in ctx.guild.members if member.bot)
		vanity = "VANITY_URL" in str(ctx.guild.features)
		splash = "INVITE_SPLASH" in str(ctx.guild.features)
		animicon = "ANIMATED_ICON" in str(ctx.guild.features)
		discoverable = "DISCOVERY" in str(ctx.guild.features)
		banner = "BANNER" in str(ctx.guild.features)
		vanityFeature = "{} - Vanity URL".format(tragedy.EmojiBool(vanity)) if not vanity else "{} - Vanity URL ({})".format(tragedy.EmojiBool(vanity), str(await ctx.guild.vanity_invite())[15:])
		embed = discord.Embed(title='{}'.format(ctx.guild.name), colour=Color.blurple())
		embed.set_thumbnail(url=ctx.guild.icon_url)
		embed.add_field(name="Members", value="Bots: {}\nHumans: {}\nOnline Members: {}/{}".format(str(findbots), ctx.guild.member_count - findbots, sum( member.status != discord.Status.offline and not member.bot for member in ctx.guild.members), str(ctx.guild.member_count)))
		embed.add_field(name="Channels", value="<:BurpleChannel:948969655689707600>Text Channels: {}\n<:blurple_vc:950358293203804210>Voice Channels: {}".format(len(ctx.guild.text_channels), len(ctx.guild.voice_channels)), inline=False)
		embed.add_field(name="Important Info", value="Owner: {}\nVerification Level: **{}**\nGuild ID: **{}**".format(ctx.guild.owner.mention, str(ctx.guild.verification_level).title( ), ctx.guild.id), inline=False)
		embed.add_field(name="Other Info", value="AFK Channel: {}\nAFK Timeout: {} minute(s)\nCustom Emojis: {}\nRole Count: {}\nFilesize Limit - {}".format( ctx.guild.afk_channel, str(ctx.guild.afk_timeout / 60), len(ctx.guild.emojis), len(ctx.guild.roles), humanize.naturalsize(ctx.guild.filesize_limit)), inline=False)
		embed.add_field(name="Server Features", value="{} - Banner\n{}\n{} - Splash Invite\n{} - Animated Icon\n{} - Server Discoverable".format(tragedy.EmojiBool(banner), vanityFeature, tragedy.EmojiBool(splash), tragedy.EmojiBool(animicon), tragedy.EmojiBool(discoverable)))
		embed.add_field(name="Boost Info", value="Number of Boosts - **{}**\nBooster Role - **{}**\nBoost Level/Tier - **{}**".format( str(ctx.guild.premium_subscription_count), ctx.guild.premium_subscriber_role.mention if ctx.guild.premium_subscriber_role != None else ctx.guild.premium_subscriber_role, ctx.guild.premium_tier), inline=False)
		await ctx.reply(embed=embed, mention_author=True)


	@commands.command(name="role", aliases=['ri', 'roleinfo'], description="Returns info about specified role",
					  help="role <role>")
	@commands.cooldown(1, 5, BucketType.member)
	async def _role(self, ctx: commands.Context, role: commands.RoleConverter):
		async with ctx.typing():
			embed = discord.Embed(title=role.name, color=Color.blurple())
			embed.add_field(name="Basic Info",
							value="Role Name - {}\nRole ID - {}\nCreated At - {} (<t:{}:R>)".format(role.name, role.id, humanize.naturaldate(role.created_at), int(role.created_at.timestamp())))
			embed.add_field(name="Features",
							value="Mentionable - {}\nBot Role - {}\nManaged by Integration - {}\nBooster Role - {}\nDefault Role - {}".format(tragedy.EmojiBool(role.mentionable), tragedy.EmojiBool(role.is_bot_managed()), tragedy.EmojiBool(role.managed), tragedy.EmojiBool(role.is_premium_subscriber()), tragedy.EmojiBool(role.is_bot_managed())), inline=False)
			await ctx.reply(embed=embed, mention_author=True)

	@commands.command(aliases=['pfp', 'avatar'], description="you know what this does too", help="av [member]")
	@commands.cooldown(1, 5, type=BucketType.member)
	async def av(self, ctx, member: commands.MemberConverter = None):
		member = member if member != None else ctx.author
		embed = discord.Embed(color=Color.blurple())
		embed.set_image(url=member.avatar_url)
		embed.set_footer(text="{}'s Avatar".format(member))
		await ctx.reply(embed=embed, mention_author=True)



def setup(bot):
	bot.add_cog(Info(bot))