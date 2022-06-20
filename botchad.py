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
    #TODO: Try except for KeyErro for region, sends invalid region if thrown
    #TODO: Try except for NotFoundError for summoner_name, sends invalid summoner name if thrown
    # if "league" in ctx.name:
    league = League()
    match = league.get_latest_normal_match(summoner_name=summoner_name, region=region)

    player = None

    for p in match.participants:
        if p.summoner.name == summoner_name:
            player = p

    message = f"""Your stats from the last normal game: \n
    Summoner: {summoner_name}\n
    Champion: {player.champion.name}\n
    Kills: {player.stats.kills}\n
    Deaths: {player.stats.deaths}\n
    Assists: {player.stats.assists}\n
        """

    await ctx.send(message)


bot.run(TOKEN)

