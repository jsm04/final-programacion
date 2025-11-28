import os

from dotenv import load_dotenv

load_dotenv()

STRCNX = os.getenv("STRCNX")
PORT = int(os.getenv("PORT", "8000"))
