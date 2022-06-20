from datapipelines import NotFoundError
import cassiopeia as cass
from collections import Counter
import arrow
import discord
from discord.ext import commands

class League:
    
    regions = {"NA":"NA", "NORTH AMERICA":"NA",
            "EUW":"EUW", "EUROPE WEST":"EUW",
            "EUNE":"EUNE", "EUN":"EUNE", "EUROPE NORDIC & EAST": "EUNE",
            "KOREA":"KR", "KR": "KR",
            "BR":"BR", "BRAZIL":"BR",
            "Japan":"JP", "JP": "JP",
            "RU":"RU", "RUSSIA": "RU",
            "OCEANIA":"OCE", "OCE": "OCE", "OC": "OCE",
            "TURKEY":"TR", "TR": "TR",
            "LATIN AMERICA NORTH":"LAN", "LAN": "LAN",
            "LATIN AMERICA SOUTH":"la2", "LAS": "LAS"}

    def __init__(self, summoner = None, region: str = None, summ_id: str = None, puuid: str = None) -> None:
        self.summoner = summoner
        self.summ_id = summ_id
        self.region = region
        self.puuid = puuid
        self.api_key = self.get_api_key()
        cass.set_riot_api_key(self.api_key)

    def get_api_key(self):
        with open('config.txt', 'r') as f:
            api_key = f.readlines()[0].strip()
        return api_key

    def set_summoner_id_from_name(self, summoner_name, region):

            self.set_region(region = region)
            summoner = self.summoner = cass.get_summoner(name=summoner_name, region=self.region)
            self.summ_id, self.puuid = summoner.id, summoner.puuid
            
        # self.latest_ranked_match()
    
    def set_region(self, region):

        self.region = self.regions[region.upper()]

    def get_regions(self):
        
        # TODO: Print all the regions that are available for input
        return """
Available regions:
North America/NA
Europe West/EUW
Europe Nordic & East/EUN/EUNE
Korea/KR
Brazil/BR
Japan/JP
Russia/RU
Oceania/OCE/OC
Turkey/TR
Latin America North/LAN
Latin America South/LAS
        """


    def get_latest_normal_match(self, summoner_name, region) -> cass.core.match.Match:

        self.set_summoner_id_from_name(summoner_name=summoner_name, region=region)

        match_history = cass.get_match_history(
            continent = self.summoner.region.continent,
            puuid = self.puuid,
            queue = cass.Queue.normal_draft_fives,
            end_index=4
        )

        return match_history[0]


    def latest_ranked_match(self) -> cass.core.match.Match:
        print("Getting latest ranked match info...\n")

        match_history = cass.get_match_history(
            continent = self.summoner.region.continent,
            puuid = self.puuid,
            queue = cass.Queue.normal_draft_fives,
            end_index=4
        )

        # champion_id_to_name = {
        #     champion.id: champion.name for champion in cass.get_champions(region=self.region)
        # }



        match = match_history[0]
        
        return match

def main(league: League):
    league.set_summoner_id_from_name()
    league.latest_ranked_match()



