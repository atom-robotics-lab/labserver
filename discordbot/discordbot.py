import discord
import pymongo
from discord.ext import tasks

# MongoDB connection setup
mongo_client = pymongo.MongoClient('')
db_name = ''
collection_name = ''
db = mongo_client[db_name]
collection = db[collection_name]

# Discord bot setup
discord_token = ''
bot = discord.Client()

# MongoDB change stream setup
@tasks.loop(seconds=0)
async def start_change_stream():
    change_stream = collection.watch()
    while True:
        try:
            change = next(change_stream)
            if change['operationType'] == 'insert':
                document = change['fullDocument']
                await send_to_discord(document)
        except StopIteration:
            break

# Sending data to Discord
async def send_to_discord(document):
    channel_id = 
    channel = bot.get_channel(channel_id)

    # Format the document data as desired
    message = f'{document["Name"]} entered into Atom Lab at {document["Time"]} on {document["Date"]}'
    # Send the message to the Discord channel
    await channel.send(message)

# Discord bot event listeners
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    start_change_stream.start()

# Start the Discord bot
bot.run(discord_token)
