import os

from main import Client
from dotenv import load_dotenv

load_dotenv('.env')

client = Client()

client.run(os.getenv("TOKEN"))