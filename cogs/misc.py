from discord.ext import commands
import discord
import datetime
import json
import os
import requests

start_time = datetime.datetime.utcnow()

URBAN_API_KEY = os.getenv('URBAN_API_KEY')

class misc(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

 # @commands.command()
  #async def info(self, ctx):
    #servers = self.bot.guilds
   # guilds = len(self.bot.guilds)
   # servers.sort(key=lambda x: x.member_count, reverse=True)
   # y = 0
   # for x in self.bot.guilds:
       # y += x.member_count
   # embed = discord.Embed(description=f"{client.user.name} is An Anti Nuke bot which protects your server from any type of damage", timestamp=datetime.datetime.utcnow())
   # embed.set_author(name=f"Cristal Security", icon_url='https://media.discordapp.net/attachments/973853810265042987/994237629124051055/20220706_191455.jpg') #guild count ={guilds} #userscount = {y}
    #embed.add_field(name="**General Sta**", value=f"<a:HM_success:981472084360327178> **USERS** :\n `{y}`\n<a:HM_success:981472084360327178> **GUILDS** :\n `{guilds}`\n<a:HM_success:981472084360327178> Creators -\n [Abhee](https://discord.com/users/957573048712712294) \n <a:HM_success:981472084360327178> **LANGUAGE** \n `Python 1.7.3`", inline=False)
    #embed.add_field(name=f"<a:HM_success:981472084360327178> **Prefix** :", value=f"`#`\n", inline=False)
    #embed.set_footer(text="Made by Abhee")
    #embed.set_thumbnail(url='https://media.discordapp.net/attachments/973853810265042987/994237629124051055/20220706_191455.jpg')
   # await ctx.send(embed=embed)




