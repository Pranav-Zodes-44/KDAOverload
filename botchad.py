from datapipelines import NotFoundError
import discord
from discord.ext import commands
import cassiopeia as cass
from league import League

with open('config.txt', 'r') as f:
    tokens = f.readlines()
    RIOT_TOKEN = tokens[0].strip()
    TOKEN = tokens[1].strip()
    
cass.set_riot_api_key(RIOT_TOKEN)

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
async def last(ctx, summ_name, region):
    await send_stats(ctx, summ_name, region)

async def send_stats(ctx, summoner_name, region):
    league = League()
    try:
        match = league.get_latest_normal_match(summoner_name=summoner_name, region=region)
    except NotFoundError as nfe:
        embed = discord.Embed(title="Summoner not found :(")
        embed.set_image(url="https://media.giphy.com/media/6uGhT1O4sxpi8/giphy.gif")
        await ctx.send(embed=embed)
        return
    except KeyError as ke:
        embed = discord.Embed(title="That's a wacky region you've entered there...", description="Even the Taliyah doesn't know where that place is!")
        embed.set_image(url="https://media.giphy.com/media/EjgA32SgtLpYAz2ZfB/giphy-downsized-large.gif")
        await ctx.send(embed=embed)
        return

    player = None

    for p in match.participants:
        if p.summoner.name == summoner_name:
            player = p
    #TODO:Get op.gg profile using region and summoner name for set_author
    # ^ op.gg/summoners/euw/Bodiez
    embed = discord.Embed(title="Latest normal match", description=f"""
    Champion: {player.champion.name}\n
    Kills: {player.stats.kills}\n
    Deaths: {player.stats.deaths}\n
    Assists: {player.stats.assists}\n
        """)
    embed.set_author(name=summoner_name, icon_url=player.summoner.profile_icon.url)
    embed.set_image(url=player.champion.image.url)

    await ctx.send(embed=embed)

bot.run(TOKEN)

