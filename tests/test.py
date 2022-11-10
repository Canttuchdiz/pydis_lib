import os

from pydis import Client
from dotenv import load_dotenv

load_dotenv('.env')

client = Client()

client.run(os.getenv("TOKEN"))

print(client.message_content)