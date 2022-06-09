from riotwatcher import LolWatcher, ApiError
import riotwatcher
class League:
    
    lol_watcher = LolWatcher('RGAPI-c3535508-120a-4a91-93f5-8b518fc60e89')
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

    def __init__(self, region: str = None, summ_id: str = None) -> None:
        self.summ_id = summ_id
        self.region = region

    def set_summoner_id_from_name(self):
        while True:
            try:
                summoner_name: str = str(input("Summoner name: "))
                self.set_region()
                summoner = self.lol_watcher.summoner.by_name(self.region, summoner_name.strip())
                self.summ_id = summoner['id']
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
        print(self.summ_id)

    def set_region(self):
        while True:
            region_in = input("Summoner region: ")
            #Change to dictionary
            try:
                self.region = self.regions[region_in]
                break
            except KeyError as e:
                #Print available region options
                print("invalid region\n")
                continue

    def menu():
        '''
        Menu printout on the what they can do
        eg:
        1. Mastery
        2. Ranked Stats
        3. etc.
        4. etc.
        '''
        pass

    
def print_regions():
    '''
    Print all the regions that are available for input
    '''
    pass
def select_region():
    pass
def get_user():
    pass
#Get input for region and match with dictionary
#Get input for summoner name
# me = lol_watcher.summoner.by_name(my_region, 'Bodiez')
# print(me)
# summ_id = me['id']
# # print(summ_id)
# champ_mastery = lol_watcher.champion_mastery
# # print(champ_mastery.by_summoner_by_champion(my_region, summ_id, '67'))
# # # all objects are returned (by default) as a dict
# # # lets see if i got diamond yet (i probably didnt)
# # my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
# # print(my_ranked_stats)
# # First we get the latest version of the game from data dragon
# versions = lol_watcher.data_dragon.versions_for_region(my_region)
# champions_version = versions['n']['champion']
# #Get input for champion name
# # Lets get some champions
# current_champ_list = lol_watcher.data_dragon.champions(champions_version)
# jhin = current_champ_list['data']['Jhin']
# print(champ_mastery.by_summoner_by_champion(my_region, summ_id, jhin['key']))
# # For Riot's API, the 404 status code indicates that the requested data wasn't found and
# # should be expected to occur in normal operation, as in the case of a an
# # invalid summoner name, match ID, etc.
# #
# # The 429 status code indicates that the user has sent too many requests
# # in a given amount of time ("rate limiting").
def main(league: League):
    league.set_summoner_id_from_name