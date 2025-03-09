import itertools
import asyncio
import discord
from discord.ext import commands  # , tasks
from spotipy import SpotifyException

from functions import *

class SpotipyBot(commands.Bot):
    def __init__(self, guild_id, channel_id, admin_id, settings, client):
        super().__init__(command_prefix='!', intents=discord.Intents.all())

        self.active_guild_id = guild_id
        self.active_channel_id = channel_id
        self.admin_id = admin_id
        self.spotify_client = client

        self.auto_del_messages = settings['auto_del']

        self.discord_msg = None
        self.status_msg = ""
        self.check_msg = ""

        self.channel = None

        self.search_results = []
        self.queue = []
        self.queue_reset = False
        self.stop = False

        @self.event
        async def on_ready():
            clan = self.get_guild(int(self.active_guild_id))
            self.channel = clan.get_channel(int(self.active_channel_id))


            # Status and stop loop
            print("Bot ready")
            while True:
                if self.stop:
                    await self.discord_msg.delete()
                    await self.close()
                if self.queue_reset:
                    await self.discord_msg.delete()
                    self.discord_msg = None
                await self.status_discord_msg()
                await asyncio.sleep(5)

        # Autodelete messages event
        @self.event
        async def on_message(message):
            if not self.auto_del_messages:
                return
                
            ctx = await self.get_context(message)
            if not await self.channel_check(ctx) or message.author == self.user:
                return
                
            if message.content.startswith('@'):
                await message.delete()
                await self.process_commands(message)
            else:
                await message.delete()  # Deletes all non command messages

        @self.command()
        async def search(ctx, req, req_am: int_or_5 = 5):
            if await self.channel_check(ctx):
                await self.search_song(ctx, req, req_am)
            else:
                print('Wrong channel')

        @self.command()
        async def add(ctx, req):
            if await self.channel_check(ctx):
                await self.play_song(req)
            else:
                print('Wrong channel')
                
        @self.command()
        async def queue(ctx):                               # Resets queue to 
            if not self.auto_del_messages:
                self.queue_reset = True

        @self.command()
        async def skip(ctx):
            if await self.channel_check(ctx):
                self.spotify_client.next_track()
                await asyncio.sleep(1.5)
            else:
                print('Wrong channel')

        @self.command()
        async def stop(ctx):
            if ctx.author == self.get_user(int(self.admin_id)):
                self.stop = True

    # Setup and logic for Status and Queue Message
    async def status_discord_msg(self):
        if not self.discord_msg:
            self.discord_msg = await self.channel.send('Starting...')
            print("Created initial message...")
        try:
            sp_request = self.spotify_client.queue()
            if not sp_request['currently_playing']:
                self.status_msg = 'No device or getting song....'
                print('No device active')
                await self.status_update()
            else:
                current = sp_request['currently_playing']          # Removes the current song from queue
                if self.queue:
                    queue_check = self.queue[0]
                    if (current['name'] == queue_check['name']
                            and current['artists'][0]['name'] == queue_check['artist']):
                        self.queue.pop(0)
                        print("Song removed from queue")

                self.load_status_message(current)  # Funktion to produce message
                await self.status_update()
                print("Updated Status")

        except SpotifyException:
            self.status_msg = 'No device or getting song....'
            await self.status_update()
            print("Loading error: Spotify exeption")

    def load_status_message(self, current_song):
        message = (f"## Currently playing....\n"
                   f"Song: {current_song['name']}\n"
                   f"Artist: {current_song['artists'][0]['name']}\n"
                   f"\n"
                   f"### Queue:\n")
        if len(self.queue) == 0:
            message += 'Empty...'
        else:
            counter = 0
            for i in self.queue:
                message += (f"{counter + 1}. {i['name']}\n"
                            f"Bye:  {i['artist']}\n\n")
                counter += 1
        self.status_msg = message

    async def status_update(self):
        if self.status_msg != self.check_msg:
            self.check_msg = self.status_msg
            await self.discord_msg.edit(content=self.status_msg)

    async def search_song(self, ctx, search, res_amount):
        song_list = self.spotify_search(search, res_amount)

        message = ''                                                   # Creates a message of the results
        for k, v in song_list.items():
            message += (f"{k + 1}\n"
                        f"Song:   {v['name']}\n"
                        f"Artist: {v['artist']}\n"
                        f"Available: {v['av_emoj']}\n"
                        f"         \n")
        message += f"Respond with an available track number"

        temp_msg = await ctx.send(message)                              # Sends message and computes input
        await asyncio.sleep(0.25)
        try:
            message = await self.wait_for('message', timeout=30.00)
            try:
                await self.add_to_queue(song_list[int(message.content) - 1])
            except ValueError:
                await print(f'Error: Message is not a number:\n{message.content}')
        except TimeoutError:
            await print('Error: Time run out')
        finally:
            await temp_msg.delete()
        
    async def play_song(self, search):
        song_list = self.spotify_search(search, 5)
        await self.add_to_queue(song_list[0])

    async def channel_check(self, ctx):
        j_guild = self.get_guild(427935123087032325)
        j_channel = j_guild.get_channel(1198020315272454174)
        s_guild = self.get_guild(1007439660982739025)
        s_channel = s_guild.get_channel(1038995291057180762)
        if ctx.channel == j_channel or ctx.channel == s_channel:
            return True
        else:
            return False

    async def add_to_queue(self, song):
        try:
            self.spotify_client.add_to_queue(song['id'])
            self.queue.append({'name': song['name'], 'artist': song['artist']})
        except spotipy.SpotifyException:
            await print('Error: Track ID out of range')

    def spotify_search(self, req, res_amount):
        counter = 0
        s_list = {}
        av_yes = '<:yes:1197783218733187192>'
        av_no = '<:no:1197783250362437653>'

        result_raw = self.spotify_client.search(q=req)                                      # Requests to Spotify api and creates a dict
        result_item = result_raw['tracks']['items']                             # Sorts out scrap files

        for i in itertools.islice(itertools.cycle(result_item), min(len(result_item), res_amount)):
            av = av_yes if 'DE' in i['available_markets'] else av_no            # Checks available in 'DE'

            s_list[counter] = {'name': i['name'], 'artist': i['artists'][0]['name'],
                           'av_emoj': av, 'id': i['id'], 'url': i['external_urls']}
            counter += 1
        return s_list