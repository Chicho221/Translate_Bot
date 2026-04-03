import discord
import requests
import re
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.reactions = True
intents.message_content = True

LANG_MAP = {
    "🇵🇱": "pl", #Polish
    "🇬🇧": "en", #English
    "🇩🇪": "de", #German
    "🇷🇺": "ru", #Russian
    "🇨🇳": "zh", #Chinese
    "🇻🇳": "vi", #Vietnamese
    "🇬🇷": "el", #Greek
    "🇫🇷": "fr"  #French
}

client = discord.Client(intents=intents)

##FIND ALL EMOJIS
def clean_text(text):
    text = re.sub(r"<a?:\w+:\d+>", "", text)
    return text.strip()

## TRANSLATE LOGIC
def translate(text, target, source):
    response = requests.post("http://localhost:5000/translate", data={
        "q": text,
        "source": source,
        "target": target,
        "format": "text"
    })
    return response.json()["translatedText"]

## PRINT ON LOGIN SUCCESS
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

## ON REACTION EVENT
@client.event
async def on_raw_reaction_add(reaction):

    ## GET CHANNEL
    channel = client.get_channel(reaction.channel_id)

    ## GET MESSAGE
    message = await channel.fetch_message(reaction.message_id)

    ## IGNORE BOT MESSAGES
    if message.author.bot:
        print("This message was sent by bot. Translation stopped.")
        return
    
    ## TRANSLATE BASED ON FLAG EMOJI
    if reaction.emoji.name in LANG_MAP:
        lang = LANG_MAP[reaction.emoji.name]
        cleaned = clean_text(message.content)
        translated_msg = translate(cleaned, lang, "auto")

        await channel.send(translated_msg, reference=message)

## SUPER SECRET CODE | DO NOT SHARE IT!
client.run(TOKEN)