#%%

from datapipelines import NotFoundError
import discord
from discord.ext import commands
from helpers import AdvancedStats, BotHelper as bh
from views import AdvancedView as av
import cassiopeia as cass
from cassiopeia import datastores
from league import League


with open('config.txt', 'r') as f:
    tokens = f.readlines()
    RIOT_TOKEN = tokens[0].strip()
    TOKEN = tokens[1].strip()
    
cass.set_riot_api_key(RIOT_TOKEN)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!!"), intents = intents, debug_guilds = [852520045359005716, 400008732425191427])

regions = ["EUW", "EUNE", "NA", "BR", "TR", "LAN", "LAS", "JP", "KR", "RU", "OCE"]
queue_types = ["normal", "flex", "solo/duo", "aram", "clash"]


@bot.event
async def on_ready():

    print("Bot connected.")


@bot.slash_command(
    name="match-history", 
    description= "Shows your last 10 matches played. Defaulted to normal draft.", 
    guild_ids = [852520045359005716, 400008732425191427]
    )
async def slash_match_history(
    ctx: discord.ApplicationContext, 
    summoner_name: discord.Option(name ="summoner-name", input_type=str, description="Your summoner name", required = True), 
    region: discord.Option(name= "region", input_type=str, description="The region you play on", required = True, choices = regions),
    queue_type: discord.Option(name="queue-type", input_type=str, description="Which queue you want to get your match history from.", required = True, choices = queue_types)
):

    if region == None:
        embed = discord.Embed(title="You left out the region!", description="Correct format: **!!last [summoner_name] [region]**")
        await invalid_region(ctx, League(), embed)
        return

    await ctx.respond("Getting match history... Give me a second, this takes some time ;_;")


    league = League()

    queue = league.get_queue_from_str(queue=queue_type)
    queue_str = league.get_str_from_queue(queue=queue)

    matches = league.get_match_history(summoner_name=summoner_name, region=region, queue=queue)

    description = ""

    # match = league.get_latest_match(summoner_name=summoner_name, region=region, queue=queue)
    for i in range(10):
        p = league.get_player_from_match(match=matches[i], summoner_name=summoner_name)
        if p.team.win:
            result = ":white_check_mark:"
        else:
            result = ":x:"
        description += f"{result} Champion: {p.champion.name} | KDA: {p.stats.kills}/{p.stats.deaths}/{p.stats.assists}\n"

    embed = discord.Embed(title=f"{queue_str} Match History", description=description)
    embed = bh().set_embed_author(p, embed, league)
    embed.set_footer(text = bh().get_footer_text(queue=queue, player=p))
    await ctx.send_followup(
        embed=embed, 
        view = bh().get_opgg(p, league)
        )


@bot.command(name="match_history", description= "Shows your last 10 matches played. Defaulted to normal draft.")
async def match_history(ctx, summoner_name = None, region = None, queue_type = None):

    if summoner_name == None and region == None:
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

    await ctx.send("Getting match history... Give me a second, this takes some time ;_;")

    league = League()

    queue = league.get_queue_from_str(queue=queue_type)
    queue_str = league.get_str_from_queue(queue=queue)
    matches = league.get_match_history(summoner_name=summoner_name, region=region, queue=queue)

    description = ""

    for i in range(10):
        p = league.get_player_from_match(match=matches[i], summoner_name=summoner_name)
        if p.team.win:
            result = ":white_check_mark:"
        else:
            result = ":x:"
        description += f"{result} Champion: {p.champion.name} | KDA: {p.stats.kills}/{p.stats.deaths}/{p.stats.assists}\n"

    embed = discord.Embed(title=f"{queue_str} Match History", description=description)
    embed = bh().set_embed_author(p, embed, league)
    embed.set_footer(text = bh().get_footer_text(queue=queue, player=p))

    await ctx.send(embed=embed, view = bh().get_opgg(player=p, league=league))


last = bot.create_group("last","Shows your last match played. Defaulted to normal draft.")

@last.command(description="Shows a simplified version of your last match. Defaulted to normal draft.")
async def simple(
    ctx: discord.ApplicationContext, 
    summoner_name: discord.Option(name ="summoner-name", input_type=str, description="Your summoner name", required = True), 
    region: discord.Option(name= "region", input_type=str, description="The region you play on", required = True, choices = regions),
    queue_type: discord.Option(name="queue-type", input_type=str, description="Which queue you want to get your match history from.", required = True, choices = queue_types)
):
    await ctx.respond("""
    Getting the data from your last match.
One moment please... :clock:""")
    await send_stats(ctx, summoner_name, region, queue_type, full = False)


@last.command(description="Shows a detailed version of your last match. Defaulted to normal draft.")
async def full(
    ctx: discord.ApplicationContext, 
    summoner_name: discord.Option(name ="summoner-name", input_type=str, description="Your summoner name", required = True), 
    region: discord.Option(name= "region", input_type=str, description="The region you play on", required = True, choices = regions),
    queue_type: discord.Option(name="queue-type", input_type=str, description="Which queue you want to get your match history from.", required = True, choices = queue_types)
    ):
    discord.OptionChoice

    try:
        await ctx.respond("""
    Getting the data from your last match.
One moment please... :clock:""")
        await send_stats(ctx, summoner_name, region, queue_type, full = True)
    except datastores.riotapi.common.APIError as e:
        await ctx.send_followup("Rate Limit! Please try again in a minute... :(")


async def send_stats(ctx: discord.ApplicationContext, summoner_name, region, queue_type, full: bool):
    league = League()

    queue: cass.Queue = league.get_queue_from_str(queue=queue_type)

    latest_match = await get_latest_match(ctx=ctx, summoner_name=summoner_name, region=region, queue=queue, league=league)

    if latest_match == None:
        return


    player = league.get_player_from_match(match=latest_match, summoner_name=summoner_name)
    
    view = bh().get_opgg(player=player, league=league)

    if full == True:
        embed = AdvancedStats(queue, player, latest_match, league).get_embed_last()
    else:
        embed = bh().get_embed_last_simple(queue, player, latest_match, league)
    
    

    if (type(ctx) == discord.ApplicationContext):
        if full:
            await ctx.edit(content="Done!\nHere it is:", embed=embed, view = av(queue=queue, player=player, match=latest_match, league=league))
        else:
            await ctx.edit(content="Done!\nHere it is:", embed=embed, view = view)
    else:
        if full:
            await ctx.send(embed=embed, view = av(queue=queue, player=player, match=latest_match, league=league))
        else:
            await ctx.send(embed=embed, view = view)


async def get_latest_match(ctx ,summoner_name, region, queue, league):
    
    try:
        match = league.latest_match(summoner_name=summoner_name, region=region, queue=queue)
        return match
    except NotFoundError as nfe:
        embed = discord.Embed(title="Summoner not found :(")
        embed.set_image(url="https://media.giphy.com/media/6uGhT1O4sxpi8/giphy.gif")
        if (type(ctx) == discord.ApplicationContext):
            await ctx.send_followup(embed=embed)
        else:
            await ctx.send(embed=embed)
        return None
    except KeyError as ke:
        embed = discord.Embed(title="That's a wacky region you've entered there...", 
                description="Even the Taliyah doesn't know where that place is!")
        await invalid_region(ctx, league, embed)
        return None


async def invalid_region(ctx, league: League, embed):
    embed.add_field(name="Regions", value=league.get_regions(), inline=False)
    embed.set_image(url="https://media.giphy.com/media/EjgA32SgtLpYAz2ZfB/giphy-downsized-large.gif")
    await ctx.send(embed=embed)


#TODO: Brainstorm more commands

bot.run(TOKEN)
# %%
