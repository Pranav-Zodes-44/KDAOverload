# KDA Overload
Get specific stats from your recent games, only using your account/summoner name. (Currently only supports League of Legends)

Features added so far: Getting latest LoL Ranked Match info (Summoners, champion played, k/d/a)

Currently using ~~RiotWatcher~~ [Cassiopeia](https://github.com/meraki-analytics/cassiopeia) API framework to assist with the Riot API requests.

Using [Pycord](https://github.com/Pycord-Development/pycord) as my Discord API framework.

||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

So far, only 2 supported commands:

- Last (!!last) - Displays your K/D/A from your last match played of specified queue type. Defaulted to normal draft.
  - Usage: !!last {summoner_name} {region} {optional: queue_type}
    - Works best with discord slash commands instead of this ^
- Match-History (!!match_history) - Shows your last 10 games played of specified queue type, alongside the result of the match and your K/D/A. Defaulted to normal draft.
  - Usage: !!match_history {summoner_name} {region} {optional: queue_type}
    - Works best with discord slash commands instead of this ^
    
More commands and options to come.

||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||


### RIOT_API and Discord bot API key is not available for public use.

If you'd like to use this bot yourself, follow these steps:

- Get your Riot API key from https://developer.riotgames.com/
- Get your Discord API key from https://discord.com/developers/applications
  - Click on your application, and click bot on the side menu. 
  - Then click reset token to get your new token.
  - If you haven't created your bot, go ahead and do so.
- Create a config.txt file in your main directory of the project. 
- On the first line put your Riot API key
- On the second line put your Discord API key
