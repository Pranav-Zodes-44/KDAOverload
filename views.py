from league import League
import discord
from discord.ui import Button, View
import cassiopeia as cass
from cassiopeia import Queue
from helpers import AdvancedStats, Gold, Items, DamageDone, DamageTaken
from helpers import BotHelper

class AdvancedView(View):

    def __init__(self, *items: discord.ui.Item, timeout: discord.Optional[float] = None, 
                    queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, 
                    league: League):
        super().__init__(*items, timeout=timeout)

        self.queue = queue
        self.player = player
        self.match = match
        self.league = league

        self.add_item(self.opgg())

        self.advanced = AdvancedStats(queue=queue, player=player, match=match, league=league)
        self.gold = Gold(queue=queue, player=player, match=match, league=league)
        self.item = Items(queue=queue, player=player, match=match, league=league)
        self.dd = DamageDone(queue=queue, player=player, match=match, league=league)
        self.dt = DamageTaken(queue=queue, player=player, match=match, league=league)


    def opgg(self):
    
        url = f"https://op.gg/summoners/{self.league.region.lower()}/{self.player.summoner.name}"
        opgg = Button(label = "OP.GG", url = url)

        return opgg
    

    @discord.ui.button(label="KDA", custom_id="kda", disabled=True)
    async def kda_button_callback(self, button, interaction: discord.interactions.Interaction):
        self.enable_all_items()
        button.disabled = True
        embed = self.advanced.get_embed_last()
        await interaction.response.edit_message(embed = embed, view=self)


    @discord.ui.button(label="Players", custom_id="items")
    async def item_button_callback(self, button, interaction: discord.interactions.Interaction):
        self.enable_all_items()
        button.disabled = True
        view = ItemsView(queue=self.queue, player=self.player, match=self.match, league=self.league, back_view=self)
        embed = BotHelper().get_embed_last_simple(queue=self.queue, player=self.player, match=self.match, league=self.league)
        await interaction.response.edit_message(embed = embed, view = view)

    @discord.ui.button(label="Gold", custom_id="gold")
    async def gold_button_callback(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = self.gold.get_gold_embed()
        await interaction.response.edit_message(embed = embed, view = self)


    @discord.ui.button(label="Damage Done", custom_id="damage_d")
    async def damage_d_button_callback(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = self.dd.get_damage_done_embed()
        await interaction.response.edit_message(embed = embed, view=self)


    @discord.ui.button(label="Damage Taken", custom_id="damage_t")
    async def damage_t_button_callback(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = self.dt.get_damage_taken_embed()
        await interaction.response.edit_message(embed = embed, view = self)

    
class ItemsView(View):
    
    def __init__(self, *items: discord.ui.Item, timeout: discord.Optional[float] = None,
                    queue: cass.Queue, player: cass.core.match.Participant, match: cass.core.match, 
                    league: League, back_view: discord.ui.View):
        super().__init__(*items, timeout=timeout)
        self.queue = queue
        self.player = player
        self.match = match
        self.league = league
        self.back_view = back_view
        self.set_player_buttons()


    def set_player_buttons(self):
        for i, button in enumerate(self.children):
            if i == 10:
                break

            button.label = self.match.participants[i].summoner.name
            if button.label == self.player.summoner.name:
                button.disabled = True


    @discord.ui.button(label="Player 1", custom_id="player1", style=discord.ButtonStyle.primary)
    async def player1_button_interaction(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = BotHelper().get_embed_last_simple(self.queue, self.match.participants[0], self.match, self.league)
        await interaction.response.edit_message(embed = embed, view = self)


    @discord.ui.button(label="Player 2", custom_id="player2", style=discord.ButtonStyle.primary)
    async def player2_button_interaction(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = BotHelper().get_embed_last_simple(self.queue, self.match.participants[1], self.match, self.league)
        await interaction.response.edit_message(embed = embed, view = self)


    @discord.ui.button(label="Player 3", custom_id="player3", style=discord.ButtonStyle.primary)
    async def player3_button_interaction(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = BotHelper().get_embed_last_simple(self.queue, self.match.participants[2], self.match, self.league)
        await interaction.response.edit_message(embed = embed, view = self)


    @discord.ui.button(label="Player 4", custom_id="player4", style=discord.ButtonStyle.primary)
    async def player4_button_interaction(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = BotHelper().get_embed_last_simple(self.queue, self.match.participants[3], self.match, self.league)
        await interaction.response.edit_message(embed = embed, view = self)


    @discord.ui.button(label="Player 5", custom_id="player5", style=discord.ButtonStyle.primary)
    async def player5_button_interaction(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = BotHelper().get_embed_last_simple(self.queue, self.match.participants[4], self.match, self.league)
        await interaction.response.edit_message(embed = embed, view = self)


    @discord.ui.button(label="Player 6", custom_id="player6", style=discord.ButtonStyle.danger)
    async def player6_button_interaction(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = BotHelper().get_embed_last_simple(self.queue, self.match.participants[5], self.match, self.league)
        await interaction.response.edit_message(embed = embed, view = self)


    @discord.ui.button(label="Player 7", custom_id="player7", style=discord.ButtonStyle.danger)
    async def player7_button_interaction(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = BotHelper().get_embed_last_simple(self.queue, self.match.participants[6], self.match, self.league)
        await interaction.response.edit_message(embed = embed, view = self)


    @discord.ui.button(label="Player 8", custom_id="player8", style=discord.ButtonStyle.danger)
    async def player8_button_interaction(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = BotHelper().get_embed_last_simple(self.queue, self.match.participants[7], self.match, self.league)
        await interaction.response.edit_message(embed = embed, view = self)


    @discord.ui.button(label="Player 9", custom_id="player9", style=discord.ButtonStyle.danger)
    async def player9_button_interaction(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = BotHelper().get_embed_last_simple(self.queue, self.match.participants[8], self.match, self.league)
        await interaction.response.edit_message(embed = embed, view = self)


    @discord.ui.button(label="Player 10", custom_id="player10", style=discord.ButtonStyle.danger)
    async def player10_button_interaction(self, button, interaction):
        self.enable_all_items()
        button.disabled = True
        embed = BotHelper().get_embed_last_simple(self.queue, self.match.participants[9], self.match, self.league)
        await interaction.response.edit_message(embed = embed, view = self)


    @discord.ui.button(label="Go back")
    async def back_button_interaction(self, button, interaction):
        self.back_view.enable_all_items()
        kda_button = [x for x in self.back_view.children if x.custom_id == "kda"][0]
        kda_button.disabled = True
        embed = AdvancedStats(queue=self.queue, player=self.player, match=self.match, league=self.league).get_embed_last()
        await interaction.response.edit_message(embed=embed, view=self.back_view)