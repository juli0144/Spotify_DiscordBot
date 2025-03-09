from spotipybot import SpotipyBot

from spotipy.oauth2 import SpotifyOAuth
import spotipy
import configparser
import os.path
import sys


config = configparser.ConfigParser()

# If not avalable creates new ini file
if not os.path.isfile("spotifybot.ini"):
    print("spotifybot.ini not found. Creating File")

    config['Spotify'] = {"client_id": "<your_spotify_client_id>",
                         "client_secret": "<your_spotify_client_secret>",
                         "redirect_uri": "<your_spotify_redirect_uri>",
                         "scope": "user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control user-read-playback-position"}
    config['Discord'] = {"discord_token": "<your_discord_bot_token",
                         "guild_id": "<your_discord_server_id>",
                         "channel_id": "<channel_id_for_the_bot",
                         "admin_id": "<your_discord_id>"}
    config['Settings'] = {"auto_del": "<True/False>"}
    with open('spotifybot.ini', 'w') as configfile:
        config.write(configfile)

    print("File has been created")
    sys.exit()
    
config.read("spotifybot.ini")



# Getting log-in data from file
try:
    with open("config.conf") as file:
        keys = {}
        for i in file:
            k, v = i.strip().split(None, 1)
            keys[k] = v
except FileNotFoundError:
    # something something config file.....
    pass

# Setting up Spotipy
spconf = config['Spotify']
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=spconf['client_id'],
    client_secret=spconf['client_secret'],
    redirect_uri=spconf['redirect_uri'],
    scope=spconf['scope']))


# Starts and connects the bots
if __name__ == "__main__":
    dcconf = config['Discord']
    bot = SpotipyBot(guild_id=dcconf['guild_id'], 
                channel_id=dcconf['channel_id'],
                admin_id=dcconf['admin_id'],
                settings=config['Settings'], 
                client=spotify)
    bot.run(token=dcconf['discord_token'])
