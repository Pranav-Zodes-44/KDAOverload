from datapipelines import NotFoundError
import cassiopeia as cass
from cassiopeia import Queue
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

    def get_queue_from_str(queue: str = None) -> Queue:
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

        if queue == None:
            return Queue.normal_draft_fives
        else:
            return queue_dict[queue.lower()]

    def get_str_from_queue(self, queue) -> str:

        queue_dict = {
            Queue.ranked_solo_fives: "Ranked Solo/Duo",
            Queue.ranked_flex_fives: "Ranked Flex",
            Queue.normal_draft_fives: "Normal Draft",
            Queue.aram: "ARAM",
            Queue.clash: "Clash"
        }

        return queue_dict[queue]


    def get_latest_match(self, summoner_name, region, queue: Queue) -> cass.core.match.Match:
        self.set_summoner_id_from_name(summoner_name=summoner_name, region=region)
        match_history = cass.get_match_history(
            continent = self.summoner.region.continent,
            puuid = self.puuid,
            queue = queue,
            end_index=2
        )

        return match_history[0]

    def get_latest_normal_match(self, summoner_name, region) -> cass.core.match.Match:

        #TODO: Change to get_latest_match
        #Create dictionary based on options of match_type from bot
        # i.e: {"ranked", cass.Queue.ranked_solo_fives}, with queue variable of course.
        # Default to normal_draft_fives
        # Add support for ARAM, Flex, and RGMs
        # Maybe tft? 

        self.set_summoner_id_from_name(summoner_name=summoner_name, region=region)

        match_history = cass.get_match_history(
            continent = self.summoner.region.continent,
            puuid = self.puuid,
            queue = cass.Queue.ranked_solo_fives,
            end_index=4
        )

        print(self.summoner.id)

        return match_history[0]

    #TODO: Create set/get queue_type to make the process of error handling easier,
    #since set_region can also throw a KeyError

    def latest_ranked_match(self) -> cass.core.match.Match:
        print("Getting latest ranked match info...\n")

        match_history = cass.get_match_history(
            continent = self.summoner.region.continent,
            puuid = self.puuid,
            queue = cass.Queue.ranked_solo_fives,
            end_index=4
        )

        # champion_id_to_name = {
        #     champion.id: champion.name for champion in cass.get_champions(region=self.region)
        # }



        match = match_history[0]
        
        return match