import asyncio
import aiohttp
import typing
import data_models
from data_models import board_object, section_object, post_object

class padlet:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        
    def board(self, board_id):
        return self._board(self, board_id)

    class _board(board_object):
        def __init__(self, padlet, board_id: int) -> None:
            super().__init__()
            self.padlet = padlet
            self.id = board_id
        
        async def fetch(self, posts: bool = True, sections: bool = True):
            _queries = [name for name, value in locals().items() if name if name in ['posts', 'sections'] and value is True] # allat just to avoid a few more lines.
            queries = "%2C".join(_queries)
            async with aiohttp.ClientSession(headers={'X-Api-Key': self.padlet.api_key}) as connection:
                resp = await connection.get(f'https://api.padlet.dev/v1/boards/{self.id}{f"?include={queries}" if queries else ""}')
            # TODO: handle resp
            print((await resp.read()).decode())



pad = padlet('pdltp_7d6761555fe960a0b77b20feab7bc5319e6e02ae6ea2a176ae31b81780e0f6064adc7e')
boar = pad.board('eq2dci54eo05spze')
asyncio.run(boar.fetch())
