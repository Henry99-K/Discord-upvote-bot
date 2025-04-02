import discord
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import asyncio



#Loading the discord token

load_dotenv()
TOKEN = os.getenv('TOKEN')

#Configurable settings
MEME_CHANNEL_ID = #channel ID here
BEST_MEME_CHANNEL_ID = #Top meme channel ID here

#Emojis for voting
THUMBS_UP = #upvote emoji ID here
THUMBS_DOWN = #downvote emoji ID here

#Intents
intents = discord.Intents.all()
client = discord.Client(intents=intents)


meme_votes = {}

def calculate_meme_score(meme_data):
    return meme_data['upvotes'] - meme_data['downvotes']

upvote_emoji = None
downvote_emoji = None


    

@client.event
async def on_message(message):
    if message.channel.id == BEST_MEME_CHANNEL_ID:
        if message.content.startswith('!score'):
            #Check if this message is a reply to a meme
            if message.reference:
                referenced_message_id = message.reference.message_id
                if referenced_message_id in meme_votes:
                    score = calculate_meme_score(meme_votes[referenced_message_id])
                    await message.reply(f"This meme's score is: {score}")

        if message.content.startswith('!topmeme'):
            try:
                if meme_votes:  #Check if there are any memes
                    recent_memes = {
                        meme_id: data
                        for meme_id, data in meme_votes.items()
                        if is_meme_recent(data)
                    }
                    if recent_memes:  #initiate if there are recent memes
                        top_meme = max(recent_memes, key=lambda x: calculate_meme_score(recent_memes[x]))
                        top_meme_data = recent_memes[top_meme]
                        channel = client.get_channel(MEME_CHANNEL_ID)
                        top_message = await channel.fetch_message(top_meme)
                        image_url = top_message.attachments[0].url
                        author_name = top_message.author.name
                        embed = discord.Embed(title="Top Meme of the Day", color=0xFFD700)
                        embed.set_image(url=image_url)
                        embed.set_footer(text=f"Upvotes: {top_meme_data['upvotes']} Downvotes: {top_meme_data['downvotes']}")
                        embed.add_field(name="Author:", value=f"{author_name}", inline=False)
                        topchannel = client.get_channel(BEST_MEME_CHANNEL_ID)
                        await topchannel.send(embed=embed)
            except Exception as e:
                print(f"Error in !topmeme command: {e}")

        

    if message.channel.id == MEME_CHANNEL_ID:
        if message.attachments:
            await message.add_reaction(THUMBS_UP)
            await message.add_reaction(THUMBS_DOWN)
            meme_votes[message.id] = {
                    'upvotes': 0,
                'downvotes': 0,
                'timestamp': datetime.now()
            }
    
   

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id == MEME_CHANNEL_ID:
       
        
    
        if reaction.message.id not in meme_votes:
            meme_votes[reaction.message.id] = {
                'upvotes': 0,
                'downvotes': 0,
                'timestamp': datetime.now()
            }
        for r in reaction.message.reactions:
            if str(r.emoji) == THUMBS_UP:
                meme_votes[reaction.message.id]['upvotes'] = r.count - 1
            elif str(r.emoji) == THUMBS_DOWN:
                meme_votes[reaction.message.id]['downvotes'] = r.count - 1


         #Debug
        print(f"Updated votes: {meme_votes[reaction.message.id]}")
      

@client.event
async def on_reaction_remove(reaction, user):
    print(f"DEBUG: Reaction {reaction.emoji} removed by {user}")
    
    if reaction.message.channel.id == MEME_CHANNEL_ID:
        # Update vote counts
        for r in reaction.message.reactions:
            if str(r.emoji) == THUMBS_UP:
                meme_votes[reaction.message.id]['upvotes'] = r.count - 1
            elif str(r.emoji) == THUMBS_DOWN:
                meme_votes[reaction.message.id]['downvotes'] = r.count - 1
        
        #Debug
        print(f"Updated votes: {meme_votes[reaction.message.id]}")

# Making sure the meme is recent
def is_meme_recent(meme_data):
    time_diff = datetime.now() - meme_data['timestamp']
    return time_diff <= timedelta(hours=24) # Time limit for fresh memes



client.run(TOKEN)
