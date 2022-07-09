from league import League
import discord
from discord.ui import Button, View
import cassiopeia as cass
from cassiopeia import Queue

class BotHelper():

    def get_embed_last_simple(self, queue_str, player, match: cass.core.match, league: League):

        embed = discord.Embed(title=f"Latest {queue_str} match", description=f"""
        **Match Start**: 
        **Champion**: {player.champion.name}\n
        **Kills**: {player.stats.kills}\n
        **Deaths**: {player.stats.deaths}\n
        **Assists**: {player.stats.assists}\n
            """)
        embed = self.set_embed_author(player, embed, league)
        embed = self.set_embed_image(player, embed=embed)

        return embed
    
    def set_embed_author(self, player, embed: discord.Embed, league: League):
        opgg = f"https://op.gg/summoners/{league.region.lower()}/{player.summoner.name}"
        embed.set_author(name=player.summoner.name, icon_url=player.summoner.profile_icon.url, 
                            url=opgg)
        return embed

    def set_embed_image(self, player, embed: discord.Embed):
        embed.set_image(url=player.champion.image.url)
        return embed


    def get_footer_text(self, queue: Queue, player: cass.core.match.Participant):
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
            
    def get_opgg(self, player, league):
        url = f"https://op.gg/summoners/{league.region.lower()}/{player.summoner.name}"
        opgg = Button(label = "OP.GG", url = url)
        return View(opgg)