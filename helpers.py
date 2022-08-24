from league import League
import discord
from discord.ui import Button, View
import cassiopeia as cass
from cassiopeia import Queue
import json
from tabulate import tabulate

class BotHelper():

    def check_overwrite(self, reaction):

        if reaction == None:
            return None
        
        if reaction == "👍":
            return True
            
        elif reaction == "👎":
            return False

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

        items_emojis = self.get_items(player)


        player_items = League().get_player_items(player)

        with open("items.json", "r") as f:
            emoji_ids = json.load(f)

        embed.add_field(name="Items:", value=items_emojis, inline=True)

        trinket = player_items[-1]

        if trinket != None:
            embed.add_field(name="Trinket: ", value=emoji_ids[str(player_items[-1].id)], inline=True)

        return embed

    def get_items(self, player: cass.core.match.Participant):

        items_emojis = ""
        player_items = League().get_player_items(player)

        with open("items.json", "r") as f:
            emoji_ids = json.load(f)
        
        for item in player_items[:-1]:
            if not item == None:
                items_emojis += f"{emoji_ids[str(item.id)]} "

        return items_emojis


    def set_embed_author(self, player, embed: discord.Embed, league: League):
        if " " in player.summoner.name:
            name = []
            name = player.summoner.name.split(" ")
            opgg_name = ""
            for word in name:
                if name.index(word) != (len(name) - 1):
                    opgg_name += word + "%20"
                else:
                    opgg_name += word
            opgg = f"https://op.gg/summoners/{league.region.lower()}/{opgg_name}"
        else:
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

                #Returns "" if player is not in promos
                promos = self.promos_text(player.summoner.league_entries.flex.promos)

                if promos == "":
                    return f"Level: {player.summoner.level} || Flex Rank: {rank.tier} {rank.division} {lp}LP"
                else:
                    return f"""Level: {player.summoner.level} |  36326      35923
Nekotaryoz         24199      31532| Flex Rank: {rank.tier} {rank.division} {lp}LP
                       Promos: {promos}"""
            else:
                rank = player.summoner.ranks[Queue.ranked_solo_fives]
                lp = player.summoner.league_entries.fives.league_points
                promos = self.promos_text(player.summoner.league_entries.fives.promos)

                if promos == "":
                    return f"""Level: {player.summoner.level} || Solo/Duo Rank: {rank.tier} {rank.division} {lp}LP"""
                else:
                    return f"""Level: {player.summoner.level} || Solo/Duo Rank: {rank.tier} {rank.division} {lp}LP
                       Promos: {promos}"""

        except KeyError as ke:
            if Queue.ranked_flex_fives in player.summoner.ranks.keys():
                rank = player.summoner.ranks[Queue.ranked_flex_fives]
                lp = player.summoner.league_entries.flex.league_points
                promos = self.promos_text(player.summoner.league_entries.flex.promos)

                if promos == "":
                    return f"Level: {player.summoner.level} || Flex Rank: {rank.tier} {rank.division} {lp}LP"
                else:
                    return f"""Level: {player.summoner.level} || Flex Rank: {rank.tier} {rank.division} {lp}LP
                       Promos: {promos}"""
            else:
                return f"Level: {player.summoner.level} || Unranked"
        except ValueError as ve:
            return f"Level: {player.summoner.level} || Unranked"

    
    def promos_text(self, promos):

        win = "✅ | "
        loss = "❌ | "

        p_text = ""

        if promos != None:
            
            progress = promos.progress
            games_played = len(progress)


            for game in progress:
                
                if game:
                    p_text += win
                else:
                    p_text += loss

            for i in range((5-games_played)):
                p_text += "- | "

        return p_text

            
    def get_opgg(self, player, league):
        
        url = f"https://op.gg/summoners/{league.region.lower()}/{player.summoner.name}"
        opgg = Button(label = "OP.GG", url = url)

        return View(opgg)

    def get_result(self, player: cass.core.match.Participant):
        return "Win :white_check_mark:" if player.team.win else "Loss :x:"


    #Add gold to advanced stats

class AdvancedStats():

    '''
    TODO: Look at creating a parent class for all these classes? 
          Maybe move the embed_last_full to the AdvancedStats() class, and have the following classes inherit from that
          Instead of setting different instance variables for each inner class
    '''

    def __init__(self, queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, league: League):
        self.queue = queue
        self.player = player
        self.match = match
        self.league = league

    def get_embed_last(self):

        bh = BotHelper()

        queue_str = self.league.get_str_from_queue(queue=self.queue)

        embed = discord.Embed(title=f"Latest {queue_str} match")
        embed = bh.set_embed_author(self.player, embed, self.league)
        embed = self.add_blue_team(embed)
        embed = self.add_red_team(embed)
       
        embed.set_footer(text=bh.get_footer_text(queue=self.queue, player=self.player))

        return embed
    

    def add_blue_team(self, embed: discord.Embed):

        blue_team = []

        for p in self.match.blue_team.participants:
            s = p.stats
            name, kills, deaths, assists, cs = p.summoner.name, s.kills, s.deaths, s.assists, s.total_minions_killed
            blue_team.append([name, kills, deaths, assists, cs])
            
        blue_team_table = tabulate(
            #Add "Champion" with champion icon before summoner when added to dc
            #Also add summoner spells
            blue_team, 
            headers=["Summoner", "K", "D", "A", "CS"], 
            tablefmt="simple", 
            maxcolwidths=[None, 2, 2, 2, 3],
            colalign=("left", "left", "left", "left", "left")
            )
        
        if self.match.blue_team.win:
            return embed.add_field(name=f"Blue Team: (W)", value=f"```\n{blue_team_table}\n```", inline=False)

        return embed.add_field(name=f"Blue Team: (L)", value=f"```\n{blue_team_table}\n```", inline=False)



    def add_red_team(self, embed: discord.Embed):

        red_team = []

        for p in self.match.red_team.participants:
            s = p.stats
            name, kills, deaths, assists, cs = p.summoner.name, s.kills, s.deaths, s.assists, s.total_minions_killed
            red_team.append([name, kills, deaths, assists, cs])

        red_team_table = tabulate(
            #Add "Champion" with champion icon before summoner when added to dc
            #Also add summoner spells
            red_team, 
            headers=["Summoner", "K", "D", "A", "CS"], 
            tablefmt="simple", 
            maxcolwidths=[None, 2, 2, 2, 3],
            colalign=("left", "left", "left", "left", "left")
            )

        if self.match.red_team.win:
            return embed.add_field(name=f"Red Team: (W)", value=f"```\n{red_team_table}\n```", inline=False)

        return embed.add_field(name=f"Red Team: (L)", value=f"```\n{red_team_table}\n```", inline=False)


    
class Gold(AdvancedStats):

    def __init__(self, queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, league: League):
        super().__init__(queue, player, match, league)

    def get_gold_embed(self):
        queue_str = self.league.get_str_from_queue(queue=self.queue)

        embed = discord.Embed(title=f"Latest {queue_str} match")
        embed = BotHelper().set_embed_author(self.player, embed, self.league)
        embed = self.add_blue_team(embed)
        embed = self.add_red_team(embed)
    
        embed.set_footer(text=BotHelper().get_footer_text(queue=self.queue, player=self.player))

        return embed

    def add_blue_team(self, embed: discord.Embed):

        blue_team = []

        for p in self.match.blue_team.participants:
            s = p.stats
            name, earned, spent = p.summoner.name, s.gold_earned, s.gold_spent
            blue_team.append([name, earned, spent])
            
        blue_team_table = tabulate(
            #Add "Champion" with champion icon before summoner when added to dc
            #Also add summoner spells
            blue_team, 
            headers=["Summoner", "Earned", "Spent"], 
            tablefmt="simple", 
            colalign=("left", "center", "center")
            )
        
        if self.match.blue_team.win:
            return embed.add_field(name=f"Blue Team: (W)", value=f"```\n{blue_team_table}\n```", inline=False)

        return embed.add_field(name=f"Blue Team: (L)", value=f"```\n{blue_team_table}\n```", inline=False)



    def add_red_team(self, embed: discord.Embed):

        red_team = []

        for p in self.match.red_team.participants:
            s = p.stats
            name, earned, spent = p.summoner.name, s.gold_earned, s.gold_spent
            red_team.append([name, earned, spent])

        red_team_table = tabulate(
            #Add "Champion" with champion icon before summoner when added to dc
            #Also add summoner spells
            red_team, 
            headers=["Summoner", "Earned", "Spent"], 
            tablefmt="simple", 
            colalign=("left", "center", "center")
            )

        if self.match.red_team.win:
            return embed.add_field(name=f"Red Team: (W)", value=f"```\n{red_team_table}\n```", inline=False)

        return embed.add_field(name=f"Red Team: (L)", value=f"```\n{red_team_table}\n```", inline=False)

class Items():

    def __init__(self, queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, league: League):
        self.queue = queue
        self.player = player
        self.match = match
        self.league = league

    def get_items_embed(self):
        #TODO: Display items and summoners

        queue_str = self.league.get_str_from_queue(queue=self.queue)

        embed = discord.Embed(title=f"Latest {queue_str} match")
        embed = BotHelper().set_embed_author(self.player, embed, self.league)
        embed = self.add_blue_team(embed)
        embed = self.add_red_team(embed)

        # embed = self.add_players_items(embed=embed)
    
        embed.set_footer(text=BotHelper().get_footer_text(queue=self.queue, player=self.player))

        return embed


    def add_blue_team(self, embed: discord.Embed):

        if self.match.blue_team.win:
            embed.add_field(name=f"Blue Team:", value="WIN",inline=False)
        else:
            embed.add_field(name=f"Blue Team:", value="LOSE",inline=False)


        for p in self.match.blue_team.participants:
            
            blue_team = []

            name, d, f,items = p.summoner.name, p.summoner_spell_d.id, p.summoner_spell_f.id, BotHelper().get_items(player=p)

            blue_team.append([d, f, items])

            blue_team_table = tabulate(
                #Add "Champion" with champion icon before summoner when added to dc
                #Also add summoner spells
                blue_team, 
                headers=["D", "F", "Items"], 
                colalign=("center", "center", "left")
                )


            embed.add_field(name=f"{name}", value=f"{blue_team_table}", inline=False)

        return embed



    def add_red_team(self, embed: discord.Embed):

        #Add each summoner to a seperate field

        if self.match.red_team.win:
            embed.add_field(name=f"Red Team:", value="WIN", inline=False)
        else:
            embed.add_field(name=f"Red Team:", value="LOSE", inline=False)


        for p in self.match.red_team.participants:

            red_team = []

            name, d, f,items = p.summoner.name, p.summoner_spell_d.id, p.summoner_spell_f.id, BotHelper().get_items(player=p)
            red_team.append([d, f, items])

            red_team_table = tabulate(
                #Add "Champion" with champion icon before summoner when added to dc
                #Also add summoner spells
                red_team, 
                headers=["D", "F", "Items"], 
                colalign=("center", "center", "left")
                )

            embed.add_field(name=f"{name}", value=f"{red_team_table}", inline=False)

        return embed

    def add_players_items(self, embed: discord.Embed):

        if self.match.blue_team.win:
            embed.add_field(name=f"Blue Team:", value="**WIN**",inline=True)
        else:
            embed.add_field(name=f"Blue Team:", value="**LOSE**",inline=True)
        
        if self.match.red_team.win:
            embed.add_field(name=f"Red Team:", value="**WIN**", inline=True)
        else:
            embed.add_field(name=f"Red Team:", value="**LOSE**", inline=True)

        for i in range(5):
            
            b = self.match.blue_team.participants[i]
            r = self.match.red_team.participants[i]

            name_b, items_b = b.summoner.name, BotHelper().get_items(player=b)
            name_r, items_r = r.summoner.name, BotHelper().get_items(player=r)

            embed.add_field(name=f"{name_b}                         {name_r}", 
                            value=f"{items_b}                       |           {items_r}", inline=False)
            # embed.add_field(name=f"{name_r}", value=f"{items_r}", inline=True)

        return embed
    

class DamageDone():

    def __init__(self, queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, league: League):
        self.queue = queue
        self.player = player
        self.match = match
        self.league = league

    def get_damage_done_embed(self):
        #TODO: Display damage done (physical and magical)
        
        queue_str = self.league.get_str_from_queue(queue=self.queue)

        embed = discord.Embed(title=f"Latest {queue_str} match")
        embed = BotHelper().set_embed_author(self.player, embed, self.league)
        embed = self.add_blue_team(embed)
        embed = self.add_red_team(embed)
    
        embed.set_footer(text=BotHelper().get_footer_text(queue=self.queue, player=self.player))

        return embed

    def add_blue_team(self, embed: discord.Embed):

        blue_team = []

        for p in self.match.blue_team.participants:
            s = p.stats
            name, physical, magic, total = p.summoner.name, s.physical_damage_dealt, s.magic_damage_dealt_to_champions, s.total_damage_dealt_to_champions
            blue_team.append([name, physical, magic, total])
            
        blue_team_table = tabulate(
            #Add "Champion" with champion icon before summoner when added to dc
            #Also add summoner spells
            blue_team, 
            headers=["Summoner", "Physical", "Magic", "Total"], 
            tablefmt="simple", 
            colalign=("left", "left", "center", "center")
            )
        
        if self.match.blue_team.win:
            return embed.add_field(name=f"Blue Team: (W)", value=f"```\n{blue_team_table}\n```", inline=False)

        return embed.add_field(name=f"Blue Team: (L)", value=f"```\n{blue_team_table}\n```", inline=False)



    def add_red_team(self, embed: discord.Embed):

        red_team = []

        for p in self.match.red_team.participants:
            s = p.stats
            name, physical, magic, total = p.summoner.name, s.physical_damage_dealt, s.magic_damage_dealt_to_champions, s.total_damage_dealt_to_champions
            red_team.append([name, physical, magic, total])

        red_team_table = tabulate(
            #Add "Champion" with champion icon before summoner when added to dc
            #Also add summoner spells
            red_team, 
            headers=["Summoner", "Physical", "Magic", "Total"], 
            tablefmt="simple", 
            colalign=("left", "left", "center", "center")
            )

        if self.match.red_team.win:
            return embed.add_field(name=f"Red Team: (W)", value=f"```\n{red_team_table}\n```", inline=False)

        return embed.add_field(name=f"Red Team: (L)", value=f"```\n{red_team_table}\n```", inline=False)



class DamageTaken():

    def __init__(self, queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, league: League):
        self.queue = queue
        self.player = player
        self.match = match
        self.league = league

    def get_damage_taken_embed(self):
        #TODO: Display damage taken and mitigated
        queue_str = self.league.get_str_from_queue(queue=self.queue)

        embed = discord.Embed(title=f"Latest {queue_str} match")
        embed = BotHelper().set_embed_author(self.player, embed, self.league)
        embed = self.add_blue_team(embed)
        embed = self.add_red_team(embed)
    
        embed.set_footer(text=BotHelper().get_footer_text(queue=self.queue, player=self.player))

        return embed

    def add_blue_team(self, embed: discord.Embed):

        blue_team = []

        for p in self.match.blue_team.participants:
            s = p.stats
            name, mitigated, total = p.summoner.name, s.damage_self_mitigated, s.total_damage_taken
            blue_team.append([name, mitigated, total])
            
        blue_team_table = tabulate(
            #Add "Champion" with champion icon before summoner when added to dc
            #Also add summoner spells
            blue_team, 
            headers=["Summoner", "Mitigated", "Total"], 
            tablefmt="simple", 
            colalign=("left", "center", "center")
            )
        
        if self.match.blue_team.win:
            return embed.add_field(name=f"Blue Team: (W)", value=f"```\n{blue_team_table}\n```", inline=False)

        return embed.add_field(name=f"Blue Team: (L)", value=f"```\n{blue_team_table}\n```", inline=False)



    def add_red_team(self, embed: discord.Embed):

        red_team = []

        for p in self.match.red_team.participants:
            s = p.stats
            name, mitigated, total = p.summoner.name, s.damage_self_mitigated, s.total_damage_taken
            red_team.append([name, mitigated, total])

        red_team_table = tabulate(
            #Add "Champion" with champion icon before summoner when added to dc
            #Also add summoner spells
            red_team, 
            headers=["Summoner", "Mitigated", "Total"], 
            tablefmt="simple", 
            colalign=("left", "center", "center")
            )

        if self.match.red_team.win:
            return embed.add_field(name=f"Red Team: (W)", value=f"```\n{red_team_table}\n```", inline=False)

        return embed.add_field(name=f"Red Team: (L)", value=f"```\n{red_team_table}\n```", inline=False)


    