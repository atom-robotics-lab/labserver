
import discord
from pymongo import MongoClient
from discord.ext import tasks

# MongoDB connection setup
client = MongoClient(
        "mongodb+srv://admin:admin@cluster0.cvhcbeg.mongodb.net/?retryWrites=true&w=majority")
db = client.attendence
collection = db.admin

# Discord bot setup
discord_token = 'MTExMzAxMTEwMjM1NjM2MTI3Ng.Gv2SDq.U8LoDm_2cIRnnQAVvu1Je9htCi4ba_mCIBVyd4'
bot = discord.Client(intents=discord.Intents.default())

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
    channel_id = 910183289703264307
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
