from league import League
import discord
from discord.ui import Button, View
import cassiopeia as cass
from cassiopeia import Queue
import json
from tabulate import tabulate

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


    def get_embed_last_full(self, queue, player, match, league: League):

        queue_str = league.get_str_from_queue(queue=queue)

        embed = discord.Embed(title=f"Latest {queue_str} match")
        embed = self.set_embed_author(player, embed, league)
        embed = self.add_blue_team(match, embed)
        embed = self.add_red_team(match, embed)
       
        embed.set_footer(text=self.get_footer_text(queue=queue, player=player))

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

    def add_blue_team(self, match: cass.core.match, embed: discord.Embed):

        blue_team = []

        for p in match.blue_team.participants:
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
        
        if match.blue_team.win:
            return embed.add_field(name=f"Blue Team: (W)", value=f"```\n{blue_team_table}\n```", inline=False)

        return embed.add_field(name=f"Blue Team: (L)", value=f"```\n{blue_team_table}\n```", inline=False)



    def add_red_team(self, match: cass.core.match, embed: discord.Embed):

        red_team = []

        for p in match.red_team.participants:
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

        if match.red_team.win:
            return embed.add_field(name=f"Red Team: (W)", value=f"```\n{red_team_table}\n```", inline=False)

        return embed.add_field(name=f"Red Team: (L)", value=f"```\n{red_team_table}\n```", inline=False)

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

                #Returns "" if player is not in promos
                promos = self.promos_text(player.summoner.league_entries.flex.promos)

                if promos == "":
                    return f"Level: {player.summoner.level} || Flex Rank: {rank.tier} {rank.division} {lp}LP"
                else:
                    return f"""Level: {player.summoner.level} || Flex Rank: {rank.tier} {rank.division} {lp}LP
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

        self.gold = self.Gold(queue=queue, player=player, match=match, league=league)
        self.items = self.Items(queue=queue, player=player, match=match, league=league)
        self.dd = self.DamageDone(queue=queue, player=player, match=match, league=league)
        self.dt = self.DamageTaken(queue=queue, player=player, match=match, league=league)

    
    class Gold():

        def __init__(self, queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, league: League):
            self.queue = queue
            self.player = player
            self.match = match
            self.league = league

        def get_gold_embed(self):
            queue_str = self.league.get_str_from_queue(queue=self.queue)

            embed = discord.Embed(title=f"Latest {queue_str} match")
            embed = BotHelper().set_embed_author(self.player, embed, self.league)
            embed = self.add_blue_team(self.match, embed)
            embed = self.add_red_team(self.match, embed)
        
            embed.set_footer(text=BotHelper().get_footer_text(queue=self.queue, player=self.player))

            return embed

        def add_blue_team(self, match: cass.core.match, embed: discord.Embed):

            blue_team = []

            for p in match.blue_team.participants:
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
            
            if match.blue_team.win:
                return embed.add_field(name=f"Blue Team: (W)", value=f"```\n{blue_team_table}\n```", inline=False)

            return embed.add_field(name=f"Blue Team: (L)", value=f"```\n{blue_team_table}\n```", inline=False)



        def add_red_team(self, match: cass.core.match, embed: discord.Embed):

            red_team = []

            for p in match.red_team.participants:
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

            if match.red_team.win:
                return embed.add_field(name=f"Red Team: (W)", value=f"```\n{red_team_table}\n```", inline=False)

            return embed.add_field(name=f"Red Team: (L)", value=f"```\n{red_team_table}\n```", inline=False)

    class Items():

        def __init__(self, queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, league: League):
            self.queue = queue
            self.player = player
            self.match = match
            self.league = league

        def get_items_embed(self, queue, player, match, league):
            #TODO: Display items and summoners
            pass

    class DamageDone():

        def __init__(self, queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, league: League):
            self.queue = queue
            self.player = player
            self.match = match
            self.league = league

        def get_damage_done_embed(self, queue, player, match, league):
            #TODO: Display damage done (physical and magical)
            pass

    class DamageTaken():

        def __init__(self, queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, league: League):
            self.queue = queue
            self.player = player
            self.match = match
            self.league = league

        def get_damage_taken_embed(self, queue, player, match, league):
            #TODO: Display damage taken and mitigated
            pass


class AdvancedView(View):

    def __init__(self, *items: discord.ui.Item, timeout: discord.Optional[float] = 180, 
                    queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, 
                    league: League):
        super().__init__(*items, timeout=timeout)
        self.queue = queue
        self.player = player
        self.match = match
        self.league = league
        self.add_item(self.opgg())
        self.advanced = AdvancedStats(queue=queue, player=player, match=match, league=league)

    def opgg(self):
    
        url = f"https://op.gg/summoners/{self.league.region.lower()}/{self.player.summoner.name}"
        opgg = Button(label = "OP.GG", url = url)

        return opgg
    

    @discord.ui.button(label="KDA", custom_id="kda", disabled=True)
    async def kda_button_callback(self, button, interaction: discord.interactions.Interaction):
        self.enable_all_items()
        button.disabled = True
        embed = BotHelper().get_embed_last_full(self.queue, self.player, self.match, self.league)
        await interaction.response.edit_message(embed=embed, view=self)


    @discord.ui.button(label="Gold", custom_id="gold")
    async def gold_button_callback(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = self.advanced.gold.get_gold_embed()
        await interaction.response.edit_message(embed=embed, view=self)


    @discord.ui.button(label="Damage Done", custom_id="damage_d")
    async def damage_d_button_callback(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        await interaction.response.edit_message(view=self)


    @discord.ui.button(label="Damage Taken", custom_id="damage_t")
    async def damage_t_button_callback(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        await interaction.response.edit_message(view=self)

    