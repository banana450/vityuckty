import discord
from discord.ext import commands
from datetime import datetime
import json
from Tools.utils import getConfig


class AntiSpam(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
      with open('whitelisted.json') as f: 
        whitelisted = json.load(f)  
        try:
              if message.author.id == 806519089144135720 or message.author.id == 806519089144135720 or str(message.author.id) in whitelisted[str(message.guild.id)]:
                return
                try:
                        data = getConfig(message.guild.id)
                        antiSpam = data["antiSpam"]
                        antiLink = data["antiLink"]
                        punishment = data["punishment"]

                except AttributeError:
                        pass
                try:
                        if antiSpam is True:
                            def check(message):
                                return(message.author == message.author and (datetime.utcnow() - message.created_at).seconds < 15)

                            if message.author.guild_permissions.administrator:
                                return

                            if len(list(filter(lambda m: check(m), self.client.cached_messages))) >= 4 and len(list(filter(lambda m: check(m), self.client.cached_messages))) < 8:
                                pass
                            elif len(list(filter(lambda m: check(m), self.client.cached_messages))) >= 8:
                                if data["punishment"] == "kick":
                                    await message.author.kick(reason=f"ViRTUCY SEC | Anti Spam")

                                if data["punishment"] == "ban":
                                    await message.author.ban(reason=f"ViRTUCY SEC | Anti Spam")

                                if data["punishment"] == "none":
                                    return

                        if antiLink is True:
                            if message.author.guild_permissions.administrator:
                                return
                            if "https://" in message.content:
                                await message.delete()

                                if data["punishment"] == "kick":
                                    await message.author.kick(reason=f"ViRTUCY SEC | Anti Link")

                                if data["punishment"] == "ban":
                                    await message.author.ban(reason=f"ViRTUCY SEC | Anti Link", delete_message_days=0)

                                else:
                                    await message.author.kick(reason=f"ViRTUCY SEC | Anti Link")


                except UnboundLocalError:
                        pass

        except discord.errors.NotFound:
            pass


def setup(client):
    client.add_cog(AntiSpam(client))