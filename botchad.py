from datapipelines import NotFoundError
import discord
from discord.ext import commands
import cassiopeia as cass
from cassiopeia import Queue
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
async def last(ctx, summ_name=None, region=None, queue_type = None):
    #TODO: add support for full or simple
    #Full = Full match stats (all summoners)
    #Simple = Simmilar to what we have now, just with more stats.

    if summ_name == None and region == None:
        embed = discord.Embed(title="Not enough arguments provided",
        description= """
    You left out your summoner name and region :( 

    Correct format: **!!last [summoner_name] [region]**""")
        await ctx.send(embed=embed)
        return
    elif region == None:
        embed = discord.Embed(title="You left out the region!", description="Correct format: **!!last [summoner_name] [region]**")
        await ctx.send(embed=embed)
        return

    await ctx.send("""
Getting the data from your last match.
One moment please... :clock:""")
    await send_stats(ctx, summ_name, region, queue_type)

async def send_stats(ctx, summoner_name, region, queue_type):
    league = League()

    try:
        queue: cass.Queue = League.get_queue_from_str(queue=queue_type)
    except KeyError as ke:
        queue = cass.Queue.normal_draft_fives

    try:
        #Parse through queue type here as param. 
        match = league.get_latest_match(summoner_name=summoner_name, region=region, queue=queue)
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
    

    if queue == Queue.ranked_flex_fives:
        rank = player.summoner.ranks[Queue.ranked_flex_fives]
        lp = player.summoner.league_entries.flex.league_points
    else:
        rank = player.summoner.ranks[Queue.ranked_solo_fives]
        lp = player.summoner.league_entries.fives.league_points

    queue_str = league.get_str_from_queue(queue=queue)

    #TODO:Get op.gg profile using region and summoner name for set_author
    # ^ op.gg/summoners/euw/Bodiez
    embed = discord.Embed(title=f"Latest {queue_str} match", description=f"""
    **Champion**: {player.champion.name}\n
    **Kills**: {player.stats.kills}\n
    **Deaths**: {player.stats.deaths}\n
    **Assists**: {player.stats.assists}\n
        """)
    embed.set_author(name=summoner_name, icon_url=player.summoner.profile_icon.url)
    embed.set_image(url=player.champion.image.url)
    embed.set_footer(text=f"Level: {player.summoner.level} || Solo/Duo Rank: {rank.tier} {rank.division} {lp}LP")

    await ctx.send(embed=embed)


#TODO: Brainstorm more commands


bot.run(TOKEN)

