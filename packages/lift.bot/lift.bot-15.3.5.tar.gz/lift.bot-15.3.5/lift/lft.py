import discord
from discord.ext import commands

from lift.gradient import Colorate, Colors, Center
import lift.status
from urllib.request import urlopen


file_url = 'https://raw.githubusercontent.com/devliftz/lift.bot/main/version.txt'
dataver = urlopen(file_url).read(203).decode('utf-8')

bot = commands.AutoShardedBot(command_prefix="?", help_command=None, intents=discord.Intents().all(), shard_count=5)
print(Colorate.Horizontal(Colors.red_to_yellow, f"""


                                      ██╗     ██╗███████╗████████╗
                                      ██║     ██║██╔════╝╚══██╔══╝
                                      ██║     ██║█████╗     ██║   
                                      ██║     ██║██╔══╝     ██║   
                                      ███████╗██║██║        ██║   
                                      ╚══════╝╚═╝╚═╝        ╚═╝   
                                                
                                        
     ┌────────────────────────────────────────────────────────────────────────────────────────┐
                      Current Version: {dataver} | Discord: https://discord.gg/pupnvCNbwN
     └────────────────────────────────────────────────────────────────────────────────────────┘
     
     """))

@bot.event
async def on_command(ctx):
    print(Colorate.Horizontal(Colors.red_to_yellow, f"""
    ┌────────────────────────────────────────────────────┐
      Command: {ctx.command.name}
      Input: {ctx.message.content}
      Server: {ctx.author.guild.name} ID: {ctx.author.guild.id}
      User: {ctx.author.name}
    └────────────────────────────────────────────────────┘
    """))

@bot.event
async def on_shard_ready(shard_id):
    print(Colorate.Horizontal(Colors.red_to_yellow, f"""Shard {shard_id} started."""))

@bot.command()
async def shard(self, ctx, shard_id):
      if shard_id is None:
          shard_id = ctx.guild.shard_id
      info = await self.shard_info(shard_id)
      embed = discord.Embed(title="", description=f"""> **Shard** `{shard_id}` **has** `{info['guilds']}` **and** `{info['users']}` **users**""")
      await ctx.reply(embed=embed)

def login(token):
    bot.run(token=f"{token}", log_handler=None)