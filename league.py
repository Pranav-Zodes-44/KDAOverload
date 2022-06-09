from riotwatcher import LolWatcher, ApiError
import time
class League:
    
    regions = {"NA":"na1", "North America":"na1",
            "EUW":"euw1", "Europe West":"euw1",
            "EUNE":"eun1", "EUN":"eun1", "Europe Nordic & East": "eun1",
            "Korea":"kr", "KR": "kr",
            "BR":"br1", "Brazil":"br1",
            "Japan":"jp1", "JP": "jp1",
            "RU":"ru", "Russia": "ru",
            "Oceania":"oc1", "OCE": "oc1", "OC": "oc1",
            "Turkey":"tr1", "TR": "tr1",
            "Latin America North":"la1", "LAN": "la1",
            "Latin America South":"la2", "LAS": "la2"}

    def __init__(self, region: str = None, summ_id: str = None, puuid: str = None, api_key: str = None) -> None:
        self.summ_id = summ_id
        self.region = region
        self.puuid = puuid
        self.api_key = self.get_api_key()
        self.lol_watcher = LolWatcher(self.api_key)

    def get_api_key(self):
        with open('config.txt', 'r') as f:
            api_key = f.readlines()[0]
        return api_key

    def set_summoner_id_from_name(self):
        while True:
            try:
                summoner_name: str = str(input("Summoner name: "))
                self.set_region()
                summoner = self.lol_watcher.summoner.by_name(self.region, summoner_name.strip())
                self.summ_id, self.puuid = summoner['id'], summoner['puuid']
                break
            except ApiError as err:
                if err.response.status_code == 429:
                    print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
                    print('this retry-after is handled by default by the RiotWatcher library')
                    print('future requests wait until the retry-after time passes')
                elif err.response.status_code == 404:
                    print('Summoner with that ridiculous name not found.')
                    print('Please make sure the name you entered is correct \n')
                    continue
                else:
                    raise
        self.latest_ranked_match()
    
    def set_region(self):
        while True:
            region_in = input("Summoner region: ")
            #TODO: Change to dictionary
            try:
                self.region = self.regions[region_in]
                break
            except KeyError as e:
                #TODO: call print_region() to print regions
                print("invalid region\n")
                continue

    def print_regions():
        
        # TODO: Print all the regions that are available for input
        
        pass

    def latest_ranked_match(self):
        print("Getting latest ranked match info...\n")

        latest_match_id = self.lol_watcher.match.matchlist_by_puuid(self.region, self.puuid, type='ranked')[0]
        latest_match_info = self.lol_watcher.match.by_id(self.region, latest_match_id)
        date = time.strftime('%A, %B %e, %Y - %H:%M',time.localtime(latest_match_info['info']['gameStartTimestamp']))
        print(f"Match date: {date}\n")
        participants = latest_match_info['info']['participants']
        for participant in participants:
            print(f"Summoner name: {participant['summonerName']}")
            print(f"    Champion: {participant['championName']}")
            print(f"    Kills: {participant['kills']}")
            print(f"    Deaths: {participant['deaths']}")
            print(f"    Assits: {participant['assists']}")
            print()

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



