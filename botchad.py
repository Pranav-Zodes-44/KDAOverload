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
    

@bot.command(name="match_history", brief = "Shows your last 10 matches played. Defaulted to normal draft.")
async def match_history():
    league = League()

    matches = league.get_match_history()

    

    return

@bot.command(name="last", brief = "Shows your last match played. Defaulted to normal draft.", 
            description="Shows your last match played. Defaulted to normal draft.\n Queue types: ranked/solo/duo, flex, normal/draft, aram, clash.")
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
        await invalid_region(ctx, League(), embed)
        return

    await ctx.send("""
Getting the data from your last match.
One moment please... :clock:""")
    await send_stats_simple(ctx, summ_name, region, queue_type)

async def send_stats_simple(ctx, summoner_name, region, queue_type):
    league = League()

    queue: cass.Queue = League.get_queue_from_str(queue=queue_type)

    try:
        match = league.get_latest_match(summoner_name=summoner_name, region=region, queue=queue)
    except NotFoundError as nfe:
        embed = discord.Embed(title="Summoner not found :(")
        embed.set_image(url="https://media.giphy.com/media/6uGhT1O4sxpi8/giphy.gif")
        await ctx.send(embed=embed)
        return
    except KeyError as ke:
        embed = discord.Embed(title="That's a wacky region you've entered there...", 
                description="Even the Taliyah doesn't know where that place is!")
        await invalid_region(ctx, league, embed)
        return

    player = league.get_player_from_match(match=match, summoner_name=summoner_name)

    queue_str = league.get_str_from_queue(queue=queue)
    
    embed = get_embed_last(queue_str, player, league)
    
    embed.set_footer(text=get_footer_text(queue=queue, player=player))
    
    await ctx.send(embed=embed)


async def invalid_region(ctx, league: League, embed):
    embed.add_field(name="Regions", value=league.get_regions(), inline=False)
    embed.set_image(url="https://media.giphy.com/media/EjgA32SgtLpYAz2ZfB/giphy-downsized-large.gif")
    await ctx.send(embed=embed)

def get_embed_last(queue_str, player, league: League):

    opgg = f"https://op.gg/summoners/{league.region.lower()}/{player.summoner.name}"

    embed = discord.Embed(title=f"Latest {queue_str} match", description=f"""
    **Champion**: {player.champion.name}\n
    **Kills**: {player.stats.kills}\n
    **Deaths**: {player.stats.deaths}\n
    **Assists**: {player.stats.assists}\n
        """)
    embed.set_author(name=player.summoner.name, icon_url=player.summoner.profile_icon.url, 
                        url=opgg)
    embed.set_image(url=player.champion.image.url)

    return embed


def get_footer_text(queue: Queue, player):
    try:
        if queue == Queue.ranked_flex_fives:
            rank = player.summoner.ranks[Queue.ranked_flex_fives]
            lp = player.summoner.league_entries.flex.league_points
            return f"Level: {player.summoner.level} || Flex Rank: {rank.tier} {rank.division} {lp}LP"
        else:
            rank = player.summoner.ranks[Queue.ranked_solo_fives]
            lp = player.summoner.league_entries.fives.league_points
            return f"Level: {player.summoner.level} || Solo/Duo Rank: {rank.tier} {rank.division} {lp}LP"
    except KeyError as ke:
        if Queue.ranked_flex_fives in player.summoner.ranks.keys():
            rank = player.summoner.ranks[Queue.ranked_flex_fives]
            lp = player.summoner.league_entries.flex.league_points
            return f"Level: {player.summoner.level} || Flex Rank: {rank.tier} {rank.division} {lp}LP"
        else:
            return f"Level: {player.summoner.level} || Unranked"

#TODO: Brainstorm more commands


bot.run(TOKEN)

