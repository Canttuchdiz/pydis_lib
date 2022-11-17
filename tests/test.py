import os

import pydis
from dotenv import load_dotenv

load_dotenv('.env')

client = pydis.Client()

@client.event
async def on_ready():
    print("i love fortnite")

@client.event
async def on_message_create():
    print("I love trees")

@client.event
async def on_message_delete():
    print("Message was deleted")

@client.event
async def hi():
    print("hi")

client.run(os.getenv("TOKEN"))

