# Bwoong Bot
## Description <br>
A simple Discord Bot that simulates the random selection of champions and has functionality to random select a user from a Discord call.

---

## Files
- `.env` : Store the api key of the Discord Bot as `DISCORD_API_KEY=*API KEY HERE*`.
- `/icons`: Stores the chammpion icons download from Riot Games' [Data Dragon](https://developer.riotgames.com/docs/lol#data-dragon) file repository. The downloaded icons take up ~5MB of storage.
- `grid.png`: Is created whenever a new grid of random champions is generated. This is then sent to the corresponding Discord text channel.

---

## Commands
- `/random_user n=<value>`: Randomly chooses n users from the Discord channel that the user is connected to. User must be in the same Discord voice channel.
- `/roll_champs n=<number of champions> ignore_previous=<True/False>`: Randomly chooses n champions. Ignore previous when set to True will ensure that 2 consecutive calls of this command will not have duplicate champions.

---