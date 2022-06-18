from datapipelines import NotFoundError
import cassiopeia as cass
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

    def set_summoner_id_from_name(self):
        while True:
            try:
                summoner_name: str = str(input("Summoner name: "))
                self.set_region()
                summoner = self.summoner = cass.get_summoner(name=summoner_name, region=self.region)
                self.summ_id, self.puuid = summoner.id, summoner.puuid
                break
            except NotFoundError as NFerr:
                print("\nThat's a ridiculous name! Please enter a valid summoner name...\n")
                continue
            # except ApiError as err:
            #     if err.response.status_code == 429:
            #         print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
            #         print('this retry-after is handled by default by the RiotWatcher library')
            #         print('future requests wait until the retry-after time passes')
            #     elif err.response.status_code == 404:
            #         print('Summoner with that ridiculous name not found.')
            #         print('Please make sure the name you entered is correct \n')
            #         continue
            #     else:
            #         raise
        # self.latest_ranked_match()
    
    def set_region(self):
        while True:
            region_in = input("Summoner region: ")
            #TODO: Change to dictionary
            try:
                self.region = self.regions[region_in.upper()]
                break
            except KeyError as e:
                print("Invalid region, please enter one of the following regions: \n")
                self.print_regions()
                continue

    def print_regions(self):
        
        # TODO: Print all the regions that are available for input
        print("""
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
        """)
        
        pass

    def latest_ranked_match(self):
        print("Getting latest ranked match info...\n")

        match_history = cass.get_match_history(
            continent = self.summoner.region.continent,
            puuid = self.puuid,
            queue = cass.Queue.ranked_solo_fives,
            begin_time=arrow.Arrow(2022, 6, 13)
        )

        champion_id_to_name = {
            champion.id: champion.name for champion in cass.get_champions(region=self.region)
        }

        played_champs = Counter()

        for match in match_history:
            champion_id = match.participants[self.summoner].champion.id
            champion_name = champion_id_to_name[champion_id]
            played_champs[champion_name] += 1
        
        print("\033c", end="")

        print("Number of matches played: ", len(match_history))

        print(f"Top 10 Champions played by {self.summoner.name}: ") 
        for champion_name, count in played_champs.most_common(10):
            print(champion_name, count)   
        print()

        match = match_history[0]
        print("Match ID: ", match.id)
        print()

        # for x, participant in enumerate(match.participants):
        #     print(participant.summoner.name, "playing", participant.champion.name, participant.win)
        #     if x == 9:
        #         break

        print("Blue team win: ", match.blue_team.win)
        for participant in match.blue_team.participants:
            print(participant.summoner.name, "playing", participant.champion.name)

        print("\nRed team win: ", match.red_team.win)
        for participant in match.red_team.participants:
            print(participant.summoner.name, "playing", participant.champion.name)
        print()


        # latest_match_id = self.lol_watcher.match.matchlist_by_puuid(self.region, self.puuid, type='ranked')[0]
        # latest_match_info = self.lol_watcher.match.by_id(self.region, latest_match_id)
        # date = time.strftime('%A, %B %e, %Y - %H:%M',time.localtime(latest_match_info['info']['gameStartTimestamp']))
        # print(f"Match date: {date}\n")
        # participants = latest_match_info['info']['participants']
        # for participant in participants:
        #     print(f"Summoner name: {participant['summonerName']}")
        #     print(f"    Champion: {participant['championName']}")
        #     print(f"    Kills: {participant['kills']}")
        #     print(f"    Deaths: {participant['deaths']}")
        #     print(f"    Assits: {participant['assists']}")
        #     print()

    def menu():
        '''
        Menu printout on the what they can do
        eg:
        1. Mastery
        2. Ranked Stats
        3. etc.
        4. etc.
        '''
        #TODO: Create menu
        pass

    



def main(league: League):
    league.set_summoner_id_from_name()
    league.latest_ranked_match()



