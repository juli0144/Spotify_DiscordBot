# Mybot: Discord Spotify Integration Bot

This is a Discord bot that integrates with Spotify, allowing users to search for songs, queue them, and get status updates on currently playing music. The bot also includes features like auto-deleting non-command messages in a Discord channel and a custom command system.

It is ment to be used in an empty channel which also prevents from intercepting with other bots. If used in a bot channel turn the auto-deleting option off. 

### Table of Contents
1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Usage](#usage)
4. [Dependencies](#dependencies)
5. [Bot Commands](#bot-commands)
6. [Contributing](#contributing)
7. [License](#license)

---

## Requirements

- Python 3.7+
- A Spotify Developer Account to create an app and obtain your client credentials.
- A Discord bot token.
- Access to a Discord server where the bot will operate.

---

## Setup

### Step 1: Install Dependencies

Ensure you have Python 3.7+ installed, then install the required dependencies by running the following command:

~~~
pip install -r requirements.txt
~~~

### Step 2: Edit the `spotifybot.ini` file

The bot requires a configuration file containing your Spotify and Discord credentials as well as server/channel ID's. A File spotifybot.ini will be created on first Startup if the file is missing.


You will need to get ID's from your Server, the desired Channel and a User. To get the ID's simply turn on developer mode in the Discord settings, then by right clicking your server, channel or users. guild_id means your Discord Server id and admin_id does not mean discord token. 


---

## Usage

To run the bot, simply execute the `main.py` file:

~~~
python main.py
~~~~

Once the bot is running, it will automatically connect to Discord and Spotify using the credentials specified in the `config.conf` file. The bot will start responding to commands in the designated Discord channel. 

You may be asked to copy a URL into the console to vertify for the Spotify api. Just do as told and copy the new opened browser-tab url into the console. Depending on the console you might need to use (ctrl+shift+v) 

---

## Dependencies

The following Python packages are required for the bot to function:

- `spotipy`: A Python library for the Spotify Web API.
- `discord.py`: A Python library for interacting with the Discord API.
- `asyncio`: A standard Python library for asynchronous programming.

These dependencies are automatically installed via the `requirements.txt` file, which includes:


spotipy
discord.py


You can install the dependencies manually using `pip` if necessary.

---

## Bot Commands

The bot supports several commands:

### `!search <song_name> <number_of_results>`
Searches for songs on Spotify and returns a list of results. You can specify the number of results (default is 5, up to 10) to be returned.

Example:
~~~
!search Shape of You
~~~

### `!add <song_name>`
Adds the first song from the search results to the queue.

Example:
~~~
!add Blinding Lights
~~~

### `!queue`
If autodelete of messages is off creates a new message to show queue.

### `!skip`
Skips the currently playing song.

### `!stop`
Stops the bot (can only be executed by the admin).

---

## Contributing

Feel free to fork this project, submit issues, and make pull requests. Contributions are always welcome!

1. Fork the repository.
2. Create a new branch (\`git checkout -b feature-name\`).
3. Make changes and commit them (\`git commit -am 'Add new feature'\`).
4. Push to your branch (\`git push origin feature-name\`).
5. Create a new pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
