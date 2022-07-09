## Templates from RiotWater

champ_mastery = lol_watcher.champion_mastery
print(champ_mastery.by_summoner_by_champion(my_region, summ_id, '67'))
### all objects are returned (by default) as a dict
### lets see if i got diamond yet (i probably didnt)
my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
print(my_ranked_stats)
### First we get the latest version of the game from data dragon
versions = lol_watcher.data_dragon.versions_for_region(my_region)
champions_version = versions['n']['champion']
#Get input for champion name
### Lets get some champions
current_champ_list = lol_watcher.data_dragon.champions(champions_version)
jhin = current_champ_list['data']['Jhin']
print(champ_mastery.by_summoner_by_champion(my_region, summ_id, jhin['key']))

For Riot's API, the 404 status code indicates that the requested data wasn't found and
should be expected to occur in normal operation, as in the case of a an
invalid summoner name, match ID, etc.
The 429 status code indicates that the user has sent too many requests
in a given amount of time ("rate limiting").


### Counter for getting top 10 champs played in last 20 games

        played_champs = Counter()
        for match in match_history:
            match = cass.Match.from_match_reference(match)
            champion_id = match.participants[self.summoner].champion.id
            champion_name = champion_id_to_name[champion_id]
            played_champs[champion_name] += 1
        

        print("Number of matches played: ", len(match_history))

        print(f"Top 10 Champions played by {self.summoner.name}: ") 
        for champion_name, count in played_champs.most_common(10):
            print(champion_name, count)   
        print()


### Match History 
    match_history = cass.get_match_history(
                continent = self.summoner.region.continent,
                puuid = self.puuid,
                queue = cass.Queue.normal_draft_fives,
                end_index=4
            )



## Getting all emoji ids from discord bot with item id
### Update with runes when added
    item_ids = []
    emoji_ids = []

    item_to_emoji = dict()

    for guild in bot.guilds:
        if guild.name == "test" or guild.name == "Temple Of Zodes" or guild.name == "Runes":
            continue
        else:
            for emoji in guild.emojis:
                item_ids.append(emoji.name)
                emoji_ids.append(f"<:{emoji.name}:{emoji.id}>")

    for i in range(len(item_ids)):
        item_ = {item_ids[i]: emoji_ids[i]}
        item_to_emoji.update(item_)
    with open("items.json", "w") as items_f:
        json.dump(item_to_emoji, items_f)