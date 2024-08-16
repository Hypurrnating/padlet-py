import pytest
import asyncio
import os
os.system('pip install python-dotenv')
import dotenv
dotenv.load_dotenv()

from .padlet import main

def testit():
    asyncio.run(main.padlet(os.environ.get('api_key')).board())