import os

import pydis
from dotenv import load_dotenv

load_dotenv()

client = pydis.Client()

@client.event
async def on_ready() -> None:
    print("i love fortnite")

@client.event
async def on_message_create(message : pydis.Message) -> None:
    print(message.content)


@client.event
async def on_message_delete() -> None:
    print("Message was deleted")


client.run(os.getenv("TOKEN"))

