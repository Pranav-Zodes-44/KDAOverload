import discord
from discord.ext import commands


with open('config.txt', 'r') as f:
    TOKEN = f.readlines()[1].strip()
    

bot = commands.Bot(command_prefix='!!')


@bot.event
async def on_ready():
    guild = None
    for guild_ in bot.guilds:
        if "test" in guild_.name:
            guild = guild_

    print(f"{bot.user} is connected to the following guild \n")
    print(f"{guild.name} ID: {guild.id}")

@bot.command(name="last")
async def last(ctx, summ_name):
    await ctx.send(f'Summoner name: {summ_name}')


bot.run(TOKEN)

