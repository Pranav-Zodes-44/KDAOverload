# KDA Overload
Get specific stats based on certain Riot games from your account, only using your account/summoner name.

Features added so far: Getting latest LoL Ranked Match info (Summoners, champion played, k/d/a)

Currently using ~~RiotWatcher~~ [Cassiopeia](https://github.com/meraki-analytics/cassiopeia) API framework to assist with the Riot API requests.
Going to play around with using [RiotWatcher](https://github.com/pseudonym117/Riot-Watcher) as well.

RIOT_API and Discord bot API key is not available for public use.

If you'd like to use this bot yourself, follow these steps:

- Get your Riot API key from https://developer.riotgames.com/
- Get your Discord API key from https://discord.com/developers/applications
  - Click on your application, and click bot on the side menu. 
  - Then click reset token to get your new token.
  - If you haven't created your bot, go ahead and do so.
- Create a config.txt file in your main directory of the project. 
- On the first line put your Riot API key
- On the second line put your Discord API key
