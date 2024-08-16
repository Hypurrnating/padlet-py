import asyncio
import aiohttp
import typing
from datetime import datetime, timezone, timedelta
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
            content = await resp.json()
            if not resp.status == 200:
                raise Exception(f'Non-200 status code: {content}')
            
            # Populate attributes & relationships
            self.title = content['data']['attributes']['title']
            self.description = content['data']['attributes']['description']
            self.builder.username = content['data']['attributes']['builder']['username']
            self.builder.full_name = content['data']['attributes']['builder']['fullName']
            self.builder.short_name = content['data']['attributes']['builder']['shortName']
            self.builder.avatar_url = content['data']['attributes']['builder']['avatarUrl']
            self.domain_name = content['data']['attributes']['domainName']
            self.icon_url = content['data']['attributes']['iconUrl']
            self.web_url.live = content['data']['attributes']['webUrl']['live']
            self.web_url.qr_code = content['data']['attributes']['webUrl']['qrCode']
            self.web_url.slideshow = content['data']['attributes']['webUrl']['slideshow']
            self.web_url.slideshow_qr_code = content['data']['attributes']['webUrl']['slideshowQrCode']
            self.settings.font = content['data']['attributes']['settings']['font']
            self.settings.color_scheme = content['data']['attributes']['settings']['colorScheme']
            self.created_at = datetime.fromisoformat(content['data']['attributes']['createdAt'])
            self.updated_at = datetime.fromisoformat(content['data']['attributes']['updatedAt'])
            for post in content['data']['relationships']['posts']['data']:
                self.posts[post['id']] = post_object()
            for section in content['data']['relationships']['sections']['data']:
                self.sections[section['id']] = section_object()
            
            # Now populate posts and sections
            for object in content['included']:
                if object['type'] == 'post':
                    post: post_object = self.posts[object['id']]
                    post.author.username = object['attributes']['author']['username']
                    post.author.short_name = object['attributes']['author']['shortName']
                    post.author.full_name = object['attributes']['author']['fullName']
                    post.author.avatar_url = object['attributes']['author']['avatarUrl']
                    post.index = object['attributes']['sortIndex']
                    post.content.subject = object['attributes']['content']['subject']
                    post.content.body_html = object['attributes']['content']['bodyHtml']
                    post.content.attachment.url = object['attributes']['content']['attachment']['url']
                    post.content.attachment.caption = object['attributes']['content']['attachment']['caption']
                    post.content.updated_at = datetime.fromisoformat(object['attributes']['content']['updatedAt'])
                    post.color = object['attributes']['color']
                    post.status = object['attributes']['status']
                    post.map_properties.longitude = object['attributes']['mapProps']['longitude']
                    post.map_properties.latitude = object['attributes']['mapProps']['latitude']
                    post.map_properties.location_name = object['attributes']['mapProps']['locationName']
                    post.canvas_properties.top = object['attributes']['canvasProps']['top']
                    post.canvas_properties.left = object['attributes']['canvasProps']['left']
                    post.canvas_properties.width = object['attributes']['canvasProps']['width']
                    post.web_url.live = object['attributes']['webUrl']['live']
                    post.created_at = datetime.fromisoformat(object['attributes']['createdAt'])
                    post.updated_at = datetime.fromisoformat(object['attributes']['updatedAt'])
                    post.custom_fields = object['attributes']['customFields']

                    # Relations are already created, so just reference them
                    post.section = self.sections[object['relationships']['section']['data']['id']]
                    post.board = self

                if object['type'] == 'section':
                    section: section_object = self.sections[object['id']]
                    section.index = object['attributes']['sortIndex']
                    section.title = object['attributes']['title']
                    section.created_at = datetime.fromisoformat(object['attributes']['createdAt'])
                    section.updated_at = datetime.fromisoformat(object['attributes']['updatedAt'])
                    
                    # Relations are already created so just reference them
                    section.board = self



pad = padlet('pdltp_7d6761555fe960a0b77b20feab7bc5319e6e02ae6ea2a176ae31b81780e0f6064adc7e')
boar = pad.board('eq2dci54eo05spze')
asyncio.run(boar.fetch())
