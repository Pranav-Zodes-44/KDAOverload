from nis import match
from attr import Attribute
from datapipelines import NotFoundError
import cassiopeia as cass
from cassiopeia import Queue, Match
from collections import Counter
import arrow

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

    def __init__(self, summoner = None, region: str = None, puuid: str = None) -> None:
        self.summoner = summoner
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
            self.puuid = summoner.puuid

        # self.latest_ranked_match()
    
    def set_region(self, region):

        self.region = self.regions[region.upper()]

    def get_regions(self):
        
        # TODO: Print all the regions that are available for input
        return """
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

    def get_queue_from_str(self, queue: str = None) -> Queue:
        queue_dict = {
            "ranked": Queue.ranked_solo_fives,
            "flex": Queue.ranked_flex_fives,
            "solo": Queue.ranked_solo_fives,
            "duo": Queue.ranked_solo_fives,
            "solo/duo": Queue.ranked_solo_fives,
            "normal": Queue.normal_draft_fives,
            "draft": Queue.normal_draft_fives,
            "aram": Queue.aram,
            "clash": Queue.clash
        }

        try:
            return queue_dict[queue.lower()]
        except KeyError as ke:
            return Queue.normal_draft_fives
        except AttributeError as ae:
            return Queue.normal_draft_fives

    def get_str_from_queue(self, queue) -> str:

        queue_dict = {
            Queue.ranked_solo_fives: "Ranked Solo/Duo",
            Queue.ranked_flex_fives: "Ranked Flex",
            Queue.normal_draft_fives: "Normal Draft",
            Queue.aram: "ARAM",
            Queue.clash: "Clash"
        }

        return queue_dict[queue]


    def latest_match(self, summoner_name, region, queue: Queue) -> cass.core.match.Match:

        self.set_summoner_id_from_name(summoner_name=summoner_name, region=region)

        match_history = cass.get_match_history(
            continent = self.summoner.region.continent,
            puuid = self.puuid,
            queue = queue,
            end_index=1
        )
         
        return match_history[0]
    
    def get_player_from_match(self, match, summoner_name) -> cass.core.match.Participant:
        for p in match.participants:
            if p.summoner.name == summoner_name:
                return p

    def get_match_history(self, summoner_name, region, queue: Queue):
        self.set_summoner_id_from_name(summoner_name=summoner_name, region=region)
        match_history = cass.get_match_history(
            continent = self.summoner.region.continent,
            puuid = self.puuid,
            queue = queue,
            end_index=10
        )
        return match_history
    
    def get_player_items(self, player: cass.core.match.Participant):
        return player.stats.items

    #TODO: Create set/get queue_type to make the process of error handling easier,
    #since set_region can also throw a KeyError