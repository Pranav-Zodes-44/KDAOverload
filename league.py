from riotwatcher import LolWatcher, ApiError
import riotwatcher
import time
class League:
    
    lol_watcher = LolWatcher('RGAPI-59fa5deb-9bf1-4589-8cc4-69eb053fdb75')
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

    def __init__(self, region: str = None, summ_id: str = None, puuid: str = None) -> None:
        self.summ_id = summ_id
        self.region = region
        self.puuid = puuid

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
            #Change to dictionary
            try:
                self.region = self.regions[region_in]
                break
            except KeyError as e:
                #Print available region options
                print("invalid region\n")
                continue

    def print_regions():
        '''
        Print all the regions that are available for input
        '''
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
        pass

    
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
    league.set_summoner_id_from_name()



    # "participants": [
    #         {
    #             "assists": 3,

    #             },
    #             "champExperience": 19889,
    #             "champLevel": 18,
    #             "championId": 122,
    #             "championName": "Darius",
    #             "championTransform": 0,
    #             "consumablesPurchased": 4,
    #             "damageDealtToBuildings": 2035,
    #             "damageDealtToObjectives": 15519,
    #             "damageDealtToTurrets": 2035,
    #             "damageSelfMitigated": 50817,
    #             "deaths": 4,
    #             "detectorWardsPlaced": 2,
    #             "doubleKills": 1,
    #             "dragonKills": 0,
    #             "eligibleForProgression": true,
    #             "firstBloodAssist": false,
    #             "firstBloodKill": false,
    #             "firstTowerAssist": true,
    #             "firstTowerKill": false,
    #             "gameEndedInEarlySurrender": false,
    #             "gameEndedInSurrender": false,
    #             "goldEarned": 17314,
    #             "goldSpent": 17133,
    #             "individualPosition": "TOP",
    #             "inhibitorKills": 2,
    #             "inhibitorTakedowns": 2,
    #             "inhibitorsLost": 0,
    #             "item0": 3078,
    #             "item1": 6333,
    #             "item2": 3075,
    #             "item3": 3053,
    #             "item4": 3742,
    #             "item5": 3047,
    #             "item6": 3364,
    #             "itemsPurchased": 28,
    #             "killingSprees": 4,
    #             "kills": 15,
    #             "lane": "TOP",
    #             "largestCriticalStrike": 31,
    #             "largestKillingSpree": 5,
    #             "largestMultiKill": 3,
    #             "longestTimeSpentLiving": 1172,
    #             "magicDamageDealt": 5880,
    #             "magicDamageDealtToChampions": 502,
    #             "magicDamageTaken": 9113,
    #             "neutralMinionsKilled": 12,
    #             "nexusKills": 0,
    #             "nexusLost": 0,
    #             "nexusTakedowns": 1,
    #             "objectivesStolen": 0,
    #             "objectivesStolenAssists": 0,
    #             "participantId": 1,
    #             "pentaKills": 0,
    #             "perks": {
    #                 "statPerks": {
    #                     "defense": 5002,
    #                     "flex": 5008,
    #                     "offense": 5005
    #                 },
    #                 "styles": [
    #                     {
    #                         "description": "primaryStyle",
    #                         "selections": [
    #                             {
    #                                 "perk": 8010,
    #                                 "var1": 647,
    #                                 "var2": 0,
    #                                 "var3": 0
    #                             },
    #                             {
    #                                 "perk": 9111,
    #                                 "var1": 2364,
    #                                 "var2": 360,
    #                                 "var3": 0
    #                             },
    #                             {
    #                                 "perk": 9105,
    #                                 "var1": 17,
    #                                 "var2": 20,
    #                                 "var3": 0
    #                             },
    #                             {
    #                                 "perk": 8299,
    #                                 "var1": 997,
    #                                 "var2": 0,
    #                                 "var3": 0
    #                             }
    #                         ],
    #                         "style": 8000
    #                     },
    #                     {
    #                         "description": "subStyle",
    #                         "selections": [
    #                             {
    #                                 "perk": 8473,
    #                                 "var1": 925,
    #                                 "var2": 0,
    #                                 "var3": 0
    #                             },
    #                             {
    #                                 "perk": 8242,
    #                                 "var1": 87,
    #                                 "var2": 0,
    #                                 "var3": 0
    #                             }
    #                         ],
    #                         "style": 8400
    #                     }
    #                 ]
    #             },
    #             "physicalDamageDealt": 190113,
    #             "physicalDamageDealtToChampions": 23822,
    #             "physicalDamageTaken": 20899,
    #             "profileIcon": 2074,
    #             "puuid": "8ZYh7dd02AW4mQJm_qmNhH62g_cwsq6LSimGx0OR0h8O7l3SxQCHODYXhsAK7uW29tPbSt0GSU0E2Q",
    #             "quadraKills": 0,
    #             "riotIdName": "",
    #             "riotIdTagline": "",
    #             "role": "SOLO",
    #             "sightWardsBoughtInGame": 0,
    #             "spell1Casts": 81,
    #             "spell2Casts": 114,
    #             "spell3Casts": 27,
    #             "spell4Casts": 14,
    #             "summoner1Casts": 5,
    #             "summoner1Id": 4,
    #             "summoner2Casts": 7,
    #             "summoner2Id": 6,
    #             "summonerId": "qJagyKSWhk_kLn0e0x62APPivnrEQicTOLkxiY_DNg95swFa",
    #             "summonerLevel": 332,
    #             "summonerName": "Davidsonsanches",
    #             "teamEarlySurrendered": false,
    #             "teamId": 100,
    #             "teamPosition": "TOP",
    #             "timeCCingOthers": 30,
    #             "timePlayed": 2340,
    #             "totalDamageDealt": 222618,
    #             "totalDamageDealtToChampions": 31726,
    #             "totalDamageShieldedOnTeammates": 0,
    #             "totalDamageTaken": 41823,
    #             "totalHeal": 12318,
    #             "totalHealsOnTeammates": 0,
    #             "totalMinionsKilled": 224,
    #             "totalTimeCCDealt": 195,
    #             "totalTimeSpentDead": 205,
    #             "totalUnitsHealed": 1,
    #             "tripleKills": 1,
    #             "trueDamageDealt": 26623,
    #             "trueDamageDealtToChampions": 7401,
    #             "trueDamageTaken": 11810,
    #             "turretKills": 1,
    #             "turretTakedowns": 2,
    #             "turretsLost": 3,
    #             "unrealKills": 0,
    #             "visionScore": 38,
    #             "visionWardsBoughtInGame": 2,
    #             "wardsKilled": 7,
    #             "wardsPlaced": 9,
    #             "win": true
    #         },