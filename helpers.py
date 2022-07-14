from league import League
import discord
from discord.ui import Button, View
import cassiopeia as cass
from cassiopeia import Queue
import json

class BotHelper():

    def get_embed_last_simple(self, queue, player, match: cass.core.match, league: League):
        
        embed = discord.Embed(title=f"Latest {League().get_str_from_queue(queue)} match", description=f"""
    **Match start**: {match.start.shift(hours=+2).format('DD-MM-YYYY HH:mm')}\n
        """)
        embed = self.set_embed_author(player, embed, league)
        embed = self.set_embed_image(player, embed=embed)

        embed.add_field(name="Champion:", value = player.champion.name, inline=True)
        embed.add_field(name="KDA:", value = f"{player.stats.kills}/{player.stats.deaths}/{player.stats.assists}", inline=True)
        embed.add_field(name="Result:", value=f"{self.get_result(player)}", inline=True)
        embed = self.get_embed_items(player, embed)

        embed.set_footer(text=self.get_footer_text(queue, player))
        
        return embed
    
    def get_embed_items(self, player: cass.core.match.Participant, embed):

        items_emojis = ""
        player_items = League().get_player_items(player)


        with open("items.json", "r") as f:
            emoji_ids = json.load(f)
        
        for item in player_items[:-1]:
            if not item == None:
                items_emojis += f"{emoji_ids[str(item.id)]} "

        embed.add_field(name="Items:", value=items_emojis, inline=True)

        trinket = player_items[-1]

        if trinket != None:
            embed.add_field(name="Trinket: ", value=emoji_ids[str(player_items[-1].id)], inline=True)


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

    def get_result(self, player: cass.core.match.Participant):
        return "Win :white_check_mark:" if player.team.win else "Loss :x:"